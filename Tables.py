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
	__tablename__ = "vibes"
	
	id: int = Column("id", Integer, primary_key=True),
	title: str = Column("title", Text),
	contents: str = Column("contents", Text, nullable=False),
	upvotes: int = Column("upvotes", Integer),
	sentiment: int =  Column("sentiment", Integer),
	source_url: str = Column("source_url", String, nullable=False),
	last_updated: datetime = Column("last_updated", Date(), nullable=False)
