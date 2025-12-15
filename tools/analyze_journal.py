import pandas as pd
from pathlib import Path

JOURNAL_PATH = Path("data/journal/trades_journal.csv")

def load_trades():
    if not JOURNAL_PATH.exists():
        print("No journal file found at:", JOURNAL_PATH)
        return None
    df = pd.read_csv(JOURNAL_PATH)
    return df

def compute_stats(df: pd.DataFrame):
    df = df.copy()
    df["pnl"] = df["realized_pnl_after_trade"].astype(float)


    total_trades = len(df)
    wins = (df["pnl"] > 0).sum()
    losses = (df["pnl"] < 0).sum()
    win_rate = wins / total_trades * 100 if total_trades else 0

    avg_win = df.loc[df["pnl"] > 0, "pnl"].mean() if wins else 0
    avg_loss = df.loc[df["pnl"] < 0, "pnl"].mean() if losses else 0

    cum_pnl = df["pnl"].cumsum()
    running_max = cum_pnl.cummax()
    drawdown = cum_pnl - running_max
    max_dd = drawdown.min()

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "avg_win": avg_win,
        "avg_loss": avg_loss,
        "total_pnl": df["pnl"].sum(),
        "max_drawdown": max_dd,
    }

def main():
    df = load_trades()
    if df is None:
        return
    stats = compute_stats(df)
    print("=== Paper Trading Stats ===")
    for k, v in stats.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
