# ML Trading Strategy: Rule-Based vs. Learning-Based Approaches

## 📌 Abstract

The objective of this project is to implement and compare two different trading strategies:

- A **manual strategy** that generates trading signals using predefined rules based on technical indicators.
- A **strategy learner**, which uses a **bagged Random Tree Learner** to learn an optimal trading policy from historical data.

Both strategies are evaluated on performance metrics such as cumulative return, Sharpe ratio, and daily return. The project is part of the final assignment for the OMSCS course *Machine Learning for Trading* (CS 7646).

---

## 📈 Technical Indicators Implemented

The following technical indicators are used to guide trading decisions in both manual and machine learning strategies:

### 📊 Bollinger Bands Percentage (BBP)

Bollinger Bands consist of:
- Simple Moving Average (SMA)
- Upper Band = SMA + 2 × σ
- Lower Band = SMA − 2 × σ

**BBP formula:**
