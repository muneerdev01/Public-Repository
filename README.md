# 🍳 Restaurant Customer Analytics & BI Dashboard

[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue)](https://www.python.org)
[![Streamlit App](https://static.streamlit.io/badge_穩定_light.svg)](https://share.streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, high-fidelity Business Intelligence (BI) dashboard engineered to analyze restaurant consumer dynamics, tipping elasticity, and transactional financial distributions. Built using a modern technical stack centered on Python, Streamlit, and Plotly, this system processes transactional matrices to extract actionable operational directives.

---

## 🎯 Core Features & Analytical Depth

* **Financial Revenue Distribution Layout:** Interactive high-density probability plots mapping total invoice values and gratuity volume densities.
* **Linear Regression Analysis (OLS):** Real-time Ordinary Least Squares trendlines exploring the correlation between party covers, baseline costs, and tipping behaviors.
* **Inferential Statistical Engine:** Built-in biostatistics core utilizing **Welch's T-Test** via `scipy.stats` to mathematically validate revenue shifts between operational windows (Lunch vs. Dinner).
* **Multi-Dimensional Heatmap:** Full Pearson Correlation Matrix evaluating hidden dependencies between numerical feature components.
* **Granular Ad-Hoc Explorer:** Operational sub-dataset engine providing randomized arrays or filtered data transmission blocks for strategic auditing.
* **Premium Slate Dark Architecture:** Modern responsive UI built using custom structural CSS overrides mimicking professional engineering platforms.

---

## 📊 Dataset Integrity & Statistical Rules

The underlying pipeline runs on a high-fidelity synthetic architecture (`restaurant_customer_dataset.csv`) enforcing strict data integrity rules rather than uniform randomness:
* **Total Bill Component:** Driven linearly by party size, dinner-hour weightings, and weekend surges.
* **Gratuity Engine:** Bound strictly to linear bill percentages (~16.5%) and dynamically suppressed/boosted by micro-customer sentiment ratings (1-5 Stars).
* **Temporal Realism:** Weekends shift density toward Dinner frames, while working weekdays naturally default toward corporate Lunch covers.

---

## 🛠️ Tech Stack & Dependencies

The system is fully validated to work with the following strict production version layers:

* **Streamlit** (`v1.35.0`) - Reactive Frontend Presentation Layer
* **Pandas** (`v2.2.2`) - High-Performance Data Manipulation Framework
* **Numpy** (`v1.26.4`) - Multi-dimensional Array Vectorization Core
* **Plotly** (`v5.22.0`) - Dynamic Canvas Visualization Engine
* **SciPy** (`v1.13.1`) - Scientific Computing & Mathematical Hypothesis Tests
* **Statsmodels** (`v0.14.2`) - Advanced Ordinary Least Squares (OLS) Engine

---

## 🚀 Local Deployment Setup

Follow these exact steps to launch the engine within your local development environment:

### 1. Clone the Architecture
```bash
git clone https://github.com/YOUR_USERNAME/restaurant-customer-analytics.git
cd restaurant-customer-analytics
