from uuid import UUID, uuid4
from dataclasses import dataclass
from typing import Optional, Dict, Any

from polyfactory.factories import DataclassFactory

from bert_server_client.schema.base import Base
from bert_server_client.schema.embedding import EmbeddingRequest, EmbeddingResponse, EmbeddingQueryRequest, EmbeddingQueryResponse


@dataclass
class MyMapClass(Base):
    dummy: str
    key_values: Optional[Dict[str, Any]] = None  # Optional key_values for advanced options

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "session": UUID,
        }


def test_map_class():
    """
    Test if the datetime encoding and decoding works correctly.
    """

    my_map_class = MyMapClass(
        dummy="test",
        key_values={"session": uuid4()}
    )

    print(my_map_class)

    packed = my_map_class.msgpack_pack()

    print(packed)

    unpacked = MyMapClass.msgpack_unpack(packed)

    print(unpacked)

    assert my_map_class == unpacked


class EmbeddingRequestFactory(DataclassFactory[EmbeddingRequest]):
    __model__ = EmbeddingRequest


def test_embedding_request_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    request = EmbeddingRequestFactory.build()

    print(request.to_json_str())

    packed = request.msgpack_pack()

    unpacked = EmbeddingRequest.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert request == unpacked


class EmbeddingResponseFactory(DataclassFactory[EmbeddingResponse]):
    __model__ = EmbeddingResponse


def test_embedding_response_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    embedding_response = EmbeddingResponseFactory.build()

    print(embedding_response.to_json_str())

    packed = embedding_response.msgpack_pack()

    unpacked = embedding_response.msgpack_unpack(packed)

    print(unpacked.to_json_str())

    assert embedding_response == unpacked


# Duplicate for EmbeddingQuery


class EmbeddingQueryRequestFactory(DataclassFactory[EmbeddingQueryRequest]):
    __model__ = EmbeddingQueryRequest


def test_embedding_query_request_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    query_request = EmbeddingQueryRequestFactory.build()
    print(query_request.to_json_str())
    packed_request = query_request.msgpack_pack()
    unpacked_request = EmbeddingQueryRequest.msgpack_unpack(packed_request)
    assert query_request == unpacked_request


class EmbeddingQueryResponseFactory(DataclassFactory[EmbeddingQueryResponse]):
    __model__ = EmbeddingQueryResponse


def test_embedding_query_response_factory():
    """
    Test if the datetime encoding and decoding works correctly.
    """
    query_response = EmbeddingQueryResponseFactory.build()
    print(query_response.to_json_str())
    packed_response = query_response.msgpack_pack()
    unpacked_response = EmbeddingQueryResponse.msgpack_unpack(packed_response)
    assert query_response == unpacked_response
