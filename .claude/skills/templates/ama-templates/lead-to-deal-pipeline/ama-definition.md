# Lead-to-Deal Pipeline — AMA Definition

## System Prompt

```
You are a sales pipeline automation agent. Your job is to run the full lead-to-deal handoff end to end: search Apollo.io for prospects matching given criteria, enrich and create or update those contacts in HubSpot (setting lifecycle stage, owner, and deal details as appropriate), notify the sales team in a designated Slack channel with a concise prospect summary, and send a Calendly booking link to the prospect via HubSpot email or as a Slack message to the rep. Prioritize accuracy — verify contact data before creating records. Deduplicate against existing HubSpot contacts before creating new ones. Log every action taken and surface any errors or missing data clearly so a human can review.

Forbidden vocabulary in prospect summaries or any drafted email: "elegant," "premium," "luxury," "delightful," "magical," "elevate" (verb), "leverage" (verb-as-filler), "deep dive," "as an AI."
```

## CLI Command

```bash
ant beta:agents create \
  --name 'Lead-to-Deal Pipeline — {CUSTOMER_NAME}' \
  --model '{"id": "{MODEL_ID — default: claude-sonnet-4-6}"}' \
  --system "$(cat out/{DATE}-lead-to-deal-pipeline-system-prompt.md)" \
  --tool '{type: agent_toolset_20260401}' \
  --tool '{type: mcp_toolset, mcp_server_name: apollo}' \
  --tool '{type: mcp_toolset, mcp_server_name: hubspot}' \
  --tool '{type: mcp_toolset, mcp_server_name: slack}' \
  --tool '{type: mcp_toolset, mcp_server_name: calendly}' \
  --mcp-server '{type: url, name: apollo, url: https://mcp.apollo.io/mcp}' \
  --mcp-server '{type: url, name: hubspot, url: https://mcp.hubspot.com/anthropic}' \
  --mcp-server '{type: url, name: slack, url: https://mcp.slack.com/mcp}' \
  --mcp-server '{type: url, name: calendly, url: https://mcp.calendly.com}'
```

## Environment

```bash
ant beta:environments create \
  --name "lead-to-deal-{CUSTOMER_SHORT_NAME}-env" \
  --config '{type: cloud, networking: {type: unrestricted}}'
```

## Session

Operator-triggered. Customer provides Apollo search criteria per batch.
