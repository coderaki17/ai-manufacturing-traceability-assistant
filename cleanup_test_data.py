
from sqlalchemy import text
from database import engine

query = text("""
    DELETE FROM inspections
    WHERE inspection_type = 'string'
      AND result = 'string'
""")

with engine.begin() as connection:
    result = connection.execute(query)

print(f"Removed {result.rowcount} placeholder inspection(s).")
