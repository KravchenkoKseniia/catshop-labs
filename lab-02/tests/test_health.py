def test_health_says_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.data == b"ok\n"
