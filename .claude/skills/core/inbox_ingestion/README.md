# Drive -> Vault INBOX Ingestion Pipeline

Watches `G:\My Drive\Random context 2\` for new images, sends each to Claude Vision (Sonnet) for OCR + categorization, and writes paired markdown + renamed image into the vault INBOX.

## Setup

```bash
cd "CORE"
pip install -r inbox_ingestion/requirements.txt
cp inbox_ingestion/.env.example inbox_ingestion/.env
# Edit .env → set ANTHROPIC_API_KEY
```

## Usage

```bash
# Run manually (from CORE/ directory)
python -m inbox_ingestion

# Dry run — list pending images without processing
python -m inbox_ingestion --dry-run

# Verbose logging
python -m inbox_ingestion -v

# Custom source directory
python -m inbox_ingestion --source-dir "D:\other\folder"
```

## Backfill

First run processes all 51 existing images. Subsequent runs only pick up new ones (idempotent — checks `_processed/` folder).

## Recovery

- **Failed images** land in `Random context 2/_failed/` with errors logged to `error_log.txt`
- To retry: move images from `_failed/` back to `Random context 2/` and re-run
- **Processed originals** are in `Random context 2/_processed/` (never deleted)

## Scheduled polling

Run `schedule_task.ps1` from an elevated PowerShell to register a 15-minute polling task:

```powershell
powershell -ExecutionPolicy Bypass -File schedule_task.ps1
```

To remove: `Unregister-ScheduledTask -TaskName "Vault-InboxIngestion" -Confirm:$false`

## Cost

~$0.008/image with Claude Sonnet. At 50 images/month ≈ $0.40/month.

## Tests

```bash
cd "CORE"
python -m pytest inbox_ingestion/tests/ -v
```
