import concurrent
import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict

import pytest
from bert_server_client.client import BertClient
from bert_server_client.schema.embedding import EmbeddingRequest, EmbeddingResponse, EmbeddingQueryRequest, EmbeddingQueryResponse
from bert_server_client.schema.health_check import HealthCheck


@pytest.fixture
def bert_client():
    host = "tcp://localhost:5555"
    client = BertClient(host)
    yield client
    client.close()


def test_request_to_bert_server(bert_client):
    request = EmbeddingRequest(
        input=['I like icecream', 'geopolitical policy', 'what is this thing here', 'no thats wrong'],
        model="test_model", user=uuid.uuid4())
    response = bert_client.send_embedding_request(request)

    assert response is not None
    assert isinstance(response, EmbeddingResponse)
    print(json.dumps(asdict(response), indent=4))


def test_request_to_bert_server_with_doc_url(bert_client):
    request = EmbeddingRequest(
        input=['I like icecream', 'geopolitical policy', 'what is this thing here', 'no thats wrong'],
        model="test_model", user=uuid.uuid4(), doc_id="https://www.google.com/important_document")
    response = bert_client.send_embedding_request(request)

    assert response is not None
    assert isinstance(response, EmbeddingResponse)
    print(json.dumps(asdict(response), indent=4))


def test_query_request_to_bert_server(bert_client):
    request = EmbeddingQueryRequest(
        input="What do I like to eat?", 
        model="test_model", user=uuid.uuid4())
    response = bert_client.send_embedding_query_request(request)

    assert response is not None
    assert isinstance(response, EmbeddingQueryResponse)
    print(json.dumps(asdict(response), indent=4))

    return json.dumps(asdict(response), indent=4)


def test_load_test_bert_server(num_requests: int = 10):
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        clients = [BertClient("tcp://localhost:5555") for _ in range(num_requests)]
        future_to_request = {executor.submit(test_request_to_bert_server, client): i for i, client in
                             enumerate(clients)}
        for future in concurrent.futures.as_completed(future_to_request):
            request_id = future_to_request[future]
            try:
                data = future.result()
                print(f"Request {request_id} completed: {data}")
            except Exception as exc:
                print(f"Request {request_id} generated an exception: {exc}")

        for client in clients:
            client.close()


def test_health_check(bert_client):
    response = bert_client.send_health_check_request()

    assert response is not None
    assert isinstance(response, HealthCheck)
    print(json.dumps(asdict(response), indent=4))
