# <ins><span style="color:#1F4E79;">Evaluating the Predictive Power of U.S. Exports on Brent–WTI Spreads</span></ins>

---

# <ins><span style="color:#2F5597;">Executive Summary</span></ins>

Following the removal of the U.S. crude export ban in 2015, U.S. crude exports and export-related arbitrage became reliable leading indicators for movements in the Brent–WTI spread. However, their effectiveness as standalone predictors gradually weakened over time.

Under the current geopolitical regime, U.S. export flows alone appear insufficient to consistently explain spread movements. Instead, the Brent–WTI spread is increasingly influenced by a broader set of variables, including geopolitical risk premiums, freight rates, and global supply disruptions. As a result, U.S. exports should be analyzed alongside other macro and market-specific factors rather than used as an isolated trading signal.

---

# <ins><span style="color:#2F5597;">Background</span></ins>

Historically, the relationship between U.S. domestic crude inventories and the Brent–WTI spread has been highly volatile and inconsistent, limiting its usefulness as a reliable leading indicator for spread-trading strategies.

However, the removal of the U.S. crude export ban in December 2015 effectively ended major restrictions imposed under the Energy Policy and Conservation Act of 1975, structurally transforming the U.S. energy market.

As shown in Figure 1, the sharp increase in U.S. crude exports subsequently transformed the country from a relatively closed domestic system into a major global swing producer.

This project investigates whether the interaction between U.S. crude inventories and export flows can serve as a reliable explanatory indicator for the Brent–WTI spread, and whether these relationships can generate high conviction spread trading opportunities.

---

# <ins><span style="color:#2F5597;">Proposed Mechanism</span></ins>

Prior to the post-2015 export era, much of the crude produced during the U.S. shale boom remained effectively landlocked within the domestic market. Limited export capacity and infrastructure bottlenecks at Cushing contributed to persistent WTI discounts of roughly $20–30/bbl relative to Brent during periods of severe oversupply.

The removal of the U.S. crude export ban enabled producers and traders to arbitrage this pricing dislocation by exporting crude through the U.S. Gulf Coast into international markets priced against Brent-linked benchmarks. As domestic oversupply eased and U.S. crude became increasingly integrated with global seaborne markets, the Brent–WTI spread gradually narrowed.

Over time, significant investments in storage, pipeline, and export infrastructure, particularly across PADD 3 (the Gulf Coast), further strengthened the connection between domestic inventories and export capacity. As a result, inventory levels at Cushing and along the Gulf Coast, together with U.S. export volumes, may provide insight into periods when export arbitrage becomes economically attractive, contributing to a narrowing of the Brent–WTI spread.

---

# <ins><span style="color:#2F5597;">Methodology</span></ins>

## <ins><span style="color:#4472C4;">Data Acquisition</span></ins>

Weekly estimates for U.S. Crude Inventory (Cushing and PADD3, excluding the Strategic Petroleum Reserve) and Crude Export volumes were sourced via the EIA API v2. This ensures the model incorporates the latest available fundamental data through May 2026.

---

## <ins><span style="color:#4472C4;">Price Standardization</span></ins>

Friday closing prices for Brent and WTI were retrieved via the Yahoo Finance API. A weekly closing frequency was selected to filter out intraday "noise" and high-frequency volatility, focusing instead on structural price shifts.

---

## <ins><span style="color:#4472C4;">Spread</span></ins>

The Brent–WTI spread was calculated as:

```text
Brent Price - WTI Price
