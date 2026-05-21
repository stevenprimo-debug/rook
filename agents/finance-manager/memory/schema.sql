-- Finance Manager SQLite Schema
-- Database: agents/finance-manager/memory/finance.db
-- Generated: 2026-05-21

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE,
    client TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    status TEXT NOT NULL DEFAULT 'pending',  -- pending | sent | paid | overdue | written-off
    issued_date TEXT,                        -- ISO-8601
    due_date TEXT,                           -- ISO-8601
    paid_date TEXT,                          -- ISO-8601
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS commissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_name TEXT NOT NULL,
    client TEXT NOT NULL,
    deal_value REAL NOT NULL,
    gp_pct REAL NOT NULL,
    gp_dollars REAL,                         -- computed: deal_value * gp_pct
    commission_rate REAL DEFAULT 0.10,       -- default 10%
    commission_amount REAL,                  -- computed: gp_dollars * commission_rate
    status TEXT NOT NULL DEFAULT 'pending',  -- pending | earned | paid | clawback
    expected_pay_date TEXT,                  -- ISO-8601
    actual_pay_date TEXT,                    -- ISO-8601
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS deal_economics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deal_name TEXT NOT NULL,
    total_value REAL NOT NULL,
    gp_pct REAL NOT NULL,
    fulfillment_hours REAL,                  -- estimated hours to fulfill
    dollars_per_hour REAL,                   -- computed: (total_value * gp_pct) / fulfillment_hours
    auto_reject BOOLEAN DEFAULT 0,           -- 1 if below minimum thresholds
    reject_reason TEXT,                      -- e.g. "below $15K commission floor"
    evaluated_at TEXT DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status);
CREATE INDEX IF NOT EXISTS idx_invoices_due ON invoices(due_date);
CREATE INDEX IF NOT EXISTS idx_commissions_status ON commissions(status);
CREATE INDEX IF NOT EXISTS idx_commissions_expected_pay ON commissions(expected_pay_date);
