
from sqlalchemy import text
from database import engine

create_table_sql = """
CREATE TABLE IF NOT EXISTS inspections (
    id SERIAL PRIMARY KEY,
    pipe_id VARCHAR(50) NOT NULL
        REFERENCES pipes(pipe_id) ON DELETE CASCADE,
    inspection_type VARCHAR(100) NOT NULL,
    result VARCHAR(50) NOT NULL,
    inspected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with engine.begin() as connection:
    connection.execute(text(create_table_sql))

print("Inspections table created successfully!")
