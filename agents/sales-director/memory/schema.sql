-- Sales Director SQLite Schema
-- Database: agents/sales-director/memory/pipeline.db
-- Generated: 2026-05-21

CREATE TABLE IF NOT EXISTS prospects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    contact_name TEXT,
    contact_title TEXT,
    contact_email TEXT,
    icp_score REAL,                      -- 0.0-1.0 ICP fit score
    source TEXT,                         -- apollo | linkedin | referral | inbound | event
    status TEXT DEFAULT 'uncontacted',   -- uncontacted | contacted | responded | qualified | disqualified
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER REFERENCES prospects(id),
    name TEXT NOT NULL,
    stage TEXT NOT NULL,                 -- discovery | scoping | proposal | negotiation | closed-won | closed-lost
    value REAL,
    gp_pct REAL,
    owner TEXT,
    close_date TEXT,                     -- ISO-8601 target
    closed_at TEXT,                      -- ISO-8601 actual
    lost_reason TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS stage_transitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_id INTEGER NOT NULL REFERENCES deals(id),
    from_stage TEXT,
    to_stage TEXT NOT NULL,
    transitioned_at TEXT DEFAULT (datetime('now')),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS outreach_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prospect_id INTEGER NOT NULL REFERENCES prospects(id),
    touch_type TEXT NOT NULL,            -- email | linkedin | call | event | referral
    subject TEXT,
    sent_at TEXT DEFAULT (datetime('now')),
    outcome TEXT,                        -- opened | replied | booked | bounced | no-response
    follow_up_date TEXT                  -- ISO-8601
);

CREATE INDEX IF NOT EXISTS idx_deals_stage ON deals(stage);
CREATE INDEX IF NOT EXISTS idx_deals_close_date ON deals(close_date);
CREATE INDEX IF NOT EXISTS idx_outreach_prospect ON outreach_log(prospect_id);
CREATE INDEX IF NOT EXISTS idx_prospects_status ON prospects(status);
