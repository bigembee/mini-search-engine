# Mini Search Engine

## Project Summary
**Category:** Data, Security & Algorithms  
**Difficulty:** Intermediate  
**Suggested team split:** Text processing, inverted index, ranking, search UI 

## Description
This project is a good fit for a small team that wants to build something real and usable in a short amount of time. It focuses on one clear feature, clean data flow, and a simple user experience that can be demoed without extra fluff. The goal is to turn a good idea into a working MVP with a solid backend, a basic interface, and a realistic set of edge cases.

## Scope
Index a supplied document collection and rank results using keyword frequency and relevance.

## Core Features
- Deliver the main user flow from start to finish.
- Support the required data model and user interactions.
- Handle validation, edge cases, and error states cleanly.
- Include basic monitoring, feedback, or reporting where relevant.
- Make the app easy to explain during a live demo.

## Deliverables
- A working deployed application or API demo
- A clear README with setup instructions and environment variables
- A minimal database schema or data model definition
- UI screens or API endpoints for the core MVP
- A basic test strategy covering the happy path and one major failure path
- A short demo script explaining the architecture, choices, and trade-offs

## Suggested Architecture
- Frontend: simple dashboard, form-based interface, or lightweight visual layer
- Backend: API or service layer for business logic and validation
- Data layer: database, in-memory persistence, or structured file storage for MVP use
- Optional extras: auth, async jobs, scheduling, WebSockets, caching, or notifications depending on the project

## Learning Outcomes
Information retrieval, indexing, ranking

## Recommended MVP Checklist
1. Define the main user flow and success criteria.
2. Build the data model and core backend logic.
3. Connect the UI or client to the main application flow.
4. Add key validation, security checks, and realistic error states.
5. Test the happy path and at least one important edge case.
6. Deploy the app and document the setup clearly.

## Free Deployment Options
Cloudflare Pages, Vercel, or GitHub Pages for demos; Render or Railway for APIs; Supabase or Postgres for persistence.

## Good Free Hosting Choices
- Static frontend: Vercel, Netlify, or GitHub Pages
- API/backend: Render, Railway, or Fly.io
- Database/realtime services: Supabase, Neon, Firebase, or Cloudflare D1
- Documentation/demo pages: GitHub Pages, Cloudflare Pages, or Vercel

## Typical Tech Stack
- Frontend: React, Next.js, plain HTML/JS, or similar lightweight UI tooling
- Backend: Node.js, Python (Flask/FastAPI), or Java/Spring Boot
- Database: Postgres, SQLite, Supabase, or a simple file-based store
- Real-time layer: WebSockets, polling, or background workers if needed

## Final Demo Expectations
- Provide a working URL with sample or seeded data
- Show one clear end-to-end flow from start to finish
- Explain the most important technical decisions and trade-offs
- Include screenshots, screen recordings, or a brief live walk-through
- Highlight what was completed in the MVP and what would be next if the project continued

## Next Improvements
- Add authorization, auditing, or stronger validation
- Improve test coverage and resilience
- Add analytics, metrics, or observability
- Expand functionality once the core MVP is stable

## Intern Profile Database

The database layer stores the spreadsheet as a normalized profile directory:

- `InternProfile` stores identity, role, schedule, contact, employment, and status data.
- `Location` prevents duplicate city/state/country records.
- `Skill` is a canonical skill vocabulary shared by many profiles.
- `InternSkill` is the profile-to-skill join table and can optionally store proficiency from 1–5.
- `search_keywords` is a generated search document containing each profile's name, role, work mode, location, and skills.

Import or refresh the supplied workbook with:

```bash
python manage.py migrate
python manage.py import_intern_profiles /path/to/intern_profiles_database.xlsx
```

The importer is idempotent: running it again updates the same `Intern ID` records instead of creating duplicates. Existing employment types and schedules are preserved, so custom full-time, part-time, contract, and intern assignments are not overwritten by the workbook's placeholder values. Blank email and phone cells remain blank, as intended by the source workbook. The import command supports the workbook directly and includes a standard-library fallback when `openpyxl` is not installed.
