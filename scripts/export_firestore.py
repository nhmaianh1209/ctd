"""
Export all courses from Firestore → courses.json
Run once before migrating to PostgreSQL.

Usage:
  pip install firebase-admin
  export GOOGLE_APPLICATION_CREDENTIALS=serviceAccountKey.json
  python export_firestore.py
"""
import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = db.collection("courses").stream()
courses = []
for doc in docs:
    d = doc.to_dict()
    d["id"] = doc.id
    # Convert Firestore Timestamps to ISO strings
    for k in ("created_at", "updated_at"):
        if hasattr(d.get(k), "isoformat"):
            d[k] = d[k].isoformat()
        elif d.get(k) is None:
            d[k] = None
    courses.append(d)

with open("courses.json", "w", encoding="utf-8") as f:
    json.dump(courses, f, ensure_ascii=False, indent=2)

print(f"Exported {len(courses)} courses → courses.json")
