-- Shopify Agent SQLite Schema
-- Database: agents/shopify-agent/memory/shopify.db
-- Generated: 2026-05-21
-- NOTE: SQLite = historical archive only (>60-day window).
--       Live queries always hit the Shopify Admin API.

CREATE TABLE IF NOT EXISTS merchants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,           -- kebab-case merchant identifier
    name TEXT NOT NULL,
    shopify_domain TEXT,                 -- e.g. my-store.myshopify.com
    plan TEXT,                           -- basic | shopify | advanced | plus
    status TEXT DEFAULT 'active',        -- active | paused | churned
    notes TEXT,
    cs_voice TEXT,                       -- tone/voice for CS emails (e.g. "warm", "direct")
    status_color_map JSON,               -- merchant-specific production status color map
    shopify_payments_active BOOLEAN DEFAULT 1, -- 0 when Payments paused (affects disputes API)
    bulk_export_signed_url_expires_at TIMESTAMP, -- GCS signed URL expiry for bulk ops
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    shopify_order_id TEXT,              -- Shopify's order GID
    order_number TEXT,
    customer_id INTEGER REFERENCES customers(id),
    total_price REAL,
    subtotal REAL,
    tax REAL,
    currency TEXT DEFAULT 'USD',
    financial_status TEXT,              -- pending | authorized | paid | refunded | voided | chargeback
    fulfillment_status TEXT,            -- null | partial | fulfilled
    has_chargeback BOOLEAN DEFAULT 0,   -- fallback flag from CSV financial_status column
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    title TEXT,
    sku TEXT,
    quantity INTEGER,
    price REAL,
    total_discount REAL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_id INTEGER NOT NULL REFERENCES merchants(id),
    shopify_customer_id TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    orders_count INTEGER DEFAULT 0,
    total_spent REAL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS fulfillment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    status TEXT NOT NULL,               -- pending | open | success | cancelled | error
    tracking_number TEXT,
    carrier TEXT,
    shipped_at TEXT,
    delivered_at TEXT
);

CREATE TABLE IF NOT EXISTS disputes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dispute_id TEXT UNIQUE,             -- Shopify dispute GID
    order_id INTEGER NOT NULL REFERENCES orders(id),
    opened_at TEXT,
    reason_code TEXT,                   -- e.g. fraudulent | subscription_cancelled | credit_not_processed
    amount REAL,
    currency TEXT DEFAULT 'USD',
    status TEXT,                        -- NEEDS_RESPONSE | UNDER_REVIEW | ACCEPTED | WON | LOST
    evidence_due_by TEXT,
    finalized_on TEXT,
    raw_json TEXT                       -- full dispute node from bulk JSONL
);

CREATE TABLE IF NOT EXISTS house_numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    house_digits TEXT NOT NULL,         -- the numeric portion of the house number
    street TEXT,                        -- full street name if available
    side_text TEXT,                     -- suffix/prefix (e.g. "N", "S", "1/2")
    source TEXT,                        -- line_item_property | csv_shipping_address | manual
    set_at TEXT DEFAULT (datetime('now')) -- immutable once set; perfect cache candidate
);

CREATE INDEX IF NOT EXISTS idx_orders_merchant ON orders(merchant_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(financial_status);
CREATE INDEX IF NOT EXISTS idx_orders_chargeback ON orders(has_chargeback);
CREATE INDEX IF NOT EXISTS idx_customers_merchant ON customers(merchant_id);
CREATE INDEX IF NOT EXISTS idx_line_items_order ON line_items(order_id);
CREATE INDEX IF NOT EXISTS idx_disputes_order ON disputes(order_id);
CREATE INDEX IF NOT EXISTS idx_disputes_status ON disputes(status);
CREATE INDEX IF NOT EXISTS idx_house_numbers_order ON house_numbers(order_id);
