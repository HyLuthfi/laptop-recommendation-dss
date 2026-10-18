# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-18

Initial stable release of **Automated Laptop Recommendation Decision Support System (MCDM: SAW, TOPSIS, WASPAS)** — an enterprise-grade multi-criteria decision analysis platform evaluating 1,304 commercial laptops through mathematical rigor, dynamic criteria weighting, and an interactive Streamlit analytics dashboard.

### Added

- **Triple MCDM Computational Engine**:
  - Implementation of **Simple Additive Weighting (SAW)** utilizing linear scale transformation across cost ($r_{ij} = \min / x_{ij}$) and benefit ($r_{ij} = x_{ij} / \max$) criteria.
  - Implementation of **Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)** utilizing vector normalization, weighted normalized matrices, Euclidean distance to Positive Ideal ($A^+$) and Negative Ideal ($A^-$) solutions, and relative closeness coefficients.
  - Implementation of **Weighted Aggregated Sum Product Assessment (WASPAS)** combining additive (WSM) and multiplicative (WPM) utility models parameterized with joint coefficient $\lambda = 0.5$ for enhanced ranking stability.
- **Dynamic Multi-Criteria Weighting & Filtering Core**:
  - Evaluation across 5 core criteria: Price ($C_1$, Cost, 35%), RAM Capacity ($C_2$, Benefit, 20%), Storage ($C_3$, Benefit, 20%), Weight ($C_4$, Cost, 15%), and Screen Size ($C_5$, Benefit, 10%).
  - Real-time user parameter sliders for budget constraints (200 - 6,000 EUR) and minimum RAM filtering (4 - 64 GB).
- **Interactive Streamlit Web Dashboard (`app.py`)**:
  - 5-tab modular analytics architecture: Executive Summary Dashboard, SAW Method Decomposition, TOPSIS Method Decomposition, WASPAS Method Decomposition, and Visual Metric Distributions.
  - Multi-method consensus ranking leaderboard tracking top-5 laptop recommendations across all algorithms.
  - Scatter plots visualizing Price vs Preference Score with Matplotlib and Seaborn integration.
- **Comprehensive Commercial Laptop Dataset**:
  - Ingestion of 1,304 verified commercial laptop specifications (`dataset_laptop_lengkap.csv`, 201KB) across major manufacturers (Apple, Dell, Asus, Lenovo, HP, MSI, Acer).
- **Showcase DX & Visual Documentation**:
  - D2 vector architecture diagram (`assets/architecture.svg`) compiled in Terminal Dark palette with ELK layout engine documenting the 5 MCDM computational layers.
  - Standard 9-element portfolio `README.md` featuring dynamic typing header, comparative mathematical formula table, and zero promotional buzzwords.
  - Live cloud deployment integration on Streamlit Community Cloud (`laptop-recommendation-dss.streamlit.app`).

### Changed

- **Numerical Stability & Zero-Division Safeguards**: Refactored matrix normalization routines with epsilon offsets preventing zero-division errors during dynamic subset filtering.
- **Decomposition Transparency**: Exposed intermediate computational matrices (normalized matrices, weighted normalized tensors, ideal solutions) directly in UI tabs for academic auditability.

### Security

- **[P0] SPDX MIT License**: Issued official `LICENSE` file under MIT License with legal copyright attributed to `Luthfi Muthathohirin`.
- **[P0] Zero Leak Certification**: Passed comprehensive 12-commit repository history scan with Gitleaks v8.30.1 (**0 leaks detected**, Health Score 98/100).
- **[P0] Hardened `.gitignore`**: Implemented comprehensive 89-rule exclusion filter protecting Python bytecode (`__pycache__/`), virtual environments (`.venv/`), Streamlit secrets (`secrets.toml`), temporary file uploads, and Jupyter notebook checkpoints.
- **Dataset Privacy Verification**: Certified clean dataset containing zero Personally Identifiable Information (PII) or confidential corporate telemetry.
