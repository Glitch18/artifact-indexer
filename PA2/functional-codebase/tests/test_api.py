# Stack: Python 3.13 / pytest / HTTPX
# AI contribution: 67%; human contribution: 33%.
# Construction brief: ../../.ai_logs/functional-brief.md
import hashlib
import io
import os
from uuid import UUID
import zipfile

import httpx
import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture
def client(tmp_path):
    base_url = os.getenv("PA2_BASE_URL")
    if base_url:
        with httpx.Client(base_url=base_url, follow_redirects=True, timeout=30) as c:
            yield c
    else:
        with TestClient(create_app(f"sqlite:///{tmp_path}/test.db", tmp_path / "files")) as c:
            yield c


@pytest.fixture
def payload():
    return {"title": "Research artifact catalog", "description": "Local robotics capstone",
            "members": [{"id": "alice", "role": "student"}, {"id": "prof-one", "role": "faculty"}],
            "units": [{"type": "lab", "id": "lab-robotics"}, {"type": "department", "id": "dept-cs"},
                      {"type": "course", "id": "CS763"}]}


@pytest.fixture
def project(client, payload):
    response = client.post("/api/v1/projects", json=payload)
    assert response.status_code == 201, response.text
    p = response.json()
    yield p
    client.delete(f"/api/v1/projects/{p['id']}")


def test_health(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_project_lifecycle(client, project, payload):
    pid = project["id"]
    assert str(UUID(pid)) == pid
    assert project["revision"] == 1
    assert project["members"] == payload["members"]
    assert project["units"] == payload["units"]
    assert project["created_at"] and project["updated_at"]
    assert client.get(f"/api/v1/projects/{pid}").json() == project
    updated = {**payload, "title": "Revised project"}
    response = client.put(f"/api/v1/projects/{pid}", json=updated)
    assert response.status_code == 200
    assert response.json()["revision"] == 2
    assert response.json()["title"] == "Revised project"
    assert client.delete(f"/api/v1/projects/{pid}").status_code == 204
    assert client.get(f"/api/v1/projects/{pid}").status_code == 404


@pytest.mark.parametrize("kind,metadata", [
    ("repositories", {"repo_url": "https://example.org/lab/robot", "target_branch": "main", "primary_tech_stack": "Python", "total_commit_count": 17, "latest_commit_timestamp": "2026-11-01T00:00:00Z"}),
    ("videos", {"video_url": "https://example.org/video", "thumbnail_url": "https://example.org/image.png", "duration": 120, "description": "Demo"}),
    ("manuscripts", {"title": "A paper", "abstract": "A robot", "authors": ["Alice"], "keywords": ["robotics"], "year": 2026, "publisher": "Local demo"}),
])
def test_artifact_lifecycle(client, project, kind, metadata):
    prefix = f"/api/v1/projects/{project['id']}/artifacts/{kind}"
    response = client.post(prefix + "/", json=metadata)
    assert response.status_code == 201, response.text
    a = response.json()
    UUID(a["id"])
    assert a["metadata"] == metadata
    assert client.get(prefix + "/").json() == [a]
    assert a in client.get(f"/api/v1/projects/{project['id']}/artifacts").json()
    assert client.get(prefix + "/" + a["id"]).json() == a
    revised = {**metadata, "description": "Updated metadata"}
    assert client.put(prefix + "/" + a["id"], json=revised).json()["metadata"] == revised
    assert client.delete(prefix + "/" + a["id"]).status_code == 204
    assert client.get(prefix + "/" + a["id"]).status_code == 404


def test_manuscript_upload_download_hash_zip_delete(client, project):
    base = f"/api/v1/projects/{project['id']}/artifacts/manuscripts"
    ids = []
    for number in range(2):
        a = client.post(base + "/", json={"title": f"Manuscript {number}"}).json()
        ids.append(a["id"])
        content = f"%PDF-1.4 course fixture {number}".encode()
        response = client.post(f"{base}/{a['id']}/file", files={"file": ("paper.pdf", content, "application/pdf")})
        assert response.status_code == 200, response.text
        assert response.json()["file"]["sha256"] == hashlib.sha256(content).hexdigest()
        assert response.json()["file"]["size"] == len(content)
        assert client.get(f"{base}/{a['id']}/file").content == content
    archive = client.get(base + "/download")
    assert archive.status_code == 200
    with zipfile.ZipFile(io.BytesIO(archive.content)) as z:
        assert len(z.namelist()) == 2
        for number, aid in enumerate(ids):
            assert z.read(f"{aid}/paper.pdf") == f"%PDF-1.4 course fixture {number}".encode()
    assert client.delete(f"{base}/{ids[0]}/file").status_code == 204
    assert client.get(f"{base}/{ids[0]}/file").status_code == 404
    assert client.get(f"{base}/{ids[0]}").json()["file"] is None


@pytest.mark.parametrize("query", [
    {"keyword": "robotics"}, {"dept_id": "dept-cs", "lab_id": "lab-robotics", "course_id": "CS763"},
    {"created_after": "2020-01-01", "created_before": "2100-01-01"},
    {"keyword": "research", "artifact_type": "repositories", "course_id": "CS763"},
])
def test_search_filters(client, project, query):
    client.post(f"/api/v1/projects/{project['id']}/artifacts/repositories/", json={"repo_url": "https://example.org/repo"})
    response = client.get("/api/v1/projects", params=query)
    assert response.status_code == 200
    assert project["id"] in {p["id"] for p in response.json()}
    assert project["id"] not in {p["id"] for p in client.get("/api/v1/projects", params={"lab_id": "nonexistent"}).json()}


def test_project_delete_removes_artifacts(client, project):
    pid = project["id"]
    a = client.post(f"/api/v1/projects/{pid}/artifacts/videos/", json={"video_url": "https://example.org/demo"}).json()
    assert client.delete(f"/api/v1/projects/{pid}").status_code == 204
    assert client.get(f"/api/v1/projects/{pid}/artifacts/videos/{a['id']}").status_code == 404
