# Recent Checks Endpoint Implementation

## Endpoint Added

**URL:** `GET /api/checks/recent`

**Query Parameters:**
- `limit` (optional): Number of checks to return (default: 20, min: 1, max: 100)

## Response Format

The endpoint now returns an array of check objects with the following structure:

```json
[
  {
    "id": 123,
    "monitor_id": 1,
    "monitor_name": "Production API",
    "target": "https://api.example.com",
    "check_type": "http",
    "status": "passed",
    "success": true,
    "status_code": 200,
    "response_time_ms": 142,
    "region": "us-east-1",
    "created_at": "2025-01-15T10:30:00Z",
    "details": {
      "status_code": 200,
      "headers": {...}
    }
  }
]
```

## Key Features

1. **Includes Monitor Information:**
   - `monitor_name`: Name of the monitored service
   - `target`: URL or endpoint being monitored

2. **Success Flag:**
   - `success`: Boolean indicating if check passed (derived from status)

3. **Response Time:**
   - `response_time_ms`: Response time in milliseconds

4. **Status Information:**
   - `status`: Check status ("passed", "failed", "degraded")
   - `status_code`: HTTP status code (if applicable)

5. **Timestamp:**
   - `created_at`: ISO 8601 formatted timestamp

## Frontend Integration

The endpoint is already integrated in the frontend Dashboard:

**File:** `/monitor_front/src/routes/Dashboard.svelte`

**Usage:**
```typescript
const checksData = await checksApi.getRecent(5);
recentChecks = Array.isArray(checksData) ? checksData : [];
```

**Display:**
- Shows last 5 recent checks on the Dashboard
- Displays check status with icons (✓ for success, ✗ for failure)
- Shows response time
- Clickable to navigate to monitor details

## Backend Changes

**File:** `/webhealth-backend/src/app/api/routers/checks.py`

**Changes:**
1. Modified `/recent` endpoint to join with Monitor table
2. Returns enriched data including monitor name and target
3. Calculates `success` boolean from check status
4. Extracts `status_code` from details JSON
5. Formats timestamp as ISO 8601 string

## Testing

### Test the endpoint:

```bash
# Get recent checks (default limit)
curl http://localhost:8000/api/checks/recent

# Get last 5 checks
curl http://localhost:8000/api/checks/recent?limit=5

# With authentication
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/checks/recent?limit=10
```

### Expected Behavior:

1. **No checks in database:**
   - Returns empty array `[]`
   - Dashboard shows "No recent checks" message

2. **With check data:**
   - Returns array of check objects
   - Dashboard displays checks with icons and response times
   - Clicking a check navigates to monitor detail page

## Status

✅ Endpoint implemented
✅ Frontend integrated
✅ Auto-reloading (FastAPI uvicorn --reload)
✅ Dashboard displays recent checks
✅ Graceful empty state handling

## Next Steps

If you want to populate the checks table with data, you can:

1. **Add checks to seed script:**
   Edit `/webhealth-backend/scripts/seed_data.py` to create sample CheckLog entries

2. **Trigger checks manually:**
   - Create monitors via the UI or API
   - The monitoring system should automatically create check logs

3. **Wait for scheduled checks:**
   - If you have a background worker running
   - It will automatically populate check logs

## Example Seed Data (Optional)

Add this to your seed script to create sample checks:

```python
from app.models.check import CheckLog, CheckStatus, CheckType
from datetime import datetime, timedelta

# Create sample checks for the first monitor
for i in range(10):
    check = CheckLog(
        monitor_id=monitor1.id,
        check_type=CheckType.HTTP,
        status=CheckStatus.PASSED if i % 3 != 0 else CheckStatus.FAILED,
        response_ms=100 + (i * 10),
        details={"status_code": 200 if i % 3 != 0 else 500},
        created_at=datetime.utcnow() - timedelta(minutes=i * 5)
    )
    session.add(check)
```
