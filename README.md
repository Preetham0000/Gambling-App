# Gambling App

A service-oriented Python application for interactive gambling session management with betting strategies, stake tracking, validation auditing, and terminal reporting.

### Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env  # Edit .env with your DB credentials
```

### Run
```powershell
python .\main.py
```

## Key Features

- **Player Profiles** — Create and manage gamblers with stake boundaries
- **Sessions** — Start, pause, resume, and end betting sessions
- **Betting** — Manual or strategy-driven bets (fixed/percentage/martingale)
- **Stake Tracking** — Real-time stake changes with boundary warnings
- **Reporting** — Live and end-of-session analytics with win/loss KPIs
- **Validation** — Structured validation with persistent audit trail

## Configuration

Set these in `.env`:

| Variable | Default | Required |
|---|---|---|
| DB_HOST | - | yes |
| DB_PORT | 3306 | no |
| DB_NAME | - | yes |
| DB_USER | - | yes |
| DB_PASSWORD | - | yes |
| SESSION_DEFAULT_WIN_PROBABILITY | 0.50 | no |
| SESSION_DEFAULT_MAX_GAMES | 100 | no |
| MIN_INITIAL_STAKE | 100.00 | no |
| MAX_INITIAL_STAKE | 1000000.00 | no |

## Project Structure

```
config/                 Configuration, DB, schema
models/                 Domain models and DTOs
services/               Business logic (betting, sessions, profiles, analytics)
strategies/             Betting strategies (fixed/percentage/martingale)
tracking_and_reports/   Statistics and reporting models
ui/                     Interactive menu and console display
utils/                  Validation and exceptions
main.py                 Entry point
```

## Technology Stack

- **Python 3.14** — Core language
- **MySQL** — Data persistence
- **Decimal** — Financial arithmetic
- **python-dotenv** — Config management

## Architecture

**Layered Design:**
- **UI Layer** (`ui/`) — Rich terminal interactions
- **Service Layer** (`services/`) — Business transactions and rules
- **Model Layer** (`models/`) — Domain DTOs and data structures
- **Data Layer** (`config/`) — DB connection and schema management
- **Validation** (`utils/`) — Cross-cutting validation and exceptions

**Key Patterns:**
- Strategy pattern for bet sizing
- Decorator-based validation guards
- Service layer orchestration
- Explicit transaction boundaries

## Database

**Core Tables:**
- `GAMBLERS` — Player profiles and thresholds
- `BETTING_PREFERENCES` — Per-player wager limits
- `SESSIONS` — Session lifecycle and state
- `BETS` — Individual bet records
- `GAME_RECORDS` — Resolved game outcomes
- `STAKE_TRANSACTIONS` — Ledger of all stake changes
- `RUNNING_TOTALS_SNAPSHOTS` — Cumulative session metrics
- `VALIDATION_EVENTS` — Audit trail for all validations

## Development Standards

- Keep business logic in `services/*`
- Use `Decimal` for monetary/probability operations
- Apply `@validation_guard` to public service methods
- Return typed dataclass DTOs
- Use explicit transaction contexts (`with database.session(...)`)
- Log validation events to `VALIDATION_EVENTS` table

- Validation event logging does not block business flow on failure
- Timestamps stored as naive UTC datetimes
- No automated test suite currently present
