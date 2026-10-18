# Contributing to Laptop Recommendation DSS

Thank you for your interest in contributing to **Automated Laptop Recommendation Decision Support System (MCDM: SAW, TOPSIS, WASPAS)** — an open-source mathematical decision support and multi-criteria optimization platform.

This project is maintained by **Luthfi Muthathohirin**.

---

## 🛠️ Architecture & Development Setup

The repository is structured as a pure Python data science and multi-criteria decision-making application:

```text
laptop-recommendation-dss/
├── app.py                         # Streamlit Interactive Dashboard & MCDM Engine
├── dataset_laptop_lengkap.csv     # Commercial laptop dataset (1,304 entries)
├── pemilihan_laptop.ipynb         # Jupyter notebook for algorithm verification & EDA
├── docs/                          # D2 architecture specification (architecture.d2)
├── assets/                        # Compiled vector SVG architecture diagrams
├── requirements.txt               # Python package dependencies
├── LICENSE                        # MIT License
└── .streamlit/config.toml         # Streamlit UI theme configuration
```

### 1. Prerequisites

- **Python**: Version 3.10 or 3.11 (Python 3.10+ recommended)
- **Pip / Virtual Environment**: Standard Python toolchain

### 2. Local Setup & Virtual Environment

```bash
# Clone the repository
git clone https://github.com/HyLuthfi/laptop-recommendation-dss.git
cd laptop-recommendation-dss

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

# Install package dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Running Local Application

Launch the Streamlit dashboard locally:

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`. Test criteria weight adjustments and inspect decomposition tables across all 5 navigation tabs.

---

## 🌿 Contribution Workflow

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally and configure upstream tracking:
   ```bash
   git clone https://github.com/<your-username>/laptop-recommendation-dss.git
   cd laptop-recommendation-dss
   git remote add upstream https://github.com/HyLuthfi/laptop-recommendation-dss.git
   ```
3. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. Implement your enhancements adhering to mathematical validation standards.
5. Verify local numerical outputs and UI rendering via `streamlit run app.py`.
6. Commit your changes following the Conventional Commits specification.
7. Open a **Pull Request** against `main` of the upstream repository.

---

## 📐 Commit Convention

This repository strictly enforces [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

| Prefix | Scope / Usage |
|---|---|
| `feat(scope):` | New feature, MCDM algorithm, or visualization component |
| `fix(scope):` | Bug fix in mathematical normalization, sorting, or UI |
| `docs(scope):` | Documentation updates, mathematical proofs, README edits |
| `chore(scope):` | Tooling, dependencies, repository hygiene |
| `refactor(scope):` | Code refactoring without mathematical behavior mutation |
| `perf(scope):` | Performance optimization (vectorization via NumPy/Pandas) |
| `test(scope):` | Adding numerical verification test cases |
| `security(scope):` | Security hardening, input validation, dependency patches |

**Valid Examples:**
```text
feat(mcdm): implement VIKOR compromise ranking algorithm
fix(normalization): prevent zero-division when price minimum equals zero
perf(matrix): vectorize Euclidean distance calculation with NumPy broadcast
docs(readme): add mathematical formulation for WASPAS joint utility
```

---

## 🔬 Guidelines for Contributing New MCDM Algorithms

We welcome contributions of classical and modern Multi-Criteria Decision Making (MCDM) algorithms (e.g. **AHP**, **VIKOR**, **PROMETHEE**, **MOORA**, **EDAS**, **ELECTRE**, **COPRAS**):

### 1. Mathematical Validation Standards

Every new algorithm implementation must adhere to strict mathematical rigor:

- **Criterion Polarity**: Properly distinguish between **Benefit** (higher is better, e.g. RAM, Storage) and **Cost** (lower is better, e.g. Price, Weight).
- **Scale Invariance & Normalization**: Implement explicit scale transformation:
  - *Linear Scale Transformation*:
    $$r_{ij} = \frac{x_{ij}}{\max_k x_{kj}} \quad (\text{Benefit}), \qquad r_{ij} = \frac{\min_k x_{kj}}{x_{ij}} \quad (\text{Cost})$$
  - *Vector Normalization*:
    $$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^m x_{kj}^2}}$$
- **Division-by-Zero Safeguard**: Add an epsilon guard ($\varepsilon = 10^{-9}$) or minimum bounds check before division.

### 2. Implementation Architecture in `app.py`

When adding a new method (e.g. `METHOD_NAME`):
1. **Computation Function**: Implement a pure mathematical function accepting `(df_subset, weights, criteria_types)` returning ranked results and intermediate decomposition matrices.
2. **Decomposition UI Tab**: Add a dedicated Streamlit tab displaying step-by-step intermediate matrices (e.g. normalized decision matrix, weighted matrix, utility measures).
3. **Consensus Integration**: Add the resulting preference scores to the executive summary leaderboard and correlation matrix.

### 3. Numerical Verification

Include numerical test verification in `pemilihan_laptop.ipynb` comparing the algorithm's output against established benchmark literature or manual matrix computation.

---

## 📊 Dataset Maintenance & Ethics

1. **Commercial Data Integrity**: Only commit genuine, verified laptop technical specifications. Do not fabricate hypothetical benchmarks.
2. **Zero Personally Identifiable Information (PII)**: The dataset must strictly contain hardware attributes and retail pricing. Never include user personal data, customer reviews with identifiable names, or private credentials.
3. **Reproducibility**: If modifying `dataset_laptop_lengkap.csv`, document data cleaning scripts and sources in the PR description.

---

## 🔒 Security Vulnerability Reporting

If you identify a security issue, vulnerability, or secret leakage, **please do not open a public GitHub issue**. Contact the maintainer directly via email: `luthfirg2502@gmail.com`.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
