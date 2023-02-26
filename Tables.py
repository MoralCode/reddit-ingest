from dataclasses import dataclass

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String, Text, Date
from sqlalchemy import Table
from sqlalchemy.orm import registry
from datetime import datetime

mapper_registry = registry()

@mapper_registry.mapped
@dataclass
class Vibes:
    __table__ = Table(
        "vibes",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("title", Text),
        Column("contents", Text, nullable=False),
        Column("upvotes", Integer),
        Column("total_votes", Integer),
        Column("sentiment", Integer),
        Column("source_url", String, nullable=False),
        Column("last_updated", Date(), nullable=False)
    )
    title: str
    contents: str
    upvotes: int
    total_votes: int
    sentiment: int
    source_url: str
    last_updated: datetime

@mapper_registry.mapped
@dataclass
class CommentVibes:
    __table__ = Table(
        "comment_vibes",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("parent_id", Integer),
        Column("contents", Text, nullable=False),
        Column("sentiment", Integer),
    )
    parent_id: int
    contents: str
    sentiment: int
