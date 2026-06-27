import app as flask_app


def test_add():
    assert flask_app.add(2, 3) == 5
    assert flask_app.add(-1, 1) == 0


def test_home_route():
    client = flask_app.app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_health_route():
    client = flask_app.app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_add_route():
    client = flask_app.app.test_client()
    resp = client.get("/add/4/6")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 10
