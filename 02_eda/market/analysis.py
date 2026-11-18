# # downloading data
# import pandas as pd
# import yfinance as yf

# gld = pd.read_csv("GLD_daily_2015_2026.csv")
# start = gld["Date"].min()
# end = (pd.to_datetime(gld["Date"].max())
#        + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

# for ticker in ["SLV", "UUP"]:
#     df = yf.download(
#         ticker, start=start, end=end,
#         auto_adjust=False, progress=False
#     )

#     if isinstance(df.columns, pd.MultiIndex):
#         df.columns = df.columns.get_level_values(0)

#     df = df.reset_index()
#     df = df[["Date", "Close", "High", "Low",
#              "Open", "Volume"]]

#     df.to_csv(f"{ticker}_daily_2015_2026.csv",
#               index=False)






# # # correlation

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# # 1. Load data
# gld = pd.read_csv("GLD_daily_2015_2026.csv")
# slv = pd.read_csv("SLV_daily_2015_2026.csv")
# uup = pd.read_csv("UUP_daily_2015_2026.csv")

# # 2. Keep Date and Close
# gld = gld[["Date", "Close"]].rename(columns={"Close": "GLD"})
# slv = slv[["Date", "Close"]].rename(columns={"Close": "SLV"})
# uup = uup[["Date", "Close"]].rename(columns={"Close": "UUP"})

# # 3. Merge by Date
# df = gld.merge(slv, on="Date").merge(uup, on="Date")

# # 4. Convert prices to daily returns
# returns = df[["GLD", "SLV", "UUP"]].pct_change().dropna()

# # 5. Correlation matrix
# corr = returns.corr()
# print(corr.round(3))

# # 6. Heatmap
# sns.heatmap(corr, annot=True, cmap="coolwarm",
#             vmin=-1, vmax=1, center=0, fmt=".2f")

# plt.title("Daily Return Correlation: GLD, SLV, UUP")
# plt.tight_layout()
# plt.savefig("correlation_heatmap.png", dpi=300)
# plt.show()


# # Lagged correlation: today's factors vs tomorrow's GLD return
# returns["GLD_next"] = returns["GLD"].shift(-1)

# lagged_corr = returns[
#     ["SLV", "UUP", "GLD_next"]
# ].corr()

# print("\nLagged Correlation:")
# print(lagged_corr["GLD_next"].round(3))

# # result: Lagged Correlation:
# SLV         0.003
# UUP         0.006
# GLD_next    1.000



import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, classification_report

# 1. Load data
gld = pd.read_csv("GLD_daily_2015_2026.csv")
slv = pd.read_csv("SLV_daily_2015_2026.csv")
uup = pd.read_csv("UUP_daily_2015_2026.csv")

# 2. Keep closing prices
gld = gld[["Date", "Close"]].rename(columns={"Close": "GLD"})
slv = slv[["Date", "Close"]].rename(columns={"Close": "SLV"})
uup = uup[["Date", "Close"]].rename(columns={"Close": "UUP"})

# 3. Merge and sort
df = gld.merge(slv, on="Date").merge(uup, on="Date")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# 4. Daily returns
for ticker in ["GLD", "SLV", "UUP"]:
    df[ticker + "_return"] = df[ticker].pct_change()

# 5. Create features: today and previous 4 trading days
for ticker in ["GLD", "SLV", "UUP"]:
    for lag in range(5):
        df[f"{ticker}_lag{lag}"] = df[ticker + "_return"].shift(lag)

# 6. Target: next-day GLD direction
df["next_return"] = df["GLD_return"].shift(-1)

# Drop missing feature and target rows
features_gld = [f"GLD_lag{i}" for i in range(5)]
features_all = [
    f"{ticker}_lag{i}"
    for ticker in ["GLD", "SLV", "UUP"]
    for i in range(5)
]

df = df.dropna(subset=features_all + ["next_return"])
df["target"] = (df["next_return"] > 0).astype(int)

# 7. Chronological train/test split (80/20)
split = int(len(df) * 0.8)
train = df.iloc[:split]
test = df.iloc[split:]

# 8. Train and evaluate both models
for name, features in [
    ("Model 1: GLD Only", features_gld),
    ("Model 2: GLD + SLV + UUP", features_all)
]:
    X_train = train[features]
    X_test = test[features]
    y_train = train["target"]
    y_test = test["target"]

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\n", name)
    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print(classification_report(y_test, predictions, zero_division=0))

# 9. Simple baseline: always predict UP
baseline = (test["target"] == 1).mean()
print("\nAlways Predict UP Accuracy:", round(baseline, 4))
print("Test period:", test["Date"].min().date(),
      "to", test["Date"].max().date())
