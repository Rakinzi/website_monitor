# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WebHealth** is a full-featured website monitoring and incident management system.

**Current Status:** Early development phase
- Frontend: Basic Svelte + Vite + TypeScript scaffold exists in `monitor_front/`
- Backend: Not yet implemented
- Skeleton UI integration: Planned but not yet added

### Tech Stack
- **Frontend**: Svelte 5 + Vite + TypeScript (Skeleton UI to be integrated)
- **Backend**: FastAPI (async Python) - to be implemented
- **Database**: MySQL or PostgreSQL - to be implemented
- **Scheduling**: Linux/CPanel Cron jobs
- **Authentication**: JWT (access + refresh tokens)

## Repository Structure

```
website_monitor/
├── monitor_front/          # Svelte frontend (basic scaffold exists)
│   ├── src/
│   │   ├── App.svelte     # Root component
│   │   ├── main.ts        # Entry point
│   │   └── lib/           # Reusable components
│   └── package.json
├── prompt.json            # Detailed system specification (TOON format)
├── skeleton-ui.md         # Skeleton UI documentation
└── CLAUDE.md             # This file
```

**Note:** Backend directory structure does not exist yet.

### Key Reference Documents

- **prompt.json**: Contains the complete system specification in TOON format (Technical, Operational flow, Organizational structure, Navigation). Read this file for detailed requirements about routes, models, services, features, and UI components.
- **skeleton-ui.md**: Full documentation for the Skeleton UI library (600KB). Reference for component APIs, theming, and design system.

## System Architecture

### Core Monitoring Capabilities
The system will perform multiple types of checks:
1. **HTTP Health Checks** - Status codes, latency, retries
2. **Regional Probes** - Multi-region performance monitoring
3. **Synthetic User Journeys** - Step-by-step user flow tracking
4. **SSL Certificate Monitoring** - Expiry tracking, mismatch detection
5. **Heartbeat Monitoring** - Ping endpoint validation

### Backend Structure (FastAPI)

**API Routes:**
- `/monitors` - Monitor CRUD operations
- `/checks` - Check execution and history
- `/incidents` - Incident management
- `/regions` - Regional probe configuration
- `/analytics` - Metrics and reporting
- `/heartbeats` - Heartbeat endpoint management
- `/webhooks` - Webhook integration
- `/auth` - Authentication endpoints

**Key Services:**
- `http_service.py` - HTTP health check logic
- `ssl_service.py` - SSL certificate validation
- `synthetic_service.py` - Synthetic journey execution
- `region_service.py` - Multi-region probe orchestration
- `incident_service.py` - Incident detection and lifecycle management
- `notification_service.py` - Email/webhook notifications

**Background Workers:**
- `check_runner.py` - Executes scheduled checks
- `incident_evaluator.py` - Evaluates check results and opens/closes incidents
- `cron_worker.py` - Cron job integration layer

**Data Models:**
- Monitor, Check, Incident, EscalationRule, Region, HeartbeatLog, User, NotificationLog

**Security:**
- Role-based access control: admin, manager, viewer
- JWT authentication with access and refresh tokens

### Frontend Structure (Svelte)

**Routes:**
- `/` - Dashboard overview
- `/monitors` - Monitor list
- `/monitors/:id` - Monitor detail page
- `/incidents` - Incident center
- `/incidents/:id` - Incident detail
- `/settings` - General settings
- `/settings/escalations` - Escalation rule management
- `/settings/webhooks` - Webhook configuration
- `/login` - Authentication page

**Key Components:**
- `Header`, `Sidebar` - Navigation
- `MonitorCard`, `ChartCard` - Dashboard widgets
- `LatencyMap` - Regional latency heatmap
- `SSLExpiryWidget` - Certificate expiry countdown
- `IncidentTimeline` - Incident history visualization
- `DataTable` - Tabular data display
- `Modal`, `FormField`, `Badge` - UI primitives

**State Management:**
- Svelte writable stores for reactive state

**Layouts:**
- `DashboardLayout` - Authenticated app layout
- `AuthLayout` - Login/registration pages

### Operational Flow

1. **Check Execution**: Cron jobs trigger FastAPI check runner → Async checks execute → Results stored in database
2. **Incident Lifecycle**:
   - Check failure detected → Incident opened/updated → Notifications sent (with cooldown) → Auto-close on recovery
3. **Frontend Updates**: Svelte SPA polls FastAPI endpoints → Updates stores → Charts and cards re-render
4. **External Integrations**: Heartbeat URLs, webhook delivery, public REST API

### Analytics Features
- Real-time response graphs
- Uptime calculations (daily/weekly/30-day)
- Incident grouping and correlation
- MTTD (Mean Time To Detect) and MTTR (Mean Time To Recover)
- Per-region latency inspection

## Common Commands

### Frontend (monitor_front/)

```bash
# Install dependencies
npm install

# Run development server (http://localhost:5173)
npm run dev

# Type checking
npm run check

# Build for production
npm run build

# Preview production build
npm run preview
```

### Backend (Not Yet Implemented)

When implementing the backend, create a directory structure like:

```bash
mkdir -p backend/{routers,services,models,workers}

# Initialize Python virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy alembic pydantic python-jose[cryptography] passlib[bcrypt]

# Run development server (when implemented)
uvicorn main:app --reload

# Database migrations (when implemented)
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Next Steps for Implementation

### Frontend Tasks
1. **Install Skeleton UI:**
   ```bash
   cd monitor_front
   npm install @skeletonlabs/skeleton @skeletonlabs/tw-plugin
   npm install -D tailwindcss postcss autoprefixer
   ```

2. **Configure Tailwind** with Skeleton UI plugin

3. **Implement core layouts:**
   - DashboardLayout (authenticated pages)
   - AuthLayout (login/register)

4. **Create routing structure** (consider using a router like `svelte-routing` or `tinro`)

### Backend Tasks
1. Set up FastAPI project structure
2. Implement database models with SQLAlchemy
3. Create API routers as defined in architecture
4. Implement authentication (JWT)
5. Build monitoring services (HTTP, SSL, synthetic, heartbeat)
6. Create background workers for check execution

## Svelte 5 Development Notes

The frontend uses **Svelte 5**, which has significant changes from Svelte 4:
- Runes-based reactivity (`$state`, `$derived`, `$effect`)
- Different component API
- Enhanced TypeScript support

**Important:** When working on Svelte code in `monitor_front/`, refer to `monitor_front/CLAUDE.md` for Svelte MCP server tools that provide access to comprehensive Svelte 5 documentation.

## Important Design Decisions

### UI Library Choice
The project uses **Skeleton UI** for Svelte because:
- Svelte-native components (not wrappers)
- Full Vite compatibility
- Built-in dark mode and theming
- Dashboard-friendly components (tables, charts, cards)
- Active ecosystem

### Notification Strategy
- Notifications include cooldown logic to prevent alert spam
- Support for both email and webhook delivery
- Separate NotificationLog model for audit trail

### Multi-Region Architecture
Regional probes enable performance monitoring from different geographic locations, helping identify regional outages or latency issues.

### Incident Management
Incidents are automatically opened when checks fail and closed when monitors recover, with full timeline tracking for root cause analysis.


You are able to use the Svelte MCP server, where you have access to comprehensive Svelte 5 and SvelteKit documentation. Here's how to use the available tools effectively:

## Available MCP Tools:

### 1. list-sections

Use this FIRST to discover all available documentation sections. Returns a structured list with titles, use_cases, and paths.
When asked about Svelte or SvelteKit topics, ALWAYS use this tool at the start of the chat to find relevant sections.

### 2. get-documentation

Retrieves full documentation content for specific sections. Accepts single or multiple sections.
After calling the list-sections tool, you MUST analyze the returned documentation sections (especially the use_cases field) and then use the get-documentation tool to fetch ALL documentation sections that are relevant for the user's task.

### 3. svelte-autofixer

Analyzes Svelte code and returns issues and suggestions.
You MUST use this tool whenever writing Svelte code before sending it to the user. Keep calling it until no issues or suggestions are returned.

### 4. playground-link

Generates a Svelte Playground link with the provided code.
After completing the code, ask the user if they want a playground link. Only call this tool after user confirmation and NEVER if code was written to files in their project.