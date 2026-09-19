import os, tempfile
os.environ["DATABASE"] = os.path.join(tempfile.mkdtemp(), "test.db")
from app import app

c = app.test_client()

def test_flow():
    r = c.post("/api/shorten", json={"url": "www.codealpha.tech"})
    assert r.status_code == 201
    code = r.get_json()["short_code"]
    r2 = c.post("/api/shorten", json={"url": "https://www.codealpha.tech"})
    assert r2.get_json()["short_code"] == code            # duplicate re-used
    r3 = c.get("/" + code)
    assert r3.status_code == 302 and r3.headers["Location"] == "https://www.codealpha.tech"
    assert c.get("/api/stats/" + code).get_json()["clicks"] == 1

def test_errors():
    assert c.post("/api/shorten", json={"url": "not a url"}).status_code == 400
    assert c.get("/nope123").status_code == 404
    assert c.post("/api/shorten", json={"url": "https://a.com", "custom_code": "mine"}).status_code == 201
    assert c.post("/api/shorten", json={"url": "https://b.com", "custom_code": "mine"}).status_code == 409
    assert c.get("/").status_code == 200
