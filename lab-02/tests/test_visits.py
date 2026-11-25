import app as shop


def test_visits_counts_up(client):
    assert client.get("/visits").get_json()["visits"] == 1
    assert client.get("/visits").get_json()["visits"] == 2


def test_visits_reports_the_file_store(client):
    r = client.get("/visits")
    assert r.status_code == 200
    assert r.get_json()["store"] == "file"


def test_visits_are_written_to_the_counter_file(client, tmp_path):
    client.get("/visits")
    client.get("/visits")
    assert (tmp_path / "visits.txt").read_text() == "2"


def test_visits_answers_503_when_the_counter_cannot_be_written(client, tmp_path, monkeypatch):
    blocker = tmp_path / "not-a-directory"
    blocker.write_text("")
    monkeypatch.setattr(shop, "COUNTER_FILE", blocker / "visits.txt")

    r = client.get("/visits")
    assert r.status_code == 503
    body = r.get_json()
    assert body["store"] == "file"
    assert "error" in body
