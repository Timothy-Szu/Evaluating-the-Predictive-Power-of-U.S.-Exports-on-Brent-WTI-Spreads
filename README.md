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



## <ins><span style="color:#4472C4;">Spread</span></ins>

The Brent–WTI spread was calculated as:

```text
Brent Price - WTI Price
```


## <ins><span style="color:#4472C4;">Temporal Alignment</span></ins>

A 13-week lag was applied to inventory data based on the hypothesis that inventory imbalances may transmit gradually into export flows and relative crude pricing dynamics. This lag is intended to account for the delayed adjustment process between domestic oversupply conditions, export responses, and the eventual impact on the Brent–WTI spread.



## <ins><span style="color:#4472C4;">Export Capacity Proxy</span></ins>

Effective export capacity was proxied using the 52-week rolling maximum of U.S. crude export volumes. This approach assumes that historical peak export levels provide a reasonable approximation of prevailing export infrastructure and logistical capacity over time.

---

## <ins><span style="color:#4472C4;">Time Lag</span></ins>

Physical preparation, scheduling, and logistical arrangements required to export crude oil through U.S. Gulf Coast terminals such as Corpus Christi and Houston involve meaningful operational delays. To account for this transmission lag, the analysis incorporates lagged inventory variables when evaluating the relationship between U.S. crude inventories and the Brent–WTI spread.

The analysis first measures the contemporaneous correlation between inventory levels and the Brent–WTI spread using a 0-week lag before progressively extending the lag horizon to evaluate how the relationship evolves over time.

As shown in Figure 2, the resulting correlation profiles exhibit an inverted U-shaped pattern, with Gulf Coast inventories (PADD 3) displaying materially stronger correlations with the Brent–WTI spread than inventories at Cushing. This result is economically intuitive, as the Gulf Coast serves as the primary export corridor for U.S. crude oil exports.

The negative correlation is consistent with the hypothesis that rising Gulf Coast inventories increase export availability, contributing to a narrowing of the Brent–WTI spread.

At a 0-week lag, the correlation between Gulf Coast inventories and the spread is approximately r = -0.400. The magnitude of the relationship strengthens as the lag horizon increases, reaching a peak correlation of approximately r = -0.535 at a 13-week lag. This pattern suggests that inventory imbalances may influence export flows and spread dynamics with a substantial transmission delay.

Accordingly, subsequent analysis focuses on the 11–14 week lag window in order to better capture the delayed adjustment process embedded within the U.S. export infrastructure and logistics network.

---

## <ins><span style="color:#2F5597;">Export Capacity</span></ins>

As the EIA dataset does not provide a direct measure of U.S. crude export capacity, a proxy variable is constructed to estimate effective system capacity. Specifically, export capacity is approximated using a 52-week rolling maximum of observed export volumes.

By using the highest recorded export volume over the previous 52 weeks, the model generates a dynamic estimate of the system’s demonstrated operational export capacity. This approach allows the analysis to account for the substantial expansion in U.S. export infrastructure between 2017 and 2026, including pipeline, storage, and terminal developments along the Gulf Coast.

Export utilization for each week is then calculated as:

We then use varying levels of export utilization and lag to further our analysis of the relationship between Gulf inventories and the Brent–WTI spread. Our findings are presented below.

Figure 3 presents a two-dimensional heatmap showing the sensitivity analysis of the correlation between inventory levels and the Brent–WTI spread across different export utilization rates and lag durations.

We observe a substantial strengthening in the relationship between inventories and the Brent–WTI spread as export utilization approaches 100% and the lag horizon approaches 11 weeks. The strongest relationship is observed when export utilization exceeds 95% with an 11-week lag, where the correlation reaches approximately r = -0.690.

This result is consistent with the hypothesis that inventory levels become more relevant to spread pricing when export infrastructure is operating near effective capacity. High export utilization suggests that elevated Gulf Coast inventories are actively being transmitted into global seaborne markets, contributing to a narrowing of the Brent–WTI spread.

---

## <ins><span style="color:#2F5597;">Inventory Normalization and Strategy Construction</span></ins>

As crude inventories exhibit strong cyclical and seasonal behavior, the analysis employs a dynamic inventory z-score framework.

The inventory z-score is calculated using a 52-week rolling window, where:

Z = (X - μ) / σ

with the rolling mean μ and rolling standard deviation σ computed over the previous 52 weeks. This approach standardizes inventory levels relative to their recent historical range while adapting to changing market conditions over time. High inventory conditions are defined as periods where the inventory z-score exceeds 1, while low inventory conditions are defined as periods where the z-score falls below -1. The strategy is back-tested beginning from January 2016, corresponding to the start of the post-export-ban regime.


## <ins><span style="color:#5B9BD5;">Trading Rules</span></ins>

1. A long Brent–WTI spread position is initiated when:

   - Inventory z-scores were above 1 for three consecutive weeks 13 weeks prior
   - Current export utilization exceeds the selected threshold

2. A short Brent–WTI spread position is initiated when:

   - Inventory z-scores were below -1 for three consecutive weeks 13 weeks prior
   - Current export utilization exceeds the selected threshold

3. No positions are initiated when export utilization remains below the selected threshold.

4. The framework is tested across multiple export utilization thresholds, including 70%, 80%, 90%, and 95%.



## <ins><span style="color:#2F5597;">Back-Test Results</span></ins>

As illustrated in Figure 4, strategy volatility declines as the export utilization threshold increases. Lower thresholds such as 70% and 80% exhibit significantly larger swings in performance, with both higher peaks and deeper drawdowns relative to the 90% and 95% threshold strategies. As of 17 May 2026, only the 70% threshold strategy has maintained positive cumulative PnL, although returns remained modest at around 6 USD per spread, driven primarily by large historical successes which offset poor performances in more recent times.

Breaking the results into subperiods reveals important regime-dependent behavior. During the initial post-export-ban period from 2016 to 2020, the strategy performed relatively well across all thresholds, generating steadily rising PnL as U.S. crude exports became increasingly integrated into global crude markets. Performance stagnated during the COVID-19 period between 2020 and 2021, when the collapse in global oil demand sharply reduced export activity and likely suppressed export utilization, resulting in fewer trading signals.

A major structural shift emerged following Russian invasion of Ukraine in February 2022. Subsequent sanctions on Russian crude exports and the reorganization of global oil trade flows increased the geopolitical sensitivity of Brent pricing. Under this new market regime, the Brent benchmark appeared to embed a more persistent geopolitical risk premium, weakening the historical relationship between U.S. export dynamics and the Brent–WTI spread.

As a result, strategy performance deteriorated sharply in the months following the opening salvo of the Ukraine War in 2022 across all thresholds, with cumulative PnL flattening or turning negative in subsequent years. As for 2026, till date no trades have been triggered.

---

## <ins><span style="color:#C00000;">Limitations</span></ins>

1. Given that the post-export-ban regime begins only in 2016, the available sample size is relatively limited for robust statistical inference. This constraint becomes even more pronounced when conditioning on export utilization thresholds above 95%, where the effective sample size falls to approximately 51 observations using an 11-week lag. Although hypothesis testing produced a statistically significant result (p < 0.001), allowing us to reject the null hypothesis of no significant correlation, the small sample size remains a key limitation in the back-testing analysis.
The issue is further compounded by the requirement of three consecutive weeks of high or low inventory levels as a trade selection criterion, which further reduces the number of observations. Consequently, the analysis may not fully capture the long-run relationship between U.S. inventories and the Brent–WTI spread across different market regimes.


2. Export capacity is proxied using a 52-week rolling maximum of observed export volumes. While this provides a dynamic estimate of effective system capacity, the approach may introduce measurement bias, particularly during periods when new peak export levels are reached near the end of the rolling window. As a result, the proxy may lag changes in underlying infrastructure capacity and may partially reflect contemporaneous market conditions, creating a degree of endogeneity in the measure.
3. 

4. Our analysis examines the relationship between inventory levels and the Brent–WTI spread across different export regimes. While the results indicate a statistically significant correlation, they do not establish causality or definitively confirm the proposed mechanism whereby export dynamics drive spread narrowing. Reverse causality may also be plausible, in which a narrower Brent–WTI spread incentivizes higher export activity. Nevertheless, the primary objective of the study is to evaluate the predictive usefulness of export-related variables, for which correlation may still provide economically meaningful signals.


5. The analysis does not explicitly incorporate freight costs or transatlantic arbitrage dynamics, both of which have become increasingly important drivers of the Brent–WTI spread in the post-2022 market structure. In particular, changes in shipping costs, refinery margins, and crude quality differentials may influence the spread independently of U.S. inventory conditions and export flows.

---

## <ins><span style="color:#2F5597;">Conclusion</span></ins>

Overall, the results suggest that an export-centric framework can partially explain movements in the Brent–WTI spread, particularly in the early years following the 2015 export ban removal, when arbitrage between U.S. domestic crude and seaborne markets was a key driver of price convergence. However, in the modern market environment, this framework becomes less effective in capturing the full set of forces influencing the spread. The Brent–WTI relationship appears to be increasingly shaped by additional structural drivers, including a persistent geopolitical risk premium embedded in Brent and broader disruptions to global crude trade flows.

Overall, the findings suggest that U.S. crude exports alone are no longer sufficient to explain movements in the Brent–WTI spread and must instead be considered alongside geopolitical factors, freight dynamics, and global supply shocks.
