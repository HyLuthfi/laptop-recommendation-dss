---
name: Bug Report
about: Report a mathematical anomaly, division-by-zero error, or UI issue in Laptop Recommendation DSS
title: "[BUG] "
labels: bug
assignees: ''
---

## Description

A clear and concise description of what the mathematical or application bug is.

## Steps to Reproduce

1. Open application locally or via Streamlit Cloud
2. Set budget range to '...'
3. Adjust criteria weight sliders to:
   - Price ($C_1$): ...
   - RAM ($C_2$): ...
   - Storage ($C_3$): ...
   - Weight ($C_4$): ...
   - Screen Size ($C_5$): ...
4. Select tab '...' (Dashboard / SAW / TOPSIS / WASPAS / Visualisasi)
5. Observe error or anomalous calculation output at '...'

## Expected Behavior

A clear and concise description of what you expected to happen (e.g. valid ranking generated, preference values bounded between $[0, 1]$, TOPSIS relative closeness calculated without NaN/Inf values).

## Actual Behavior / Error Traceback

What actually happened (e.g. `ZeroDivisionError`, `ValueError: Input contains NaN`, ranking mismatch, UI widget failure).

```text
Paste terminal error output or browser console traceback here
```

## Criteria Weight & Filter Parameters

| Parameter | Slider Value | Criterion Type |
|---|---|---|
| **Budget Range** | e.g. 500 - 1500 EUR | Constraint |
| **Minimum RAM** | e.g. 16 GB | Constraint |
| **$C_1$ Price Weight** | e.g. 0.35 | Cost |
| **$C_2$ RAM Weight** | e.g. 0.20 | Benefit |
| **$C_3$ Storage Weight** | e.g. 0.20 | Benefit |
| **$C_4$ Weight Weight** | e.g. 0.15 | Cost |
| **$C_5$ Screen Size Weight** | e.g. 0.10 | Benefit |

## System & Execution Environment

| Parameter | Value |
|---|---|
| **Execution Environment** | Streamlit Community Cloud / Local Python venv |
| **Operating System** | Windows 11 / Ubuntu 22.04 / macOS |
| **Python Version** | e.g. Python 3.10.12 / 3.11.8 |
| **Streamlit Version** | e.g. 1.32.0 |
| **Pandas / NumPy Versions** | e.g. pandas 2.2.0, numpy 1.26.4 |
| **Browser & Version** | e.g. Chrome 129 / Edge / Firefox |

## Additional Context

Add any other context about the problem here (e.g. sample laptop alternative ID triggering the issue, screenshots of the decomposition table).
