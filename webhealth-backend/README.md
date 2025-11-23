## Passive Cybersecurity Checks

All monitoring logic must follow the passive-only rules captured in `src/app/core/cybersecurity_checks.py` (also summarized in `CYBERSECURITY_CHECKS.md`). Highlights:

- Only perform HTTP GET/SSL handshake checks; no fuzzing, scanning, or brute force.
- Allowed checks include TLS posture, security headers, passive exposure checks for `.env`, `.git/HEAD`, robots.txt, DNS posture, and WAF detection via headers.
- Hard rate limit of one request per monitor per 60 seconds, randomized User-Agent rotation, Retry-After/backoff handling, and automatic cooldowns to avoid bans.
- A background scheduler (`SecurityAuditScheduler`) periodically runs these checks for every active monitor and stores the findings in `security_audits`, triggering notification webhooks/emails when severity reaches `warning` or `critical`.

Import and reuse the `CYBERSECURITY_CHECKS` constant whenever you need to validate a task or explain an automation rule.

## Database Migrations

Run schema changes via Alembic:

```bash
cd webhealth-backend
uv run alembic upgrade head   # apply latest migrations
uv run alembic revision -m "..." --autogenerate  # create new migration (DB required)
```

The current head introduces the `security_audits` table plus monitor security columns for the passive-check pipeline.

## Email Notifications

Notifications now send real emails via SMTP. Configure the following environment variables (defaults match the Gmail account you provided):

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=leightonsilver@gmail.com
MAIL_PASSWORD=qxfjyciwtityhvrz
MAIL_DEFAULT_SENDER=silverrakinzi@gmail.com
```

Set them before starting FastAPI so `NotificationService` can deliver messages to your alert recipients.
