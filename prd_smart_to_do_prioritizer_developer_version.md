# Product Requirements Document (PRD)
## Smart To-Do Prioritizer & Task Breakdown (MVP)

---

## 1. Product Overview

**Working name:** StartNow – Smart To-Do Prioritizer  
**Product type:** One-page AI-powered web application  
**Goal:** Convert unstructured to-do lists into prioritized tasks with clear, executable next steps within seconds.

**Primary success metric:** User receives a clear "what to do next" action in under 10 seconds.

---

## 2. Problem Statement

Users struggle with:
- Deciding task priority
- Breaking large tasks into actionable steps
- Knowing where to start

Existing tools focus on task storage, not execution guidance.

---

## 3. Target Users (for logic assumptions)

- Knowledge workers
- Students
- Freelancers
- Founders

**User state:** Overwhelmed, time-constrained, wants instant clarity, minimal UI.

---

## 4. In-Scope Features (MVP)

### 4.1 One-Page UI
- Single landing page
- No authentication
- No dashboards

### 4.2 Task Input
- Free-text textarea
- Accepts:
  - Bullet lists
  - Comma-separated tasks
  - Natural language

### 4.3 AI Task Prioritization
Each task must be categorized as:
- **Must Do** (urgent & high impact)
- **Should Do** (important but not urgent)
- **Optional** (low urgency/impact)

### 4.4 Task Breakdown Engine
For each prioritized task:
- Break into micro-steps
- Each step duration: **2–20 minutes**
- Steps must be concrete actions (verbs only)
- First step must be extremely easy

### 4.5 Time Estimation
- Estimated duration per step
- Estimated total task time

### 4.6 Immediate Action Output
- A dedicated section:
  **"What should I do in the next 10 minutes?"**
- Must always return exactly one suggested action

---

## 5. Out of Scope (Explicitly Excluded)

- User accounts / login
- Task saving or history
- Team collaboration
- Notifications
- Calendar integrations
- Mobile app

---

## 6. User Flow

1. User lands on page
2. Sees headline + task input
3. Pastes tasks
4. Clicks CTA: **Get Clarity**
5. Backend processes tasks
6. UI renders:
   - Prioritized task list
   - Task breakdowns
   - Immediate next action

---

## 7. Functional Requirements

### 7.1 Input Handling
- Max input size: 2,000 characters
- Must sanitize input
- Must split tasks reliably

### 7.2 AI Processing Pipeline

**Step 1: Task Parsing**
- Convert input into discrete task list

**Step 2: Prioritization Logic**
- Criteria:
  - Urgency
  - Impact
  - Dependencies
  - Estimated effort

**Step 3: Task Decomposition**
- Generate micro-steps
- Enforce step constraints programmatically

**Step 4: Next Action Selection**
- Choose smallest viable step from highest priority task

---

## 8. Non-Functional Requirements

### Performance
- Response time < 5 seconds

### Reliability
- Graceful failure with user-friendly error message

### Security
- No data persistence
- No PII storage

### Scalability
- Stateless backend
- Ready for horizontal scaling

---

## 9. Tech Stack (Suggested, not mandatory)

### Frontend
- React / Next.js
- Minimal UI (Tailwind or equivalent)

### Backend
- Python (FastAPI preferred)
- Single API endpoint: `/analyze`

### AI
- LLM via API (OpenAI-compatible)
- Prompt-engineered deterministic output

---

## 10. API Contract (Initial)

### POST /analyze

**Request:**
```json
{
  "tasks": "string"
}
```

**Response:**
```json
{
  "priorities": {
    "must": [],
    "should": [],
    "optional": []
  },
  "breakdown": {
    "task": [
      { "step": "string", "minutes": number }
    ]
  },
  "next_action": {
    "step": "string",
    "minutes": number
  }
}
```

---

## 11. Edge Cases

- Empty input → show guidance message
- Single vague task → request clarification via AI
- Too many tasks → prioritize top 5 only

---

## 12. Acceptance Criteria

- User receives prioritized tasks
- Every task has actionable steps
- Next action is always shown
- No login required
- Page works on desktop & mobile

---

## 13. Future Enhancements (Not MVP)

- User profiles
- ADHD-friendly modes
- Daily task email
- Task history
- Calendar sync

---

## 14. Definition of Done (MVP)

- One-page app deployed
- AI responses consistent and structured
- Average user understands next step instantly
- No onboarding required

---

**Product philosophy:**
> This is not a planning tool. It is an execution trigger.

