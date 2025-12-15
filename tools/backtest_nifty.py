import pandas as pd
from pathlib import Path
from strategies.sma import add_sma_rsi_signal


CSV_PATH = Path("data/history/NIFTY_5min.csv")


def backtest(df, lot_size=25):
    position = 0
    entry_price = 0.0
    realized_pnl = 0.0
    trades = 0

    for i in range(1, len(df)):
        row_prev = df.iloc[i-1]
        row = df.iloc[i]
        sig_prev = row_prev["signal"]
        sig = row["signal"]

        # generate trade on signal change
        if sig != sig_prev:
            price = row["close"]

            # close existing
            if position != 0:
                pnl = (price - entry_price) * position * lot_size
                realized_pnl += pnl
                trades += 1
                position = 0
                entry_price = 0.0

            # open new
            if sig == 1:
                position = 1
                entry_price = price
            elif sig == -1:
                position = -1
                entry_price = price

    return realized_pnl, trades


def main():
    if not CSV_PATH.exists():
        print("Missing file:", CSV_PATH)
        return

    df = pd.read_csv(CSV_PATH)
    print("Columns:", list(df.columns))

    # build datetime column from existing columns
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
    elif "date" in df.columns:
        df["datetime"] = pd.to_datetime(df["date"])
    elif "Date" in df.columns:
        df["datetime"] = pd.to_datetime(df["Date"])
    else:
        raise KeyError("No datetime/date column found")

    # adjust price/volume column names to match your CSV
    rename_map = {}
    for col in ["Open", "High", "Low", "Close", "Volume", "open", "high", "low", "close", "volume"]:
        if col in df.columns:
            rename_map[col] = col.lower()
    if rename_map:
        df = df.rename(columns=rename_map)

    # add SMA+RSI combined signal
    df = add_sma_rsi_signal(df)

    pnl, trades = backtest(df)

    print("=== NIFTY SMA+RSI Backtest ===")
    print("File:", CSV_PATH)
    print("Trades:", trades)
    print("Total P&L:", round(pnl, 2))


if __name__ == "__main__":
    main()
