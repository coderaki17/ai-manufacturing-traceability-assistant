
from sqlalchemy import text
from database import engine

sample_pipes = [
    {
        "pipe_id": "PIPE-1001",
        "material": "Carbon Steel",
        "production_status": "Completed",
        "manufacturing_stage": "Final Inspection",
        "production_date": "2026-10-20",
        "quality_status": "Passed",
    },
    {
        "pipe_id": "PIPE-1002",
        "material": "Carbon Steel",
        "production_status": "In Progress",
        "manufacturing_stage": "Welding",
        "production_date": "2026-10-21",
        "quality_status": "Pending",
    },
]

insert_sql = text("""
    INSERT INTO pipes (
        pipe_id,
        material,
        production_status,
        manufacturing_stage,
        production_date,
        quality_status
    )
    VALUES (
        :pipe_id,
        :material,
        :production_status,
        :manufacturing_stage,
        :production_date,
        :quality_status
    )
    ON CONFLICT (pipe_id) DO NOTHING
""")

with engine.begin() as connection:
    connection.execute(insert_sql, sample_pipes)

print("Sample pipe records inserted successfully!")
