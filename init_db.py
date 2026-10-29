
from sqlalchemy import text
from database import engine

create_table_sql = """
CREATE TABLE IF NOT EXISTS pipes (
    pipe_id VARCHAR(50) PRIMARY KEY,
    material VARCHAR(100) NOT NULL,
    production_status VARCHAR(50) NOT NULL,
    manufacturing_stage VARCHAR(100) NOT NULL,
    production_date DATE NOT NULL,
    quality_status VARCHAR(50) NOT NULL
);
"""

with engine.begin() as connection:
    connection.execute(text(create_table_sql))

print("Pipes table created successfully!")
