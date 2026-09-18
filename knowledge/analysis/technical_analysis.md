---

title: Technical Analysis
category: Investing
difficulty: Beginner
tags:

* technical analysis
* technical indicators
* momentum
* trend
* moving average
* volatility
* price action
* trading
* stocks
* machine learning

---

# Technical Analysis

## Overview

Technical analysis is an approach to analysing financial markets using historical price, volume, and market data.

Instead of primarily examining a company's financial statements, technical analysis focuses on patterns and measurements derived from market data.

Common technical-analysis concepts include:

* Price trends.
* Momentum.
* Moving averages.
* Volatility.
* Trading volume.
* Support and resistance.
* Relative performance.

Technical analysis is commonly used by traders and investors to understand market behaviour and identify potential opportunities or risks.

However, historical market patterns do not guarantee future performance.

---

# How Technical Analysis Works

Technical analysis typically starts with historical market data such as:

* Open price.
* High price.
* Low price.
* Closing price.
* Trading volume.

Indicators can then be calculated from this information.

For example, an investor might calculate a moving average from historical closing prices to understand the general direction of a stock's price.

Multiple indicators can be combined to provide a broader view of market behaviour.

---

# Price and Return

A stock's return measures how its price changes over a particular period.

A simple daily return can be calculated as:

**Return = (Current Price ÷ Previous Price) - 1**

For example, if a stock moves from $100 to $105:

**Return = (105 ÷ 100) - 1 = 0.05**

The return is therefore **5%**.

Returns can be calculated over different periods, such as:

* 1 day.
* 3 days.
* 5 days.
* 10 days.
* 20 days.
* 1 year.

---

# Moving Averages

A moving average calculates the average price over a specified number of previous observations.

For example, a 20-day moving average uses the previous 20 trading days.

Moving averages can help identify longer-term price trends by reducing the effect of individual daily price movements.

Common moving averages include:

* 10-day moving average.
* 20-day moving average.
* 50-day moving average.
* 100-day moving average.
* 200-day moving average.

---

# Moving Average Example

Suppose a stock has closing prices of:

$10, $12, $11, $13, $14

A five-day simple moving average would be:

**($10 + $12 + $11 + $13 + $14) ÷ 5 = $12**

As new prices become available, the oldest price is removed from the calculation and the newest price is included.

This is why it is called a **moving** average.

---

# Trend

A trend describes the general direction of an asset's price.

A stock may generally be:

* Trending upward.
* Trending downward.
* Moving sideways.

Technical indicators can be used to estimate the strength and direction of a trend.

---

# Trend Strength

One way to measure trend strength is to compare shorter-term and longer-term moving averages.

For example:

**Trend Strength = (MA10 - MA50) ÷ MA50**

A positive value indicates that the shorter-term moving average is above the longer-term moving average.

A negative value indicates that the shorter-term moving average is below the longer-term moving average.

This type of measurement can provide information about the stock's recent trend.

It does not guarantee that the trend will continue.

---

# Momentum

Momentum measures the rate at which an asset's price has been changing.

A simple momentum calculation can compare the current price with its price several periods earlier.

For example:

**Momentum = Current Price - Price n periods ago**

Positive momentum indicates that the current price is above the earlier reference price.

Negative momentum indicates that the current price is below the earlier reference price.

---

# Momentum Acceleration

Momentum acceleration attempts to measure whether momentum itself is increasing or decreasing.

For example, if a stock's recent returns are becoming increasingly positive, momentum acceleration may become positive.

This can provide additional information beyond simply measuring whether momentum is currently positive or negative.

---

# Volatility

Volatility measures the variability of an asset's returns.

A common approach is to calculate the standard deviation of returns over a particular period.

For example, your Financial Advisor Bot uses:

**Vol_20**

which represents a 20-period volatility measurement.

Higher volatility generally indicates that recent returns have varied more significantly.

Volatility does not indicate the direction of future price movement.

---

# Relative Performance

Technical analysis can also compare one stock's performance with other stocks or a broader market.

For example:

**Relative Return = Stock Return - Benchmark Return**

A positive relative return means the stock has outperformed the selected benchmark over the measurement period.

A negative relative return means the stock has underperformed the benchmark.

---

# Relative Momentum

Relative momentum compares the momentum of one stock with another stock, group, or benchmark.

This can help identify securities that have demonstrated stronger or weaker recent momentum relative to their comparison group.

Relative measurements can be useful when evaluating a large universe of stocks.

---

# Volume

Trading volume represents the number of shares or contracts traded during a particular period.

Changes in volume can provide additional information about market activity.

For example:

* Increasing price + increasing volume can indicate strong market participation.
* Increasing price + decreasing volume may indicate weaker participation.

However, volume should not be interpreted in isolation.

---

# Volume Z-Score

A Z-score can be used to measure how unusual the current volume is relative to its historical behaviour.

A simplified Z-score is:

**Z = (Current Value - Mean) ÷ Standard Deviation**

A high positive volume Z-score means current trading volume is significantly above its historical average.

A negative value means volume is below its historical average.

---

# Maximum Drawdown

Maximum drawdown measures the largest decline from a previous portfolio or asset peak to a subsequent low over a particular period.

For example:

A stock rises from $100 to $120 and later falls to $90.

The drawdown from the $120 peak is:

**($90 - $120) ÷ $120 = -25%**

Maximum drawdown is useful for understanding historical downside behaviour.

It does not predict the maximum loss that will occur in the future.

---

# Relative Strength

Relative strength compares the performance of an asset with another asset or benchmark.

It should not be confused with the **Relative Strength Index (RSI)**.

Relative strength is generally about comparative performance, while RSI is a specific momentum oscillator.

---

# Technical Indicators in Machine Learning

Technical indicators can also be used as features in machine-learning models.

Instead of manually interpreting an indicator such as momentum as a BUY or SELL signal, a machine-learning model can use multiple features simultaneously.

For example:

**Features → Machine Learning Model → Predicted Return → Ranking → Signal**

This allows the model to identify relationships between historical market characteristics and future returns.

---

# Technical Features Used by the Financial Advisor Bot

Your current model uses several technical and market-derived features.

## Return_1d

Measures the stock's one-day return.

It provides information about very recent price movement.

---

## Return_5d

Measures the stock's return over approximately five trading days.

This is particularly relevant because the model predicts approximately five-day future returns.

---

## Vol_20

Measures volatility over a 20-period window.

It provides information about recent variability in the stock's returns.

---

## Trend_Strength

Measures the relationship between short-term and longer-term moving averages.

It provides information about the current price trend.

---

## Momentum_Accel

Measures changes in momentum.

It attempts to identify whether recent momentum is strengthening or weakening.

---

## Volume_Z

Measures how unusual current trading volume is compared with its historical behaviour.

---

## Rolling_MaxDD

Measures historical downside from a recent peak.

It provides information about recent drawdown behaviour.

---

## Relative_Return

Measures the stock's return relative to another comparison measure.

This helps identify stocks that are outperforming or underperforming their peers or benchmark.

---

## Relative_Momentum

Measures momentum relative to other stocks or a benchmark.

---

## MomentumRiskAdj

Combines momentum information with a risk consideration.

This allows the model to distinguish between strong momentum with relatively different risk characteristics.

---

# Why Multiple Indicators Are Used

A single technical indicator can provide incomplete information.

For example:

**Momentum is positive**

does not necessarily mean:

**The stock will continue rising.**

The stock could have positive momentum while simultaneously experiencing:

* High volatility.
* Weak relative performance.
* Large drawdowns.
* Unusual trading volume.

Using multiple features allows the model to consider several aspects of market behaviour at the same time.

---

# Technical Analysis vs Fundamental Analysis

Technical and fundamental analysis approach investments differently.

| Technical Analysis     | Fundamental Analysis          |
| ---------------------- | ----------------------------- |
| Historical market data | Company financial information |
| Price                  | Revenue                       |
| Returns                | Earnings                      |
| Volume                 | Cash flow                     |
| Momentum               | Debt                          |
| Volatility             | Profitability                 |
| Trends                 | Valuation                     |
| Market behaviour       | Business performance          |

These approaches can also be combined.

---

# Technical Analysis and Machine Learning

Traditional technical analysis often involves rules such as:

> Buy when the moving average crosses above another moving average.

Machine learning can take a different approach.

Instead of manually assigning a fixed rule, a model can learn relationships from historical data.

For your Financial Advisor Bot:

**Historical Market Data**

↓

**Feature Engineering**

↓

**Technical / Market Features**

↓

**LightGBM Regression Model**

↓

**Predicted 5-Day Return**

↓

**Cross-Sectional Ranking**

↓

**BUY / HOLD / SELL**

The model therefore uses technical features as inputs rather than simply treating one indicator as a trading rule.

---

# Important Limitation

Machine learning does not eliminate the limitations of technical analysis.

Historical relationships may change because:

* Market conditions change.
* Investor behaviour changes.
* Economic conditions change.
* New information becomes available.
* Relationships between variables can weaken.
* Extreme events can occur.

A model that performs well historically may therefore perform differently in future markets.

This is why walk-forward validation and out-of-sample testing are important.

---

# Technical Analysis and the Financial Advisor Bot

The chatbot's recommendations should be interpreted as **model-based predictions**, not guarantees.

For example:

**Recommendation: BUY**

**Expected 5-Day Return: +0.86%**

This means the model estimates that the stock has a positive expected short-term return relative to the model's prediction framework.

It does not mean that:

* The stock will definitely rise.
* The investor will earn 0.86%.
* The prediction is guaranteed.
* The stock is suitable for every investor.

The model's prediction should therefore be presented alongside appropriate risk context.

---

# Common Misconceptions

### Technical analysis predicts the future perfectly.

False.

Technical analysis uses historical information to identify patterns and relationships. It cannot guarantee future prices.

---

### One indicator is enough to make an investment decision.

Not necessarily.

Indicators can provide different and sometimes conflicting information.

---

### Positive momentum guarantees a price increase.

False.

Momentum can weaken or reverse.

---

### High trading volume means the stock will rise.

False.

High volume indicates increased trading activity but does not determine direction.

---

### Machine learning makes technical analysis reliable.

False.

Machine learning can identify patterns in historical data, but those patterns may not persist in future markets.

---

# Best Practices

When using technical analysis:

* Use multiple indicators rather than relying on one.
* Understand what each indicator measures.
* Avoid interpreting historical patterns as guarantees.
* Consider market conditions.
* Account for transaction costs where appropriate.
* Validate strategies using out-of-sample data.
* Avoid overfitting historical data.
* Combine technical information with appropriate risk management.

---

# Frequently Asked Questions

### What is technical analysis?

Technical analysis is the study of historical market data such as price and volume to identify trends, patterns, momentum, and other characteristics.

---

### Is technical analysis accurate?

Technical analysis can provide useful information, but it cannot guarantee future investment returns.

---

### What are common technical indicators?

Common indicators include:

* Moving averages.
* Momentum.
* RSI.
* MACD.
* Bollinger Bands.
* Volatility measures.
* Volume indicators.

---

### What is momentum?

Momentum measures the direction or rate of recent price movement.

---

### What is volatility?

Volatility measures the variability of returns.

---

### What is a moving average?

A moving average calculates the average price over a rolling historical period.

---

### Does the Financial Advisor Bot use technical analysis?

Yes.

The model uses several market-derived features, including returns, volatility, trend strength, momentum, volume, drawdown, and relative-performance features.

---

### Does a technical BUY signal guarantee a profit?

No.

The chatbot's BUY signal is a model prediction and does not guarantee that the stock will increase in price.

---

# Chatbot Keywords

Technical Analysis

What is technical analysis

Technical Indicators

Technical Indicator

Stock Indicators

Moving Average

MA

Momentum

Momentum Trading

Momentum Acceleration

Trend

Trend Strength

Volatility

Stock Volatility

Trading Volume

Volume Z Score

Relative Return

Relative Momentum

Maximum Drawdown

Drawdown

Price Trend

Technical Analysis and Machine Learning

Technical Analysis and AI

---

# Related Topics

* Stocks
* Market Volatility
* Risk Management
* Diversification
* Long-Term Investing
* Machine Learning
* Investing Basics
* Portfolio Management

---

# References

U.S. Securities and Exchange Commission (Investor.gov). *Investing Basics*
https://www.investor.gov/introduction-investing

FINRA. *Technical Analysis*
https://www.finra.org/investors

CFA Institute. *Technical Analysis*
https://www.cfainstitute.org/

Investopedia. *Technical Analysis*
https://www.investopedia.com/terms/t/technicalanalysis.asp
