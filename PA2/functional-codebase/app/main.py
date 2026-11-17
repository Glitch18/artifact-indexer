# Stack: Python 3.13 / FastAPI / SQLAlchemy
# Tool: OpenAI Codex desktop; AI contribution: 65%; human contribution: 35%.
# Human verification: 33%; automated evidence is recorded separately.
# Construction brief: .ai_logs/functional-brief.md; history: .ai_logs/prompt-history.md
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import os
from typing import Literal
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from fastapi import Body, Depends, FastAPI, File, HTTPException, Query, Request, Response, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import JSON, ForeignKey, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

ArtifactType = Literal["manuscripts", "videos", "repositories"]


def now():
    return datetime.now(timezone.utc).isoformat()


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    members: Mapped[list] = mapped_column(JSON)
    units: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[str] = mapped_column(String(40))
    updated_at: Mapped[str] = mapped_column(String(40))
    revision: Mapped[int] = mapped_column(Integer)


class Artifact(Base):
    __tablename__ = "artifacts"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[str] = mapped_column(String(40))
    updated_at: Mapped[str] = mapped_column(String(40))
    file_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    filename: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ProjectInput(BaseModel):
    title: str
    description: str = ""
    members: list[dict] = Field(min_length=1)
    units: list[dict] = Field(min_length=1)


def project_json(p):
    return {k: getattr(p, k) for k in ("id", "title", "description", "members", "units", "created_at", "updated_at", "revision")}


def artifact_json(a):
    return {"id": a.id, "project_id": a.project_id, "artifact_type": a.kind,
            "metadata": a.data, "created_at": a.created_at, "updated_at": a.updated_at,
            "file": {"filename": a.filename, "sha256": a.file_hash, "size": a.file_size} if a.file_path else None}


def get_session(request: Request):
    with Session(request.app.state.engine) as session:
        yield session


def get_project(session, project_id):
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(404, "Project not found")
    return project


def get_artifact(session, project_id, kind, artifact_id):
    get_project(session, project_id)
    artifact = session.get(Artifact, artifact_id)
    if artifact is None or artifact.project_id != project_id or artifact.kind != kind:
        raise HTTPException(404, "Artifact not found")
    return artifact


def remove_binary(artifact):
    if artifact.file_path:
        Path(artifact.file_path).unlink(missing_ok=True)
    artifact.file_path = artifact.filename = artifact.file_hash = artifact.file_size = None


def create_app(database_url=None, storage_dir=None):
    url = database_url or os.getenv("DATABASE_URL", "sqlite:///./baseline.db")
    storage = Path(storage_dir or os.getenv("STORAGE_DIR", "./data/manuscripts"))
    engine = create_engine(url, **({"connect_args": {"check_same_thread": False}} if url.startswith("sqlite") else {}))

    @asynccontextmanager
    async def lifespan(app):
        storage.mkdir(parents=True, exist_ok=True)
        Base.metadata.create_all(engine)
        yield
        engine.dispose()

    app = FastAPI(title="Project Artifact & Repository Indexer — PA2", lifespan=lifespan)
    app.state.engine = engine

    @app.get("/healthz")
    def health():
        return {"status": "ok"}

    @app.post("/api/v1/projects", status_code=201)
    def create_project(body: ProjectInput, session: Session = Depends(get_session)):
        stamp = now()
        project = Project(id=str(uuid4()), **body.model_dump(), created_at=stamp, updated_at=stamp, revision=1)
        session.add(project)
        session.commit()
        return project_json(project)

    @app.get("/api/v1/projects")
    def search(keyword: str | None = None, dept_id: str | None = None, lab_id: str | None = None,
               course_id: str | None = None, created_after: str | None = None, created_before: str | None = None,
               artifact_type: ArtifactType | None = None, session: Session = Depends(get_session)):
        statement = select(Project).order_by(Project.created_at, Project.id)
        if keyword:
            statement = statement.where(Project.title.ilike(f"%{keyword}%") | Project.description.ilike(f"%{keyword}%"))
        if created_after:
            statement = statement.where(Project.created_at >= created_after)
        if created_before:
            statement = statement.where(Project.created_at <= created_before)
        projects = session.scalars(statement).all()
        for kind, unit_id in (("department", dept_id), ("lab", lab_id), ("course", course_id)):
            if unit_id:
                projects = [p for p in projects if any(u.get("type") == kind and u.get("id") == unit_id for u in p.units)]
        if artifact_type:
            ids = set(session.scalars(select(Artifact.project_id).where(Artifact.kind == artifact_type)))
            projects = [p for p in projects if p.id in ids]
        return [project_json(p) for p in projects]

    @app.get("/api/v1/projects/{project_id}")
    def read_project(project_id: str, session: Session = Depends(get_session)):
        return project_json(get_project(session, project_id))

    @app.put("/api/v1/projects/{project_id}")
    def update_project(project_id: str, body: ProjectInput, session: Session = Depends(get_session)):
        project = get_project(session, project_id)
        for key, value in body.model_dump().items():
            setattr(project, key, value)
        project.revision += 1
        project.updated_at = now()
        session.commit()
        return project_json(project)

    @app.delete("/api/v1/projects/{project_id}", status_code=204)
    def delete_project(project_id: str, session: Session = Depends(get_session)):
        project = get_project(session, project_id)
        for artifact in session.scalars(select(Artifact).where(Artifact.project_id == project_id)).all():
            remove_binary(artifact)
            session.delete(artifact)
        session.delete(project)
        session.commit()
        return Response(status_code=204)

    @app.get("/api/v1/projects/{project_id}/artifacts")
    def all_artifacts(project_id: str, session: Session = Depends(get_session)):
        get_project(session, project_id)
        return [artifact_json(a) for a in session.scalars(select(Artifact).where(Artifact.project_id == project_id).order_by(Artifact.id))]

    # Register the fixed download route before routes containing artifact IDs.
    @app.get("/api/v1/projects/{project_id}/artifacts/manuscripts/download")
    def download_zip(project_id: str, session: Session = Depends(get_session)):
        get_project(session, project_id)
        output = BytesIO()
        with ZipFile(output, "w", ZIP_DEFLATED) as archive:
            for artifact in session.scalars(select(Artifact).where(Artifact.project_id == project_id, Artifact.kind == "manuscripts")):
                if artifact.file_path:
                    archive.write(artifact.file_path, arcname=f"{artifact.id}/{Path(artifact.filename).name}")
        output.seek(0)
        return StreamingResponse(output, media_type="application/zip", headers={"Content-Disposition": 'attachment; filename="manuscripts.zip"'})

    @app.post("/api/v1/projects/{project_id}/artifacts/{artifact_type}/", status_code=201)
    def add_artifact(project_id: str, artifact_type: ArtifactType, metadata: dict = Body(...), session: Session = Depends(get_session)):
        get_project(session, project_id)
        stamp = now()
        artifact = Artifact(id=str(uuid4()), project_id=project_id, kind=artifact_type, data=metadata, created_at=stamp, updated_at=stamp)
        session.add(artifact)
        session.commit()
        return artifact_json(artifact)

    @app.get("/api/v1/projects/{project_id}/artifacts/{artifact_type}/")
    def list_artifacts(project_id: str, artifact_type: ArtifactType, session: Session = Depends(get_session)):
        get_project(session, project_id)
        return [artifact_json(a) for a in session.scalars(select(Artifact).where(Artifact.project_id == project_id, Artifact.kind == artifact_type).order_by(Artifact.id))]

    @app.get("/api/v1/projects/{project_id}/artifacts/{artifact_type}/{artifact_id}")
    def read_artifact(project_id: str, artifact_type: ArtifactType, artifact_id: str, session: Session = Depends(get_session)):
        return artifact_json(get_artifact(session, project_id, artifact_type, artifact_id))

    @app.put("/api/v1/projects/{project_id}/artifacts/{artifact_type}/{artifact_id}")
    def update_artifact(project_id: str, artifact_type: ArtifactType, artifact_id: str, metadata: dict = Body(...), session: Session = Depends(get_session)):
        artifact = get_artifact(session, project_id, artifact_type, artifact_id)
        artifact.data = metadata
        artifact.updated_at = now()
        session.commit()
        return artifact_json(artifact)

    @app.delete("/api/v1/projects/{project_id}/artifacts/{artifact_type}/{artifact_id}", status_code=204)
    def delete_artifact(project_id: str, artifact_type: ArtifactType, artifact_id: str, session: Session = Depends(get_session)):
        artifact = get_artifact(session, project_id, artifact_type, artifact_id)
        remove_binary(artifact)
        session.delete(artifact)
        session.commit()
        return Response(status_code=204)

    @app.post("/api/v1/projects/{project_id}/artifacts/manuscripts/{artifact_id}/file")
    async def upload(project_id: str, artifact_id: str, file: UploadFile = File(...), session: Session = Depends(get_session)):
        artifact = get_artifact(session, project_id, "manuscripts", artifact_id)
        content = await file.read()
        target = storage / artifact.id
        target.write_bytes(content)
        artifact.file_path = str(target)
        artifact.filename = file.filename or "manuscript.bin"
        artifact.file_hash = sha256(content).hexdigest()
        artifact.file_size = len(content)
        artifact.updated_at = now()
        session.commit()
        return artifact_json(artifact)

    @app.get("/api/v1/projects/{project_id}/artifacts/manuscripts/{artifact_id}/file")
    def download(project_id: str, artifact_id: str, session: Session = Depends(get_session)):
        artifact = get_artifact(session, project_id, "manuscripts", artifact_id)
        if not artifact.file_path or not Path(artifact.file_path).is_file():
            raise HTTPException(404, "File not found")
        return FileResponse(artifact.file_path, filename=Path(artifact.filename).name, media_type="application/octet-stream")

    @app.delete("/api/v1/projects/{project_id}/artifacts/manuscripts/{artifact_id}/file", status_code=204)
    def delete_file(project_id: str, artifact_id: str, session: Session = Depends(get_session)):
        artifact = get_artifact(session, project_id, "manuscripts", artifact_id)
        remove_binary(artifact)
        session.commit()
        return Response(status_code=204)

    return app


app = create_app()
