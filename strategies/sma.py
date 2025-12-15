import pandas as pd

def add_sma_signals(df: pd.DataFrame, fast: int = 10, slow: int = 20) -> pd.DataFrame:
    df = df.copy()
    df["sma_fast"] = df["close"].rolling(fast).mean()
    df["sma_slow"] = df["close"].rolling(slow).mean()
    df["signal_sma"] = 0
    df.loc[df["sma_fast"] > df["sma_slow"], "signal_sma"] = 1
    df.loc[df["sma_fast"] < df["sma_slow"], "signal_sma"] = -1
    return df

def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df = df.copy()
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def add_sma_rsi_signal(
    df: pd.DataFrame,
    fast: int = 10,
    slow: int = 20,
    rsi_period: int = 14,
    rsi_buy: int = 55,
    rsi_sell: int = 45,
) -> pd.DataFrame:
    df = add_sma_signals(df, fast=fast, slow=slow)
    df = add_rsi(df, period=rsi_period)

    df["signal"] = 0
    df.loc[(df["signal_sma"] == 1) & (df["rsi"] >= rsi_buy), "signal"] = 1
    df.loc[(df["signal_sma"] == -1) & (df["rsi"] <= rsi_sell), "signal"] = -1
    return df
