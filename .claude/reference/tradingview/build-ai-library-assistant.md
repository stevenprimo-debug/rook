---
title: Build AI library assistant | Advanced Charts Documentation
source: https://www.tradingview.com/charting-library-docs/latest/resources/llm-context
author: []
published: []
created: 2026-05-12
description: Overview
tags: [clippings]
---
## Overview

Using generic AI assistants for library-specific questions can be unreliable. The models often rely on outdated public data, which can lead to frustrating results.

To address this challenge, a [downloadable knowledge file](https://www.tradingview.com/charting-library-docs/charting-library-context.txt) is now available, containing the complete documentation. By providing this file as a knowledge base, you can turn a general-purpose AI into a dedicated expert on the library. Ask complex questions and receive detailed answers, code examples, and direct links back to the documentation.

## File contents and prerequisites

The [charting-library-context.txt](https://www.tradingview.com/charting-library-docs/charting-library-context.txt) file is a comprehensive knowledge base compiled directly from our official sources. It contains the complete public documentation and full TypeScript definitions, ensuring the AI has a deep and accurate understanding of the library.

Before you begin, review the technical information below.

- **File size.** Approximately 670,000 tokens.
- **Model compatibility.** Due to its large size, this file requires an AI model with a very large [context window](https://en.wikipedia.org/wiki/Large_language_model#Attention_mechanism_and_context_window) (one million tokens or more).
- **Version specificity.** The file is always for the **latest version** of our library. Consequently, solutions and code examples provided by the AI may not be compatible with older versions of the library.

> [!-info] -info
> info
> The exact token count can vary slightly between different AI providers, but the file size remains a critical factor for model compatibility.

## How to use

Follow these steps to get started. We'll use Google AI Studio as an example, but the process is similar for other AI tools that support large file uploads.

1. Download the [charting-library-context.txt](https://www.tradingview.com/charting-library-docs/charting-library-context.txt) file.
2. Go to the [Google AI Studio](https://aistudio.google.com/welcome) website and sign in.
3. Start a new chat with the assistant.
4. Upload the file to the prompt box.
5. Start asking questions in the prompt box. For example: "How can I hide the toolbar on the left?"

The AI will answer your question using only the information contained in the file you provided. See the example below.

![LLM answer example](https://www.tradingview.com/charting-library-docs/assets/images/llm-context-example-a934d0604636643c7a9ebc84b3006554.png)

## Best practices

To get the most out of this feature, follow these tips:

- **Be specific.** The more detailed your question, the better the answer.
- **Start a new chat for new topics.** To prevent context confusion, start a fresh chat when switching between major topics (e.g., from custom indicators to data integration).
- **Tune the AI for accuracy.** If your AI tool allows it, adjust the model settings for better results:
	- **Choose the best model.** Always select the latest, most powerful model available.
		- **Set a low temperature.** To minimize AI "creativity" and force it to stick to the facts, adjust the temperature setting to a low value.
- **Ask for code.** Explicitly ask the AI to "provide a full JavaScript code example" or "show me the TypeScript interface for this."
- **Verify with the documentation.** The AI is trained to provide direct links to the official documentation. Use these to double-check critical information and explore topics further.

## Limitations and disclaimers

Please keep the following in mind when using this feature:

- **The official documentation is the source of truth.** While the AI is highly accurate, it is still a tool. This documentation website should always be considered the definitive source of information.
- **Your code, your control.** The AI-generated responses and code are for informational purposes only and should not be considered official TradingView advice. It is **your responsibility** to thoroughly test, verify, and validate any code or suggestions before implementing them in a production environment. TradingView assumes no responsibility for any outcomes resulting from the use of AI-generated content.
- **AI can make mistakes.** The model may misinterpret a question or "hallucinate." If an answer seems incorrect, try rephrasing your question or refer to the official documentation website.
- **No support for third-party tools.** TradingView doesn't provide technical support for any third-party LLM service.