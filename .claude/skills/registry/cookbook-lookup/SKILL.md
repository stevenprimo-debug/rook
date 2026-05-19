---
name: cookbook-lookup
description: Anthropic Claude Cookbooks reference library. Use this skill ANY time the operator says "think about," "how would I build," "what's the pattern for," "best practice for," "cookbook for," "reference for," "how does Claude handle," "agent pattern for," "show me how to," or asks about RAG, tool use, extended thinking, agent workflows, evaluations, vision, multimodal, prompt caching, context management, memory, MCP patterns, or the Claude Agent SDK. Also trigger when the operator is architecting something new and needs to see how Anthropic recommends approaching it. Even casual mentions like "is there a cookbook for this" or "what does Anthropic say about X" should trigger this skill. The goal is zero reinvention — if Anthropic has published a pattern, surface it before building from scratch.
---

# Anthropic Claude Cookbooks — Reference Lookup

## Purpose

This skill searches the official Anthropic Claude Cookbooks repository (github.com/anthropics/claude-cookbooks) and surfaces relevant patterns, code examples, and architectural guidance before you build something from scratch.

## When This Skill Activates

- "Think about [X]" or "How would I build [X]"
- "What's the pattern for [X]"
- "Best practice for [X]"
- "Is there a cookbook for [X]"
- Any architecture/design question involving Claude capabilities
- Before building any agent, RAG system, tool pipeline, or multi-step workflow

## How It Works

1. **Match the request** against the cookbook registry index below
2. **Fetch the relevant notebook** from GitHub using WebFetch
3. **Extract the key pattern/approach** and present it concisely
4. **Link to the full notebook** for deeper reference

## Fetching Notebooks

All notebooks live at predictable raw URLs. To fetch any notebook:

```
https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/{path}
```

Use WebFetch with the prompt: "Extract the key concepts, code patterns, and architectural decisions from this notebook. Focus on the approach and reusable patterns, not boilerplate."

For large notebooks, focus the WebFetch prompt on the specific section relevant to the user's question.

---

## Cookbook Registry Index

### Agent Patterns

| Title | Path | Description |
|-------|------|-------------|
| Basic workflows | patterns/agents/basic_workflows.ipynb | Three multi-LLM workflow patterns: prompt chaining, routing, parallelization |
| Orchestrator workers | patterns/agents/orchestrator_workers.ipynb | Central LLM delegates tasks to worker LLMs and synthesizes results |
| Evaluator optimizer | patterns/agents/evaluator_optimizer.ipynb | One LLM generates, another evaluates in a feedback loop |
| Customer service agent | tool_use/customer_service_agent.ipynb | Build customer service chatbot with tools for lookup and order management |
| Memory & context management | tool_use/memory_cookbook.ipynb | Persistent memory using Claude's memory tool and context editing |
| Session memory compaction | misc/session_memory_compaction.ipynb | Manage long conversations with instant memory compaction and prompt caching |
| Automatic context compaction | tool_use/automatic-context-compaction.ipynb | Manage context limits by automatically compressing conversation history |
| Context engineering | tool_use/context_engineering/context_engineering_tools.ipynb | Compare context strategies for long-running agents — cost, tradeoffs, composition |
| Using Haiku as sub-agent | multimodal/using_sub_agents.ipynb | Haiku sub-agents for extraction, Opus for synthesis |

### Claude Agent SDK

| Title | Path | Description |
|-------|------|-------------|
| One-liner research agent | claude_agent_sdk/00_The_one_liner_research_agent.ipynb | Build a research agent using Claude Code SDK with WebSearch |
| Chief of staff agent | claude_agent_sdk/01_The_chief_of_staff_agent.ipynb | Multi-agent systems with subagents, hooks, output styles, plan mode |
| Observability agent | claude_agent_sdk/02_The_observability_agent.ipynb | Connect agents to external systems via MCP for GitHub monitoring and CI |
| Site reliability agent | claude_agent_sdk/03_The_site_reliability_agent.ipynb | Incident response agent with read-write MCP tools for diagnosis and remediation |
| Migrating from OpenAI Agents SDK | claude_agent_sdk/04_migrating_from_openai_agents_sdk.ipynb | Port OpenAI Agents SDK to Claude Agent SDK — tools, guardrails, sessions, handoffs |
| Building a session browser | claude_agent_sdk/05_Building_a_session_browser.ipynb | List, read, rename, tag, fork Agent SDK sessions on disk |

### Tools & Tool Use

| Title | Path | Description |
|-------|------|-------------|
| Programmatic tool calling (PTC) | tool_use/programmatic_tool_calling_ptc.ipynb | Reduce latency by letting Claude write code that calls tools programmatically |
| Tool search with embeddings | tool_use/tool_search_with_embeddings.ipynb | Scale to thousands of tools using semantic embeddings for dynamic discovery |
| Parallel tool calls | tool_use/parallel_tools.ipynb | Enable parallel tool calls using batch tool meta-pattern |
| Tool choice | tool_use/tool_choice.ipynb | Control tool selection with tool_choice parameter |
| Extracting structured JSON | tool_use/extracting_structured_json.ipynb | Extract structured JSON using tool use capabilities |
| Tool use with Pydantic | tool_use/tool_use_with_pydantic.ipynb | Create validated tools using Pydantic models for type-safe interactions |
| Vision with tools | tool_use/vision_with_tools.ipynb | Combine vision with tools to extract structured data from images |
| Calculator tool | tool_use/calculator_tool.ipynb | Calculator tool for arithmetic operations |

### RAG & Retrieval

| Title | Path | Description |
|-------|------|-------------|
| Knowledge graph construction | capabilities/knowledge_graph/guide.ipynb | Build knowledge graphs from unstructured text — entity extraction, relation mining, multi-hop querying |
| Contextual retrieval | capabilities/contextual-embeddings/guide.ipynb | Improve RAG accuracy by adding context to chunks before embedding |
| RAG fundamentals | capabilities/retrieval_augmented_generation/guide.ipynb | Build and optimize RAG systems with summary indexing and reranking |
| Text to SQL | capabilities/text_to_sql/guide.ipynb | Convert natural language to SQL using RAG and chain-of-thought |
| Classification | capabilities/classification/guide.ipynb | Build classification systems with RAG and chain-of-thought |
| Summarization | capabilities/summarization/guide.ipynb | Summarize legal documents with evaluation and advanced techniques |
| Citations | misc/using_citations.ipynb | Enable detailed source citations for document-based answers |

### Extended Thinking

| Title | Path | Description |
|-------|------|-------------|
| Extended thinking | extended_thinking/extended_thinking.ipynb | Transparent step-by-step reasoning with budget management |
| Extended thinking with tools | extended_thinking/extended_thinking_with_tool_use.ipynb | Combine extended thinking with tools for transparent multi-step reasoning |

### Multimodal

| Title | Path | Description |
|-------|------|-------------|
| Getting started with vision | multimodal/getting_started_with_vision.ipynb | Pass images to Claude API for vision-based analysis |
| Best practices for vision | multimodal/best_practices_for_vision.ipynb | Tips for optimal image processing performance |
| Crop tool for image analysis | multimodal/crop_tool.ipynb | Give Claude a crop tool to zoom into image regions |
| Transcribe documents | multimodal/how_to_transcribe_text.ipynb | Extract and structure text from images and PDFs |
| Charts, graphs, slide decks | multimodal/reading_charts_graphs_powerpoints.ipynb | Extract insights from charts, graphs, presentations |

### Responses & Prompt Engineering

| Title | Path | Description |
|-------|------|-------------|
| JSON mode | misc/how_to_enable_json_mode.ipynb | Get reliable JSON output with effective prompting |
| Metaprompt | misc/metaprompt.ipynb | Generate starting prompts for tasks — solve the blank page problem |
| Prompt caching | misc/prompt_caching.ipynb | Cache and reuse prompt context for cost savings |
| Speculative prompt caching | misc/speculative_prompt_caching.ipynb | Warm cache speculatively while users formulate queries |
| Batch processing | misc/batch_processing.ipynb | Process large volumes asynchronously with 50% cost reduction |
| Sampling past max tokens | misc/sampling_past_max_tokens.ipynb | Generate longer responses using prefill continuation |
| Moderation filter | misc/building_moderation_filter.ipynb | Build customizable content moderation filters |
| Frontend aesthetics prompting | coding/prompting_for_frontend_aesthetics.ipynb | Prompt Claude for distinctive, polished frontend designs |

### Evaluations

| Title | Path | Description |
|-------|------|-------------|
| Building evals | misc/building_evals.ipynb | Build evaluation systems to measure and improve Claude's performance |
| Generate synthetic test data | misc/generate_test_cases.ipynb | Generate synthetic test cases to evaluate prompt templates |
| Tool evaluation | tool_evaluation/tool_evaluation.ipynb | Run parallel agent evaluations on tools from evaluation task files |

### Skills Development

| Title | Path | Description |
|-------|------|-------------|
| Introduction to Skills | skills/notebooks/01_skills_introduction.ipynb | Create documents, analyze data, automate workflows with Excel, PowerPoint, PDF skills |
| Skills for financial apps | skills/notebooks/02_skills_financial_applications.ipynb | Financial dashboards and portfolio analytics with skills |
| Building custom skills | skills/notebooks/03_skills_custom_development.ipynb | Create, deploy, and manage custom skills for organizational workflows |

### Integrations

| Title | Path | Description |
|-------|------|-------------|
| ElevenLabs voice assistant | third_party/ElevenLabs/low_latency_stt_claude_tts.ipynb | Low-latency voice assistant with speech-to-text and text-to-speech |
| LlamaIndex RAG | third_party/LlamaIndex/Basic_RAG_With_LlamaIndex.ipynb | Basic RAG pipeline with LlamaIndex |
| LlamaIndex multi-document agents | third_party/LlamaIndex/Multi_Document_Agents.ipynb | RAG for large document collections with DocumentAgents |
| LlamaIndex ReAct agent | third_party/LlamaIndex/ReAct_Agent.ipynb | ReAct agents with tool-based reasoning |
| MongoDB RAG | third_party/MongoDB/rag_using_mongodb.ipynb | RAG system with Claude and MongoDB |
| Pinecone RAG | third_party/Pinecone/rag_using_pinecone.ipynb | Vector database RAG with Pinecone |
| Pinecone RAG agents | third_party/Pinecone/claude_3_rag_agent.ipynb | RAG agents with LangChain v1 |
| Wolfram Alpha tool | third_party/WolframAlpha/using_llm_api.ipynb | Wolfram Alpha as Claude tool for computational queries |

### Observability & Admin

| Title | Path | Description |
|-------|------|-------------|
| Usage & cost API | observability/usage_cost_api.ipynb | Access and analyze Claude API usage and cost data |
| PDF upload & summarization | misc/pdf_upload_summarization.ipynb | Process PDFs with text extraction and encoding |
| SQL queries | misc/how_to_make_sql_queries.ipynb | Generate SQL from natural language with schema context |

---

## Usage Pattern

When this skill triggers:

1. **Identify the category** from the registry above that matches the user's question
2. **Fetch the most relevant notebook(s)** using:
   ```
   WebFetch URL: https://raw.githubusercontent.com/anthropics/claude-cookbooks/main/{path}
   Prompt: "Extract the key concepts, architecture decisions, and reusable code patterns. Focus on the approach, not boilerplate setup."
   ```
3. **Present the pattern concisely** — headline first, then offer to go deeper
4. **Link to the notebook** for full reference:
   ```
   https://github.com/anthropics/claude-cookbooks/blob/main/{path}
   ```

## Important Notes

- This skill is READ-ONLY reference. It surfaces patterns — it doesn't execute notebook code.
- Always check the registry first before fetching. Don't fetch notebooks that aren't relevant.
- For multi-topic questions, fetch the most relevant single notebook first, then offer related ones.
- The registry was last synced from the official repo. If a topic isn't listed, use WebSearch to check if a new cookbook has been added.
- Prefer the Anthropic-recommended pattern over rolling your own approach.
