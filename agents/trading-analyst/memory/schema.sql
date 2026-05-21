-- Trading Analyst SQLite Schema
-- Database: agents/trading-analyst/memory/trading.db
-- Generated: 2026-05-21

CREATE TABLE IF NOT EXISTS setups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    side TEXT NOT NULL,                  -- long | short
    framework TEXT NOT NULL,             -- ICT setup name (e.g. order-block, FVG, liquidity-grab)
    entry REAL,
    stop REAL,
    target_1 REAL,
    target_2 REAL,
    risk_reward REAL,                    -- computed: (target_1 - entry) / (entry - stop)
    position_size REAL,                  -- shares/contracts
    risk_amount REAL,                    -- dollars at risk (1% of book)
    status TEXT DEFAULT 'watching',      -- watching | active | closed | invalidated
    setup_date TEXT DEFAULT (datetime('now')),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS posture_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posture TEXT NOT NULL,               -- risk-on | risk-off | neutral | cautious
    macro_regime TEXT,                   -- bull | bear | sideways | volatile
    recorded_at TEXT DEFAULT (datetime('now')),
    rationale TEXT
);

CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setup_id INTEGER REFERENCES setups(id),
    entry_date TEXT,
    exit_date TEXT,
    entry_price REAL,
    exit_price REAL,
    pnl REAL,                            -- realized P&L
    pnl_pct REAL,                        -- percentage gain/loss
    outcome TEXT,                        -- win | loss | breakeven
    thesis TEXT,                         -- what was the thesis
    what_worked TEXT,
    what_didnt TEXT,
    lesson TEXT
);

CREATE TABLE IF NOT EXISTS learnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,              -- entry | exit | sizing | framework | regime | psychology
    learning TEXT NOT NULL,
    confidence TEXT DEFAULT 'medium',    -- low | medium | high
    added_at TEXT DEFAULT (datetime('now')),
    source TEXT                          -- journal_id or free-text reference
);

CREATE INDEX IF NOT EXISTS idx_setups_ticker ON setups(ticker);
CREATE INDEX IF NOT EXISTS idx_setups_status ON setups(status);
CREATE INDEX IF NOT EXISTS idx_journal_outcome ON journal(outcome);
CREATE INDEX IF NOT EXISTS idx_posture_date ON posture_history(recorded_at);
