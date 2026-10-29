
from sqlalchemy import text
from database import engine

sample_inspections = [
    {
        "pipe_id": "PIPE-1001",
        "inspection_type": "Visual Inspection",
        "result": "Passed",
    },
    {
        "pipe_id": "PIPE-1001",
        "inspection_type": "Dimensional Inspection",
        "result": "Passed",
    },
]

insert_sql = text("""
    INSERT INTO inspections (pipe_id, inspection_type, result)
    SELECT
        CAST(:pipe_id AS VARCHAR(50)),
        CAST(:inspection_type AS VARCHAR(100)),
        CAST(:result AS VARCHAR(50))
    WHERE NOT EXISTS (
        SELECT 1
        FROM inspections
        WHERE pipe_id = CAST(:pipe_id AS VARCHAR(50))
          AND inspection_type = CAST(:inspection_type AS VARCHAR(100))
    )
""")

with engine.begin() as connection:
    connection.execute(insert_sql, sample_inspections)

print("Sample inspections inserted successfully!")
