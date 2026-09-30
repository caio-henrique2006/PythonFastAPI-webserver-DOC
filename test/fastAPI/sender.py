import json
from urllib import error, request

BASE_URL = "http://127.0.0.1:8000"


def send_request(method: str, path: str, payload=None):
    url = BASE_URL + path
    headers = {"Content-Type": "application/json"}
    body = None

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = request.Request(url, data=body, headers=headers, method=method)

    try:
        with request.urlopen(req, timeout=10) as response:
            response_body = response.read().decode("utf-8")
            print(f"{method} {path} -> {response.status} {response_body}")
    except error.HTTPError as http_error:
        response_body = http_error.read().decode("utf-8")
        print(f"{method} {path} -> {http_error.code} {response_body}")
    except Exception as exc:
        print(f"{method} {path} -> ERROR: {exc}")


if __name__ == "__main__":
    print("Example requests to the FastAPI server")
    print("Make sure the server is running first:")
    print("uvicorn main:app --reload --host 127.0.0.1 --port 8000")
    print("-" * 50)

    # GET /
    send_request("GET", "/")

    # GET /people
    send_request("GET", "/people")

    # GET /people/1
    send_request("GET", "/people/1")

    # POST /people
    send_request(
        "POST",
        "/people",
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
        },
    )

    # GET /people/1 after creation
    send_request("GET", "/people/1")

    # PUT /people/1
    send_request(
        "PUT",
        "/people/1",
        {
            "id": 1,
            "name": "Alice Updated",
            "email": "alice.updated@example.com",
        },
    )

    # GET /people to list all
    send_request("GET", "/people")

    # DELETE /people/1
    send_request("DELETE", "/people/1")

    # GET /people after delete
    send_request("GET", "/people")
