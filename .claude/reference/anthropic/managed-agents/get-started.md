---
title: Get started with Claude Managed Agents
source: https://platform.claude.com/docs/en/managed-agents/quickstart
author: []
published: []
created: 2026-05-15
description: Create your first autonomous agent.
tags: [clippings]
category: vendor-api-reference
rook-relevance: high
rook-consumers: software-dev-team, chief-of-staff
---
This guide walks you through creating an agent, setting up an environment, starting a session, and streaming agent responses.

**Prefer an interactive walkthrough?** Run `/claude-api managed-agents-onboard` in the latest version of [Claude Code](https://claude.com/product/claude-code) for a guided setup and interactive question-answering.

## Core concepts

| Concept | Description |
| --- | --- |
| **Agent** | The model, system prompt, tools, MCP servers, and skills |
| **Environment** | A configured container template (packages, network access) |
| **Session** | A running agent instance within an environment, performing a specific task and generating outputs |
| **Events** | Messages exchanged between your application and the agent (user turns, tool results, status updates) |

## Prerequisites

- An Anthropic [Console account](https://platform.claude.com/)
- An [API key](https://platform.claude.com/settings/keys)

## Install the CLI

```
brew install anthropics/tap/ant
```

Check the installation:

```
ant --version
```

## Install the SDK

```
npm install @anthropic-ai/sdk
```

Set your API key as an environment variable:

```
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Create your first session

All Managed Agents API requests require the `managed-agents-2026-04-01` beta header. The SDK sets the beta header automatically.

1. Create an agent
	Create an agent that defines the model, system prompt, and available tools.
	```
	ant beta:agents create \
	  --name "Coding Assistant" \
	  --model '{id: claude-opus-4-7}' \
	  --system "You are a helpful coding assistant. Write clean, well-documented code." \
	  --tool '{type: agent_toolset_20260401}'
	```
	The `agent_toolset_20260401` tool type enables the full set of pre-built agent tools (bash, file operations, web search, and more). See [Tools](https://platform.claude.com/docs/en/managed-agents/tools) for the complete list and per-tool configuration options.
	Save the returned `agent.id`. You'll reference it in every session you create.
2. Create an environment
	An environment defines the container where your agent runs.
	```
	ant beta:environments create \
	  --name "quickstart-env" \
	  --config '{type: cloud, networking: {type: unrestricted}}'
	```
	Save the returned `environment.id`. You'll reference it in every session you create.
3. Start a session
	Create a session that references your agent and environment.
	```
	const session = await client.beta.sessions.create({
	  agent: agent.id,
	  environment_id: environment.id,
	  title: "Quickstart session",
	});
	console.log(\`Session ID: ${session.id}\`);
	```
4. Send a message and stream the response
	Open a stream, send a user event, then process events as they arrive:
	```
	const stream = await client.beta.sessions.events.stream(session.id);
	// Send the user message after the stream opens
	await client.beta.sessions.events.send(session.id, {
	  events: [
	    {
	      type: "user.message",
	      content: [
	        {
	          type: "text",
	          text: "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
	        },
	      ],
	    },
	  ],
	});
	// Process streaming events
	for await (const event of stream) {
	  if (event.type === "agent.message") {
	    for (const block of event.content) {
	      process.stdout.write(block.text);
	    }
	  } else if (event.type === "agent.tool_use") {
	    console.log(\`\n[Using tool: ${event.name}]\`);
	  } else if (event.type === "session.status_idle") {
	    console.log("\n\nAgent finished.");
	    break;
	  }
	}
	```
	The agent will write a Python script, execute it in the container, and verify the output file was created. Your output will look similar to this:
	```
	I'll create a Python script that generates the first 20 Fibonacci numbers and saves them to a file.
	[Using tool: write]
	[Using tool: bash]
	The script ran successfully. Let me verify the output file.
	[Using tool: bash]
	fibonacci.txt contains the first 20 Fibonacci numbers (0 through 4181).
	Agent finished.
	```

## What's happening

When you send a user event, Claude Managed Agents:

1. **Provisions a container:** Your environment configuration determines how it's built.
2. **Runs the agent loop:** Claude decides which tools to use based on your message
3. **Executes tools:** File writes, bash commands, and other tool calls run inside the container
4. **Streams events:** You receive real-time updates as the agent works
5. **Goes idle:** The agent emits a `session.status_idle` event when it has nothing more to do