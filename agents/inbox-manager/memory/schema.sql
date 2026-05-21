-- Inbox Manager SQLite Schema
-- Database: agents/inbox-manager/memory/messages.db
-- Generated: 2026-05-21

CREATE TABLE IF NOT EXISTS threads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel TEXT NOT NULL,               -- gmail | whatsapp | other
    external_id TEXT,                   -- channel-native thread/conversation ID
    subject TEXT,
    sender_email TEXT,
    sender_name TEXT,
    status TEXT NOT NULL DEFAULT 'unread', -- unread | categorized | draft-ready | sent | archived | snoozed
    category TEXT,                       -- REPLY_NEEDED | FYI_ONLY | NEWSLETTER | SPAM | WAITING_ON_THEM
    received_at TEXT,
    last_activity TEXT DEFAULT (datetime('now')),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER NOT NULL REFERENCES threads(id),
    direction TEXT NOT NULL,             -- inbound | outbound
    body_preview TEXT,                   -- first 500 chars
    sent_at TEXT,
    channel_message_id TEXT             -- channel-native message ID
);

CREATE TABLE IF NOT EXISTS drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER NOT NULL REFERENCES threads(id),
    body TEXT NOT NULL,
    status TEXT DEFAULT 'pending',       -- pending | approved | sent | discarded
    created_at TEXT DEFAULT (datetime('now')),
    approved_at TEXT,
    sent_at TEXT
);

CREATE TABLE IF NOT EXISTS escalations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id INTEGER NOT NULL REFERENCES threads(id),
    escalated_to TEXT NOT NULL,          -- agent slug or operator
    reason TEXT,
    escalated_at TEXT DEFAULT (datetime('now')),
    resolved_at TEXT
);

CREATE TABLE IF NOT EXISTS triage_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT DEFAULT (datetime('now')),
    threads_reviewed INTEGER DEFAULT 0,
    reply_needed INTEGER DEFAULT 0,
    fyi_only INTEGER DEFAULT 0,
    archived INTEGER DEFAULT 0,
    drafts_created INTEGER DEFAULT 0,
    drafts_sent INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_threads_status ON threads(status);
CREATE INDEX IF NOT EXISTS idx_threads_channel ON threads(channel);
CREATE INDEX IF NOT EXISTS idx_drafts_thread ON drafts(thread_id);
CREATE INDEX IF NOT EXISTS idx_drafts_status ON drafts(status);
