# WebHealth Frontend

A modern website monitoring dashboard built with Svelte 5, Vite, and Skeleton UI.

## Features

- Real-time monitoring dashboard
- Monitor management (HTTP, SSL, Regional Probes, Synthetic Journeys)
- Incident tracking and management
- Analytics and uptime reports
- User authentication with JWT
- Responsive design with dark mode support
- Tailwind CSS + Skeleton UI components

## Tech Stack

- **Svelte 5** - Modern reactive framework with runes
- **Vite** - Lightning-fast build tool
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Utility-first CSS framework
- **Skeleton UI** - Svelte component library
- **svelte-spa-router** - Client-side routing

## Getting Started

### Prerequisites

- Node.js 18+ or Bun
- Backend API running (default: http://localhost:8000)

### Installation

```bash
# Install dependencies
bun install
# or
npm install
```

### Development

```bash
# Start development server
bun run dev
# or
npm run dev
```

The app will be available at http://localhost:5173 (or next available port).

### Build for Production

```bash
# Build
bun run build
# or
npm run build

# Preview build
bun run preview
# or
npm run preview
```

## Configuration

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── routes/              # Page components
│   ├── Dashboard.svelte
│   ├── Monitors.svelte
│   ├── MonitorDetail.svelte
│   ├── Incidents.svelte
│   ├── Settings.svelte
│   └── Login.svelte
├── lib/
│   ├── layouts/         # Layout components
│   │   └── DashboardLayout.svelte
│   ├── components/      # Reusable components
│   └── services/        # API service layer
│       └── api.ts
├── stores/              # Svelte stores
│   └── authStore.ts     # Authentication state
├── App.svelte           # Root component with routing
└── main.ts              # Entry point
```

## Authentication

The app uses JWT-based authentication:

- Navigate to `/login`
- Enter your credentials
- JWT token is stored in localStorage
- Protected routes redirect to login if not authenticated

**Note:** Currently using mock authentication. Connect to the FastAPI backend for production use.

## Routes

- `/` - Dashboard overview
- `/monitors` - Monitor list
- `/monitors/:id` - Monitor detail
- `/incidents` - Incident list
- `/incidents/:id` - Incident detail (TBD)
- `/settings` - Application settings
- `/login` - Authentication

## API Integration

The app communicates with a FastAPI backend. API endpoints are defined in `src/lib/services/api.ts`.

Current mock data will be replaced with real API calls once the backend is implemented.

## Type Checking

```bash
bun run check
# or
npm run check
```

## Themes

The app uses Skeleton UI's Cerberus theme by default. To change themes:

1. Update `src/app.css` to import a different theme
2. Update `index.html` to set the `data-theme` attribute

Available themes: cerberus, wintry, vintage, crimson, gold-nouveau, hamlindigo, rocket, sahara, seafoam, skeleton, modern

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Your License Here]
