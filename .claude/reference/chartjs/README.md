---
name: chartjs
source: https://github.com/chartjs/Chart.js
fetched: 2026-05-22
category: javascript-library
rook-relevance: high
rook-consumers: software-dev-team, trading-analyst, finance-manager, marketing-director
license: MIT
---

# Chart.js Project Reference

## Overview

Chart.js is a lightweight JavaScript library that enables designers and developers to create interactive, animated charts with minimal configuration. It provides a simple yet flexible approach to data visualization, supporting multiple chart types and responsive design patterns suitable for both web and mobile applications.

## Installation

**npm:**
```bash
npm install chart.js
```

**CDN:**
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

## Supported Chart Types

Line, bar, pie, doughnut, radar, polar area, bubble, scatter — plus mixed and combined chart types.

## Basic Usage

```javascript
const ctx = document.getElementById('myChart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['January', 'February', 'March'],
    datasets: [{
      label: 'Sales',
      data: [12, 19, 3],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  }
});
```

## Key Features

- **Animation support** — built-in animations for visual feedback
- **Responsive design** — charts adapt to container dimensions automatically
- **Plugin architecture** — extensible system for custom functionality
- **Tree-shakeable** — modular design allows importing only necessary components
- **Canvas-based rendering** — efficient performance across browsers and devices

## ROOK applicability

- **software-dev-team** — dashboard builds, customer-facing analytics surfaces, embedded reporting
- **trading-analyst** — equity curve charts, posture history visualization, backtest result plots
- **finance-manager** — P&L charts, commission tracking, deal-economics waterfalls
- **marketing-director** — campaign performance dashboards, funnel visualizations
- **seo-specialist** — ranking history, AEO baseline trend plots, CWV time-series

Pairs with the `html2pdf` skill in the universal stack — a chart rendered to HTML can be exported to PDF for client deliverables in one pipeline.

## Documentation + resources

| Resource | URL |
|---|---|
| Official documentation | https://www.chartjs.org/docs/latest/ |
| Getting started | https://www.chartjs.org/docs/latest/getting-started/index |
| Chart types reference | https://www.chartjs.org/docs/latest/charts/line |
| Configuration guide | https://www.chartjs.org/docs/latest/configuration/index |
| Live samples | https://www.chartjs.org/samples/ |
| Popular extensions | https://github.com/chartjs/awesome |
| Developer documentation | https://www.chartjs.org/docs/latest/developers/index |

Older versions accessible via URL version pinning (e.g., `chartjs.org/docs/2.9.4/`).

## License

MIT — permits free use in personal and commercial projects.

## Cross-references

- `.claude/skills/core/html-to-pdf/` — pairs with this for chart-to-PDF workflows
- `agents/trading-analyst/SKILL.md` — equity curve + backtest visualization use cases
- `agents/finance-manager/SKILL.md` — P&L dashboard surfaces
- `agents/software-dev-team/SKILL.md` — dashboard builds
