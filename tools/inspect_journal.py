import pandas as pd

df = pd.read_csv("data/journal/trades_journal.csv")
print(df.columns.tolist())
print(df.head())
