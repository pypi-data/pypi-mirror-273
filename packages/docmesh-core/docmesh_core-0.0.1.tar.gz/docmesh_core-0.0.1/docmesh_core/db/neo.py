import os
import pandas as pd

from typing import Any
from pandas.core.frame import DataFrame

from neomodel import db
from neomodel import (
    StructuredNode,
    StructuredRel,
    StringProperty,
    IntegerProperty,
    FloatProperty,
    DateTimeProperty,
    ArrayProperty,
    RelationshipTo,
    RelationshipFrom,
)
from neomodel.integration.pandas import to_dataframe

from ..utils.semantic_scholar import (
    get_paper_id_from_title,
    get_paper_id_from_arxiv,
    get_references,
    get_paper_details,
    PaperIdNotFound,
)


class FollowRel(StructuredRel):
    since = DateTimeProperty(default_now=True, index=True)


class ReadRel(StructuredRel):
    read_time = DateTimeProperty(default_now=True, index=True)


class Entity(StructuredNode):
    name = StringProperty(unique_index=True)

    reads = RelationshipTo("Paper", "read", model=ReadRel)
    follows = RelationshipTo("Entity", "follow", model=FollowRel)
    followers = RelationshipFrom("Entity", "follow", model=FollowRel)

    @property
    def serialize(self) -> dict[str, Any]:
        data = {"name": self.name}
        return data


class Paper(StructuredNode):
    paper_id = StringProperty(unique_index=True)
    title = StringProperty()
    abstract = StringProperty()
    summary = StringProperty()
    publication_date = DateTimeProperty()
    reference_count = IntegerProperty()
    citation_count = IntegerProperty()
    pdf = StringProperty()
    # openai text-embedding-3-large cast to 1024
    embedding_te3l = ArrayProperty(FloatProperty())

    readers = RelationshipFrom("Entity", "read", model=ReadRel)
    references = RelationshipTo("Paper", "cite")
    citations = RelationshipFrom("Paper", "cite")

    @property
    def serialize(self) -> dict[str, Any]:
        data = {
            "paper_id": self.paper_id,
            "title": self.title,
            "abstract": self.abstract,
            "summary": self.summary,
            "publication_date": self.publication_date,
            "reference_count": self.reference_count,
            "citation_count": self.citation_count,
            "pdf": self.pdf,
        }
        return data


def _nodelist_to_dataframe(nodes: list[StructuredNode]) -> DataFrame:
    df = pd.DataFrame.from_dict([node.serialize for node in nodes])
    return df


def get_entity(entity_name: str) -> Entity:
    entity = Entity.nodes.get(name=entity_name)
    return entity


@db.transaction
def add_entity(entity_name: str) -> Entity:
    entity: Entity = Entity.create_or_update({"name": entity_name})
    return entity


@db.transaction
def follow_entity(follower_name: str, follow_name: str) -> None:
    follower_entity = get_entity(follower_name)
    followed_entity = get_entity(follow_name)
    # XXX: neomodel says that they can ensure relationship uniqueness
    # however, it doesn't
    if not follower_entity.follows.is_connected(followed_entity):
        follower_entity.follows.connect(followed_entity)


@db.transaction
def list_follows(entity_name: str) -> DataFrame:
    entity = get_entity(entity_name)
    follows: list[Entity] = entity.follows.all()
    return _nodelist_to_dataframe(follows)


@db.transaction
def list_popular_entities(n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e:Entity)
        RETURN e.name AS name,
        COUNT {
            (:Entity) -[:follow]-> (e)
        } AS num_followers,
        COUNT {
            (e) -[:read]-> (:Paper)
        } AS num_reads
        ORDER BY num_followers DESC, num_reads DESC
        LIMIT $n
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "n": n,
            },
        )
    )

    return df


def get_paper_from_id(paper_id: str) -> Paper:
    paper = Paper.nodes.get(paper_id=paper_id)
    return paper


def get_paper_from_title(title: str) -> Paper:
    paper = Paper.nodes.get(title=title)
    return paper


@db.transaction
def _add_paper_references(paper: DataFrame, references: DataFrame) -> Paper:
    paper: Paper = Paper.create_or_update(*paper.to_dict(orient="records"))[0]

    if references.shape[0] != 0:
        references: list[Paper] = Paper.create_or_update(*references.to_dict(orient="records"))

        for reference in references:
            # XXX: neomodel says that they can ensure relationship uniqueness
            # however, it doesn't
            if not paper.references.is_connected(reference):
                paper.references.connect(reference)

    return paper


def _add_paper(paper_id: str) -> Paper:
    if paper_id is None:
        raise PaperIdNotFound(f"Cannot find semantic scholar paper id for {title}.")
    paper = get_paper_details([paper_id])

    references_ids = get_references(paper_id)
    if len(references_ids) == 0:
        references = pd.DataFrame()
    else:
        references = get_paper_details(references_ids)

    paper = _add_paper_references(paper, references)
    return paper


def add_paper_from_title(title: str) -> Paper:
    if (paper_id := get_paper_id_from_title(title)) is None:
        raise PaperIdNotFound(f"Cannot find semantic scholar paper id from title {title}.")

    paper = _add_paper(paper_id)
    return paper


def add_paper_from_arxiv(arxiv_id: str) -> Paper:
    if (paper_id := get_paper_id_from_arxiv(arxiv_id)) is None:
        raise PaperIdNotFound(f"Cannot find semantic scholar paper id from arxiv {arxiv_id}.")

    paper = _add_paper(paper_id)
    return paper


@db.transaction
def read_paper(entity_name: str, paper_id: str) -> None:
    entity = get_entity(entity_name)
    paper = get_paper_from_id(paper_id=paper_id)
    # XXX: neomodel says that they can ensure relationship uniqueness
    # however, it doesn't
    if not entity.reads.is_connected(paper):
        entity.reads.connect(paper)


@db.transaction
def list_latest_papers(entity_name: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e:Entity) -[r:read]-> (p:Paper)
        WHERE e.name = $entity_name
        RETURN p.paper_id AS paper_id, p.title AS title
        ORDER BY r.read_time DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "entity_name": entity_name,
                "n": n,
            },
        )
    )

    return df


@db.transaction
def list_unread_similar_papers(entity_name: str, paper_id: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (p0:Paper)
        WHERE p0.paper_id = $paper_id
        CALL db.index.vector.queryNodes('vector_embedding_te3l', $n, p0.embedding_te3l)
        YIELD node AS p, score
        WHERE NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $entity_name 
        }
        RETURN p.title AS title, p.pdf AS pdf, score
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "entity_name": entity_name,
                "paper_id": paper_id,
                "n": n,
            },
        )
    )

    return df


@db.transaction
def list_unread_semantic_papers(entity_name: str, semantic_embedding: list[float], n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        CALL db.index.vector.queryNodes('vector_embedding_te3l', $n, $semantic_embedding)
        YIELD node AS p, score
        WHERE NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $entity_name 
        }
        RETURN p.title AS title, p.pdf AS pdf, score
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "entity_name": entity_name,
                "semantic_embedding": semantic_embedding,
                "n": n,
            },
        )
    )

    return df


@db.transaction
def list_unread_follows_papers(entity_name: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e1:Entity) -[:follow]-> (:Entity) -[r:read]-> (p:Paper)
        WHERE e1.name = $name
        AND NOT EXISTS {
            (p) <-[:read]- (e2:Entity)
            WHERE e2.name = $entity_name
        }
        RETURN p.title AS title, p.pdf AS pdf
        ORDER BY r.read_time, p.citation_count DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "entity_name": entity_name,
                "n": n,
            },
        )
    )

    return df


@db.transaction
def list_unread_influential_papers(entity_name: str, date_time: str) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (p:Paper)
        WHERE p.publication_date >= DATETIME($date_time).epochSeconds
        AND NOT EXISTS {
            (p) <-[:read]- (e:Entity)
            WHERE e.name = $entity_name
        }
        RETURN p.title AS title, p.pdf AS pdf
        ORDER BY p.citation_count DESC
        limit 10;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "entity_name": entity_name,
                "date_time": date_time,
            },
        )
    )

    return df


@db.transaction
def get_latest_citegraph(entity_name: str, n: int) -> DataFrame:
    # XXX: use cypher query language, since OGM is not well supported
    query = """
        MATCH (e1:Entity) -[r:read]-> (p1:Paper) -[:cite]-> (p2:Paper) <-[:read]- (e2:Entity)
        WHERE e1.name = $name AND e2.name = $entity_name
        RETURN p1.paper_id AS p1_paper_id, p2.paper_id AS p2_paper_id
        ORDER BY r.read_time DESC
        LIMIT $n;
    """
    df = to_dataframe(
        db.cypher_query(
            query,
            params={
                "entity_name": entity_name,
                "n": n,
            },
        )
    )

    return df
