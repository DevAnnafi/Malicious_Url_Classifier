# Malicious URL Detector

A machine-learning classifier that flags **malicious URLs** (phishing, malware, defacement) from benign ones using only features extractable from the URL string and its host — **no live network calls at inference time**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This project trains a supervised binary classifier to detect malicious URLs before a user clicks — the kind of model that sits inside an email gateway, proxy, or browser extension. It's built from the ground up: raw URLs in, engineered features out, honest evaluation throughout.

The emphasis is on **methodology, not just a score**. The hard part of security ML isn't calling `.fit()` — it's avoiding the subtle mistakes (data leakage, source artifacts, metric misuse) that make a model look great in a notebook and fail in production. Those are treated as first-class concerns here.

## What This Project Demonstrates

- **Feature engineering** from semi-structured text — lexical, host-based, and structural signals derived from exploratory analysis, not copied from a tutorial.
- **Leakage-safe methodology** — a single early train/test split, cross-validation for model selection, and a test set touched exactly once.
- **Metric literacy** — precision / recall / F1 / PR-AUC chosen deliberately for an imbalanced, asymmetric-cost problem, rather than headline accuracy.
- **Model comparison** across multiple families with documented tuning.
- **Error analysis** — characterizing *what* the model gets wrong and *why*.

## Tech Stack

- **Language:** Python 3.11
- **ML:** scikit-learn, (optionally) XGBoost / LightGBM
- **Data:** pandas, NumPy
- **Viz:** matplotlib, seaborn
- **Serving (optional):** FastAPI `/predict` endpoint

## Dataset

Trained on a labeled corpus of benign and malicious URLs (see `data/README.md` for the source and fetch instructions — raw data is git-ignored).

Class balance, label provenance, and known source biases are documented in the EDA notebook, because *where the labels came from* shapes what the model actually learns.

## Project Structure

```
malicious-url-classifier/
├── README.md
├── requirements.txt
├── features.py            # feature extraction module
├── notebooks/
│   ├── 01_eda.ipynb       # exploration + data-bias analysis
│   ├── 02_baseline.ipynb  # baseline model
│   ├── 03_models.ipynb    # model comparison + tuning
│   └── 04_eval.ipynb      # final evaluation + error analysis
└── data/                  # git-ignored; see data/README.md
```

## Getting Started

```bash
# 1. Clone
git clone https://github.com/DevAnnafi/malicious-url-classifier.git
cd malicious-url-classifier

# 2. Environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Fetch the dataset (see data/README.md), then run the notebooks in order.
```

## Methodology

| Concern | How it's handled |
|---|---|
| Data leakage | Split performed once, before any preprocessing; scalers/encoders fit on training data only. |
| Near-duplicate leakage | Split by domain (not raw URL) to prevent memorization of trivial variants. |
| Class imbalance | Reported with PR-AUC and per-class precision/recall; threshold chosen for the deployment context. |
| Model selection | Cross-validation on the training set only — the test set is evaluated exactly once. |

## Results

> _Populated as the model is built — numbers below are placeholders._

| Model | Precision | Recall | F1 | PR-AUC |
|---|---|---|---|---|
| Logistic Regression (baseline) | – | – | – | – |
| Random Forest | – | – | – | – |
| Gradient Boosting | – | – | – | – |

**Final model:** _TBD_
**Chosen operating threshold & rationale:** _TBD_

### Error Analysis

_Summary of characteristic false positives and false negatives, with representative examples and takeaways._

## Roadmap

- [ ] Model calibration + reliability curve
- [ ] FastAPI `/predict` endpoint
- [ ] Adversarial robustness: hand-crafted evasion URLs and analysis
- [ ] Feature-importance study (SHAP / permutation importance)

## Author

**Annafi Islam** — Cybersecurity Engineer
[GitHub](https://github.com/DevAnnafi) · [LinkedIn](https://linkedin.com/in/annafi-islam) · [Portfolio](https://annafiislam.com)

## License

Released under the MIT License. See `LICENSE` for details.
