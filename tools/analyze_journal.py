import pandas as pd
from pathlib import Path

JOURNAL_PATH = Path("data/paper-broker/trades_journal.csv")

def main():
    if not JOURNAL_PATH.exists():
        print("No journal file found:", JOURNAL_PATH)
        return

    df = pd.read_csv(JOURNAL_PATH)

    total_trades = len(df)
    buys = (df["side"] == "BUY").sum()
    sells = (df["side"] == "SELL").sum()

    # simple win = realized_pnl_after_trade > 0
    wins = (df["realized_pnl_after_trade"] > 0).sum()
    losses = (df["realized_pnl_after_trade"] < 0).sum()
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0.0

    total_pnl = df["realized_pnl_after_trade"].sum()

    print("=== Trading Journal Stats ===")
    print("File:", JOURNAL_PATH)
    print("Total trades:", total_trades)
    print("Buys:", buys, "Sells:", sells)
    print("Wins:", wins, "Losses:", losses)
    print("Win rate: {:.1f}%".format(win_rate))
    print("Total P&L:", round(total_pnl, 2))

if __name__ == "__main__":
    main()
