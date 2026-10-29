
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from pydantic import BaseModel, Field
from typing import Literal

from database import engine

app = FastAPI(title="AI Manufacturing Traceability Assistant")



class InspectionCreate(BaseModel):
    inspection_type: str = Field(
        min_length=3,
        max_length=100
    )
    result: Literal["Passed", "Failed", "Pending"]



@app.get("/")
def home():
    return {
        "message": "Welcome to the Manufacturing Traceability Assistant!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def get_inspections(connection, pipe_id: str):
    query = text("""
        SELECT inspection_type, result
        FROM inspections
        WHERE pipe_id = :pipe_id
        ORDER BY id
    """)

    result = connection.execute(
        query, {"pipe_id": pipe_id}
    )

    return [dict(row._mapping) for row in result]


@app.get("/pipes")
def get_all_pipes():
    query = text("""
        SELECT pipe_id, material, production_status,
               manufacturing_stage, production_date, quality_status
        FROM pipes
        ORDER BY pipe_id
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        pipes = []

        for row in result:
            pipe = dict(row._mapping)
            pipe["production_date"] = pipe["production_date"].isoformat()
            pipe["inspections"] = get_inspections(
                connection, pipe["pipe_id"]
            )
            pipes.append(pipe)

    return {
        "total_pipes": len(pipes),
        "pipes": pipes
    }


@app.get("/pipes/{pipe_id}")
def get_pipe(pipe_id: str):
    query = text("""
        SELECT pipe_id, material, production_status,
               manufacturing_stage, production_date, quality_status
        FROM pipes
        WHERE pipe_id = :pipe_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query, {"pipe_id": pipe_id.upper()}
        ).mappings().first()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Pipe {pipe_id} was not found"
            )

        pipe = dict(result)
        pipe["production_date"] = pipe["production_date"].isoformat()
        pipe["inspections"] = get_inspections(
            connection, pipe["pipe_id"]
        )

    return pipe



@app.post("/pipes/{pipe_id}/inspections")
def add_inspection(pipe_id: str, inspection: InspectionCreate):
    with engine.begin() as connection:
        # Check whether the pipe exists.
        pipe = connection.execute(
            text("SELECT pipe_id FROM pipes WHERE pipe_id = :pipe_id"),
            {"pipe_id": pipe_id.upper()}
        ).first()

        if pipe is None:
            raise HTTPException(
                status_code=404,
                detail=f"Pipe {pipe_id} was not found"
            )

        # Save the inspection in PostgreSQL.
        result = connection.execute(
            text("""
                INSERT INTO inspections
                    (pipe_id, inspection_type, result)
                VALUES
                    (:pipe_id, :inspection_type, :result)
                RETURNING id, pipe_id, inspection_type, result, inspected_at
            """),
            {
                "pipe_id": pipe_id.upper(),
                "inspection_type": inspection.inspection_type,
                "result": inspection.result
            }
        )

        saved_inspection = dict(result.mappings().one())

    saved_inspection["inspected_at"] = (
        saved_inspection["inspected_at"].isoformat()
    )

    return {
        "message": "Inspection added successfully",
        "inspection": saved_inspection
    }

