def test_ready_reports_the_file_store(client):
    r = client.get("/ready")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ready"] is True
    assert body["store"].startswith("file:")
