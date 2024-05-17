from typing import Union, List, Optional, Dict, Any
from dataclasses import dataclass, field
from uuid import UUID

from bert_server_client.schema.base import Base
from bert_server_client.schema.split import Split


@dataclass
class Embedding:
    object: str
    index: int
    embedding: List[float]


@dataclass
class EmbeddingUsage:
    prompt_tokens: int
    total_tokens: int


@dataclass
class EmbeddingResponse(Base):
    object: str
    data: List[Embedding]
    model: Optional[str] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)


@dataclass
class EmbeddingQueryResponse(Base):
    object: str
    data: List[Split]
    model: Optional[str] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)


@dataclass
class EmbeddingRequest(Base):
    input: Union[str, List[str]]
    model: str
    encoding_format: Optional[str] = field(default="float")
    dimensions: Optional[int] = field(default=None)
    user: Optional[UUID] = field(default=None)
    doc_id: Optional[str] = field(default=None) # Currently mocked not derived from URL

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }
    

@dataclass
class EmbeddingQueryRequest(Base):
    input: str
    model: str
    encoding_format: Optional[str] = field(default="float")
    dimensions: Optional[int] = field(default=None)
    user: Optional[UUID] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }
