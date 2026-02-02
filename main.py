import glob
import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

INPUT_DIR = "input"
OUTPUT_DIR = "output"


def ensure_dirs():
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def find_csv_files():
    files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    if not files:
        raise FileNotFoundError(f"CSVが見つかりません: {INPUT_DIR} に .csv を入れてください")
    return files


def load_and_concat_csv(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    # date を datetime に
    df_all["date"] = pd.to_datetime(df_all["date"], errors="coerce")
    df_all = df_all[df_all["date"].notna()]

    # 売上列を作る
    df_all["sales"] = df_all["price"] * df_all["quantity"]

    # 出力用に date を日付だけへ
    df_all["date"] = df_all["date"].dt.date

    return df_all


def summarize(df_all):
    daily = (
        df_all.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    product = (
        df_all.groupby("product", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    top5 = product.head(5)
    return daily, product, top5


def export_csv(df_all, daily, product, top5):
    df_all.to_csv(os.path.join(OUTPUT_DIR, "merged_sales.csv"), index=False)
    daily.to_csv(os.path.join(OUTPUT_DIR, "daily_sales.csv"), index=False)
    product.to_csv(os.path.join(OUTPUT_DIR, "product_sales.csv"), index=False)
    top5.to_csv(os.path.join(OUTPUT_DIR, "top5_products.csv"), index=False)


def export_graphs(daily, top5):
    # 日別売上（折れ線）
    daily_sorted = daily.sort_values("date")
    plt.figure(figsize=(10, 5))
    plt.plot(daily_sorted["date"], daily_sorted["sales"], marker="o")
    plt.title("Daily Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "daily_sales.png"), dpi=200)
    plt.close()

    # TOP5（棒）
    top5_sorted = top5.sort_values("sales", ascending=False)
    plt.figure(figsize=(10, 5))
    plt.bar(top5_sorted["product"], top5_sorted["sales"])
    plt.title("Top 5 Products by Sales")
    plt.xlabel("Product")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top5_products.png"), dpi=200)
    plt.close()


def main():
    ensure_dirs()

    files = find_csv_files()
    df_all = load_and_concat_csv(files)

    daily, product, top5 = summarize(df_all)

    export_csv(df_all, daily, product, top5)
    export_graphs(daily, top5)

    print("✅ 完了")
    print("処理CSV数:", len(files))
    print("対象行数:", len(df_all))
    print("出力先:", OUTPUT_DIR)
    print("生成ファイル: merged_sales.csv / daily_sales.csv / product_sales.csv / top5_products.csv / daily_sales.png / top5_products.png")


if __name__ == "__main__":
    main()