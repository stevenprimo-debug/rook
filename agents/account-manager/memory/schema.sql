-- Account Manager SQLite Schema
-- Database: agents/account-manager/memory/accounts.db
-- Generated: 2026-05-21

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,           -- kebab-case client identifier
    name TEXT NOT NULL,                  -- display name
    stage TEXT NOT NULL,                 -- active | at-risk | closed | prospect
    contract_value REAL,                 -- total contract value
    gp_pct REAL,                         -- gross profit percentage
    owner TEXT,                          -- operator or rep name
    renewal_date TEXT,                   -- ISO-8601 date
    next_check_date TEXT,               -- ISO-8601 next scheduled touchpoint
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    deal_name TEXT NOT NULL,
    value REAL,
    gp_pct REAL,
    stage TEXT NOT NULL,                 -- scoping | proposal | closed-won | closed-lost
    close_date TEXT,                     -- ISO-8601 expected or actual close
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS renewals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    renewal_date TEXT NOT NULL,          -- ISO-8601
    window_open_date TEXT,              -- ISO-8601 (typically 90 days before renewal)
    status TEXT DEFAULT 'pending',       -- pending | initiated | closed | churned
    value REAL,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS at_risk_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL REFERENCES accounts(id),
    signal_type TEXT NOT NULL,           -- quiet | payment-lag | missed-milestone | support-escalation | scope-creep
    detected_at TEXT DEFAULT (datetime('now')),
    description TEXT,
    resolved_at TEXT,
    resolution_notes TEXT
);

-- Index for fast renewal window queries
CREATE INDEX IF NOT EXISTS idx_accounts_renewal_date ON accounts(renewal_date);
CREATE INDEX IF NOT EXISTS idx_at_risk_account ON at_risk_signals(account_id);
CREATE INDEX IF NOT EXISTS idx_at_risk_resolved ON at_risk_signals(resolved_at);
