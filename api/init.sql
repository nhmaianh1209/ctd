-- CTD Training Calendar — PostgreSQL schema
-- Auto-run by Docker on first start

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS courses (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_code     TEXT,
    course_name     TEXT NOT NULL,
    course_short_name TEXT,
    category        TEXT CHECK (category IN ('technical','mandatory','language','soft-skills')),
    formats         TEXT[],          -- ['Online','Trực tiếp HCM']
    dates           DATE[],          -- ['2026-07-15','2026-07-16']
    months          TEXT[],          -- ['2026-07'] — denormalized for fast month queries
    duration_hours  FLOAT,
    audience_type   TEXT CHECK (audience_type IN ('internal','external')),
    audience_detail TEXT,
    instructor_type TEXT CHECK (instructor_type IN ('internal','external')),
    instructor_detail TEXT,
    pic             TEXT,            -- person-in-charge
    registration_type TEXT CHECK (registration_type IN ('link','email','assigned','other')),
    registration_link TEXT,
    registration_other TEXT,
    requirements    TEXT,
    visibility      TEXT DEFAULT 'public' CHECK (visibility IN ('public','private')),
    created_by      TEXT,
    updated_by      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_courses_months ON courses USING GIN (months);
CREATE INDEX IF NOT EXISTS idx_courses_visibility ON courses (visibility);
