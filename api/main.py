import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Course
from auth import verify_token, authenticate, create_token

app = FastAPI(title="CTD API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # ponytail: restrict to your domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class CourseIn(BaseModel):
    course_code:        Optional[str] = None
    course_name:        str
    course_short_name:  Optional[str] = None
    category:           Optional[str] = None
    formats:            Optional[List[str]] = []
    dates:              Optional[List[str]] = []
    months:             Optional[List[str]] = []
    duration_hours:     Optional[float] = None
    audience_type:      Optional[str] = "internal"
    audience_detail:    Optional[str] = None
    instructor_type:    Optional[str] = "internal"
    instructor_detail:  Optional[str] = None
    pic:                Optional[str] = None
    registration_type:  Optional[str] = None
    registration_link:  Optional[str] = None
    registration_other: Optional[str] = None
    requirements:       Optional[str] = None
    visibility:         Optional[str] = "public"

class CourseOut(CourseIn):
    id:         str
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True


def row_to_dict(c: Course) -> dict:
    return {
        "id":                 str(c.id),
        "course_code":        c.course_code,
        "course_name":        c.course_name,
        "course_short_name":  c.course_short_name,
        "category":           c.category,
        "formats":            c.formats or [],
        "dates":              c.dates or [],
        "months":             c.months or [],
        "duration_hours":     c.duration_hours,
        "audience_type":      c.audience_type,
        "audience_detail":    c.audience_detail,
        "instructor_type":    c.instructor_type,
        "instructor_detail":  c.instructor_detail,
        "pic":                c.pic,
        "registration_type":  c.registration_type,
        "registration_link":  c.registration_link,
        "registration_other": c.registration_other,
        "requirements":       c.requirements,
        "visibility":         c.visibility,
        "created_by":         c.created_by,
        "updated_by":         c.updated_by,
        "created_at":         c.created_at.isoformat() if c.created_at else None,
        "updated_at":         c.updated_at.isoformat() if c.updated_at else None,
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"status": "ok"}


class LoginIn(BaseModel):
    username: str
    password: str

@app.post("/api/auth/login")
def login(body: LoginIn):
    user = authenticate(body.username, body.password)
    return {"token": create_token(user), "email": user["email"], "name": user["name"]}

@app.get("/api/auth/me")
def me(user: dict = Depends(verify_token)):
    return user


@app.get("/api/courses")
def list_courses(
    month:      Optional[str] = None,
    visibility: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Public endpoint — no auth required. Used by calendar/index.html."""
    q = db.query(Course)
    if month:
        q = q.filter(Course.months.any(month))
    if visibility:
        q = q.filter(Course.visibility == visibility)
    return [row_to_dict(c) for c in q.all()]


@app.post("/api/courses")
def create_course(
    body: CourseIn,
    db:   Session = Depends(get_db),
    user: dict    = Depends(verify_token),
):
    course = Course(**body.model_dump(), created_by=user["email"], updated_by=user["email"])
    db.add(course)
    db.commit()
    db.refresh(course)
    return row_to_dict(course)


@app.put("/api/courses/{course_id}")
def update_course(
    course_id: str,
    body:      CourseIn,
    db:        Session = Depends(get_db),
    user:      dict    = Depends(verify_token),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(course, k, v)
    course.updated_by = user["email"]
    course.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(course)
    return row_to_dict(course)


@app.delete("/api/courses/{course_id}", status_code=204)
def delete_course(
    course_id: str,
    db:        Session = Depends(get_db),
    user:      dict    = Depends(verify_token),
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(course)
    db.commit()
