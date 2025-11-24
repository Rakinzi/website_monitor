# Settings API Integration Summary

## Backend Endpoints

### Settings Endpoints (`/api/settings`)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/settings/` | Get current settings | - | `SettingsOut` |
| PUT | `/api/settings/` | Update settings | `SettingsUpdate` | `SettingsOut` |
| POST | `/api/settings/webhook/test` | Test webhook delivery | `{ url?: string }` | `{ detail: string }` |

### Escalation Rules Endpoints (`/api/settings/escalations`)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/settings/escalations` | List all escalation policies | - | `EscalationPolicyOut[]` |
| POST | `/api/settings/escalations` | Create escalation policy | `EscalationPolicyCreate` | `EscalationPolicyOut` |
| PUT | `/api/settings/escalations/{id}` | Update escalation policy | `EscalationPolicyUpdate` | `EscalationPolicyOut` |
| DELETE | `/api/settings/escalations/{id}` | Delete escalation policy | - | 204 No Content |

## Data Models

### SettingsOut/SettingsUpdate

```typescript
{
  emailNotifications: boolean;      // Enable email alerts
  slackNotifications: boolean;      // Enable Slack alerts
  pushNotifications: boolean;       // Enable browser push notifications
  webhookUrl: string | null;        // Webhook URL for incident notifications
  emailAddress: string | null;      // Email address for notifications
  checkInterval: number;            // Check interval in seconds (10-3600)
  retryAttempts: number;            // Number of retries (1-10)
  timeout: number;                  // Timeout in seconds (5-120)
  sslVerification: boolean;         // Verify SSL certificates
  followRedirects: boolean;         // Follow HTTP redirects
  updatedAt: string;                // ISO 8601 timestamp (response only)
}
```

### EscalationPolicyOut/Create

```typescript
{
  id: number;                       // Policy ID (response only)
  name: string;                     // Policy name (1-128 chars)
  rules: {                          // Flexible rules object
    severity?: string;              // Severity level (info/warning/critical)
    description?: string;           // Rule description
    [key: string]: any;             // Additional custom fields
  } | null;
}
```

## Frontend Integration

### API Service (`src/lib/services/api.ts`)

The frontend API service includes the following methods:

```typescript
// Settings
settingsApi.get()                           // Get settings
settingsApi.update(data)                    // Update settings
settingsApi.testWebhook(url?)              // Test webhook

// Escalation Rules
settingsApi.getEscalationRules()           // List rules
settingsApi.createEscalationRule(data)     // Create rule
settingsApi.updateEscalationRule(id, data) // Update rule
settingsApi.deleteEscalationRule(id)       // Delete rule
```

### Settings Page (`src/routes/Settings.svelte`)

**Features:**
- ✅ Load settings from backend on mount
- ✅ Save settings with validation
- ✅ Test webhook functionality
- ✅ Reset to server defaults
- ✅ Loading and error states
- ✅ Success messages with auto-dismiss
- ✅ Escalation rules CRUD operations
- ✅ Empty states for no rules

**State Management:**
- Uses Svelte 5 `$state` runes for reactive state
- All form fields bound to state variables
- Proper error handling with user feedback

**UI Components:**
1. **Notifications Card**
   - Email, Slack, Push notification toggles
   - Email address input field

2. **Webhooks Card**
   - Webhook URL input
   - Test webhook button

3. **Check Settings Card**
   - Check interval (10-3600 seconds)
   - Retry attempts (1-10)
   - Timeout (5-120 seconds)

4. **Advanced Settings Card**
   - SSL verification toggle
   - Follow redirects toggle

5. **Escalation Rules Section**
   - List of escalation policies
   - Add/Edit/Delete functionality
   - Empty state message

## Backend Implementation Details

### Database Model (`AppSettings`)

**Table:** `app_settings`

**Columns:**
- `id` (Integer, Primary Key, default=1) - Singleton row
- `email_notifications` (Boolean)
- `slack_notifications` (Boolean)
- `push_notifications` (Boolean)
- `webhook_url` (String, max 2048)
- `email_address` (String, max 255)
- `check_interval` (Integer, default=60)
- `retry_attempts` (Integer, default=3)
- `timeout_seconds` (Integer, default=30)
- `ssl_verification` (Boolean, default=True)
- `follow_redirects` (Boolean, default=True)
- `updated_at` (DateTime, auto-updated)

**Note:** Settings use a singleton pattern (id=1 always)

### Escalation Policy Model

**Table:** `escalation_policies`

**Columns:**
- `id` (Integer, Primary Key)
- `name` (String, 1-128 chars)
- `rules` (JSON/JSONB) - Flexible rules storage

## API Response Examples

### Get Settings Response

```json
{
  "emailNotifications": false,
  "slackNotifications": false,
  "pushNotifications": false,
  "webhookUrl": null,
  "emailAddress": null,
  "checkInterval": 60,
  "retryAttempts": 3,
  "timeout": 30,
  "sslVerification": true,
  "followRedirects": true,
  "updatedAt": "2025-01-23T10:30:00Z"
}
```

### List Escalation Rules Response

```json
[
  {
    "id": 1,
    "name": "Critical Incidents → #ops-team",
    "rules": {
      "severity": "critical",
      "description": "Immediate notification for all critical incidents"
    }
  },
  {
    "id": 2,
    "name": "Warning Alerts → #monitoring",
    "rules": {
      "severity": "warning",
      "description": "Send warnings to monitoring channel"
    }
  }
]
```

## Usage Notes

### Webhook Testing

The webhook test endpoint (`/api/settings/webhook/test`) sends a test payload:

```json
{
  "event": "webhealth_test",
  "status": "ok"
}
```

If no URL is provided in the request, it uses the `webhook_url` from settings.

### Error Handling

All endpoints return standard HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Deletion success
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Pydantic validation error

### Field Mapping

Backend uses `snake_case` in database, but `camelCase` in API responses:
- `email_notifications` ↔ `emailNotifications`
- `check_interval` ↔ `checkInterval`
- `retry_attempts` ↔ `retryAttempts`
- `timeout_seconds` ↔ `timeout`
- `ssl_verification` ↔ `sslVerification`
- `follow_redirects` ↔ `followRedirects`
- `webhook_url` ↔ `webhookUrl`
- `email_address` ↔ `emailAddress`

This mapping is handled automatically by the Pydantic schemas.

## Testing the Integration

### 1. Test Settings Endpoints

```bash
# Get settings
curl http://localhost:8000/api/settings/

# Update settings
curl -X PUT http://localhost:8000/api/settings/ \
  -H "Content-Type: application/json" \
  -d '{
    "emailNotifications": true,
    "emailAddress": "admin@example.com",
    "checkInterval": 120
  }'

# Test webhook
curl -X POST http://localhost:8000/api/settings/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"url": "https://webhook.site/your-unique-id"}'
```

### 2. Test Escalation Rules

```bash
# List rules
curl http://localhost:8000/api/settings/escalations

# Create rule
curl -X POST http://localhost:8000/api/settings/escalations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Critical Alerts",
    "rules": {
      "severity": "critical",
      "description": "High priority incidents"
    }
  }'

# Update rule
curl -X PUT http://localhost:8000/api/settings/escalations/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Rule Name"
  }'

# Delete rule
curl -X DELETE http://localhost:8000/api/settings/escalations/1
```

## Next Steps

1. **Add validation feedback** - Show field-specific errors from backend validation
2. **Add edit functionality** for escalation rules (currently only add/delete)
3. **Improve UI for escalation rules** - Use a modal instead of prompts
4. **Add webhook URL validation** - Real-time validation before test
5. **Add more escalation rule fields** - Channels, schedules, conditions
6. **Implement notification testing** - Test email/Slack notifications
7. **Add settings history** - Track changes to settings over time
