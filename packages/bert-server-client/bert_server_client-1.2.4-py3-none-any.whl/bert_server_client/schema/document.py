from dataclasses import dataclass
from typing import List

from bert_server_client.schema.base import Base
from bert_server_client.schema.split import Split


@dataclass
class Document(Base):
    """
    Dataclass representing a Document response.
    """
    document_id: int
    splits: List[Split]
