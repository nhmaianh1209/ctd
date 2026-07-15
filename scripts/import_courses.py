"""
Import courses.json → PostgreSQL (after Docker stack is running).

Usage:
  pip install psycopg2-binary
  python import_courses.py courses.json
"""
import json, sys, os, uuid
import psycopg2

DB_URL = os.getenv("DATABASE_URL", "postgresql://ctd:ctd@localhost:5432/ctd")
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

with open(sys.argv[1] if len(sys.argv) > 1 else "courses.json", encoding="utf-8") as f:
    courses = json.load(f)

inserted = 0
for c in courses:
    cur.execute("""
        INSERT INTO courses (
            id, course_code, course_name, course_short_name,
            category, formats, dates, months, duration_hours,
            audience_type, audience_detail, instructor_type, instructor_detail,
            pic, registration_type, registration_link, registration_other,
            requirements, visibility, created_by, updated_by, created_at, updated_at
        ) VALUES (
            %s,%s,%s,%s, %s,%s,%s,%s,%s,
            %s,%s,%s,%s, %s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s
        ) ON CONFLICT (id) DO NOTHING
    """, (
        c.get("id") or str(uuid.uuid4()),
        c.get("course_code"), c.get("course_name",""), c.get("course_short_name"),
        c.get("category"), c.get("formats"), c.get("dates"), c.get("months"),
        c.get("duration_hours"),
        c.get("audience_type","internal"), c.get("audience_detail"),
        c.get("instructor_type","internal"), c.get("instructor_detail"),
        c.get("pic"),
        c.get("registration_type"), c.get("registration_link"), c.get("registration_other"),
        c.get("requirements"), c.get("visibility","public"),
        c.get("created_by"), c.get("updated_by"),
        c.get("created_at"), c.get("updated_at"),
    ))
    inserted += 1

conn.commit()
cur.close()
conn.close()
print(f"Imported {inserted} courses → PostgreSQL")
