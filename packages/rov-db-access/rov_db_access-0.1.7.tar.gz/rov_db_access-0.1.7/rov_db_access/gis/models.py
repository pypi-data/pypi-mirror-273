from geoalchemy2 import Geometry
from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy import JSON

from rov_db_access.authentication.models import Organization, User, Base


class Image(Base):
    __tablename__ = "image"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    url: Mapped[str]
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)

    user_id: Mapped[int] = mapped_column(ForeignKey("admin.user.id"))
    user: Mapped["User"] = relationship()

    organization_id: Mapped[int] = mapped_column(ForeignKey("admin.organization.id"))
    organization: Mapped["Organization"] = relationship()

    bbox: Mapped[Geometry] = mapped_column(Geometry("POLYGON", srid=4326))
    footprint: Mapped[Optional[Geometry]] = mapped_column(Geometry("POLYGON", srid=4326))

    def __repr__(self) -> str:
        return f"Image (id={self.id!r}, name={self.name!r}, url={self.url!r}, user_id={self.user_id!r}, organization_id={self.organization_id!r})"


class Input(Base):
    __tablename__ = "input"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(server_default='upload')
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)

    user_id: Mapped[int] = mapped_column(ForeignKey("admin.user.id"))
    user: Mapped["User"] = relationship()

    organization_id: Mapped[int] = mapped_column(ForeignKey("admin.organization.id"))
    organization: Mapped["Organization"] = relationship()

    def __repr__(self) -> str:
        return f"Input (id={self.id!r}, user_id={self.user_id!r}, organization_id={self.organization_id!r})"


class InferenceModel(Base):
    __tablename__ = "inference_model"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    img_url: Mapped[str]
    price: Mapped[int] = mapped_column(server_default='0')
    min_resolution: Mapped[float]
    config: Mapped[Optional[JSON]] = mapped_column(type_=JSON)

    def __repr__(self) -> str:
        return f"InferenceModel (id={self.id!r}, name={self.name!r}, price={self.price!r}, config={self.config!r})"


class Process(Base):
    __tablename__ = "process"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    status: Mapped[str] = mapped_column(server_default="queued")
    type: Mapped[str] = mapped_column(server_default="on demand")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    time: Mapped[float] = mapped_column(server_default="0")
    area: Mapped[float] = mapped_column(server_default="0")
    cost_estimated: Mapped[float] = mapped_column(server_default="0")

    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)

    geom: Mapped[Optional[Geometry]] = mapped_column(Geometry("POLYGON", srid=4326))
    mask: Mapped[Optional[Geometry]] = mapped_column(Geometry("POLYGON", srid=4326))

    inference_model_id: Mapped[int] = mapped_column(ForeignKey("gis.inference_model.id"))
    inference_model: Mapped["InferenceModel"] = relationship()

    organization_id: Mapped[int] = mapped_column(ForeignKey("admin.organization.id"))
    organization: Mapped["Organization"] = relationship()

    user_id: Mapped[int] = mapped_column(ForeignKey("admin.user.id"))
    user: Mapped["User"] = relationship()

    runs: Mapped[List["Run"]] = relationship(
       back_populates="process",
       order_by="Run.id"
    )

    def __repr__(self) -> str:
        return f"Process(id={self.id!r}, name={self.name!r}, status={self.status!r}, inference_model_id={self.inference_model_id!r}), user_id={self.user_id!r})"


class ResultsRaster(Base):
    __tablename__ = "results_raster"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)
    bbox: Mapped[Optional[Geometry]] = mapped_column(Geometry("POLYGON", srid=4326))

    run_id: Mapped[int] = mapped_column(ForeignKey("gis.run.id"))
    run: Mapped["Run"] = relationship(back_populates="results_raster")

    def __repr__(self) -> str:
        return f"ResultsRaster(id={self.id!r}, url={self.url!r}, run_id={self.run_id!r})"


class ResultsRaw(Base):
    __tablename__ = "results_raw"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)
    geom: Mapped[Geometry] = mapped_column(Geometry("MULTIPOLYGON", srid=4326))

    run_id: Mapped[int] = mapped_column(ForeignKey("gis.run.id"))
    run: Mapped["Run"] = relationship(back_populates="results_raw")

    def __repr__(self) -> str:
        return f"ResultsRaw(id={self.id!r}, data={self.data!r}, geom={self.geom!r}, run_id={self.run_id!r})"


class Run(Base):
    __tablename__ = "run"
    __table_args__ = {"schema": "gis"}
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(server_default="queued")
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    engine: Mapped[str] = mapped_column(server_default="local")
    runtime: Mapped[float] = mapped_column(server_default="0")
    cost: Mapped[float] = mapped_column(server_default="0")
    filepath: Mapped[Optional[str]]

    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)

    input_id: Mapped[Optional[int]] = mapped_column(ForeignKey("gis.input.id"), nullable=True)
    input: Mapped[Optional["Input"]] = relationship()

    inference_model_id: Mapped[int] = mapped_column(ForeignKey("gis.inference_model.id"))
    inference_model: Mapped["InferenceModel"] = relationship()

    process_id: Mapped[int] = mapped_column(ForeignKey("gis.process.id"))
    process: Mapped["Process"] = relationship()

    results_raw: Mapped[List["ResultsRaw"]] = relationship(
       back_populates="run",
       order_by="ResultsRaw.id"
    )

    results_raster: Mapped[List["ResultsRaster"]] = relationship(
        back_populates="run",
        order_by="ResultsRaster.id"
    )

    def __repr__(self) -> str:
        return f"Run(id={self.id!r}, status={self.status!r}, process_id={self.process_id!r}) inference_model_id={self.inference_model_id!r})"
