# 売上CSV → 自動レポート（Sales CSV → Auto Report）

💡 **想定ユーザー**  
請求書・売上チェックで「税抜 / 税込」を確認しながら、  
CSV集計とグラフ作成を **Pythonで自動化したい人向け**

---

## 概要

売上CSV（`date, product, price, quantity`）を読み込み、  
**日別売上 / 商品別売上 / 売上TOP N** を集計し、  
CSVとグラフ（PNG）を自動生成する Python ツールです。

- `input/` にCSVを置いて実行するだけ
- `output/report_YYYYMMDD_HHMMSS/` に結果を自動出力
- 税抜 / 税込を `--tax-rate` で切り替え可能

---

## Before / After

- **Before**：Excelで売上集計・グラフ作成を手作業で実施  
- **After**：CSVを `input/` に置いて実行するだけで、  
  売上集計・税抜/税込切替・CSV/グラフ生成まで自動化

---

## フォルダ構成

```text
sales_auto_report/
├─ input/      # 売上CSVファイル（date, product, price, quantity）
├─ output/     # 集計結果（CSV / PNG）
├─ main.py     # メインスクリプト
├─ requirements.txt
├─ .gitignore
└─ README.md
```

---

## 出力内容（実行後）

本ツールを実行すると、`output/` 配下に  
**実行時刻を含むタイムスタンプ付きフォルダ**が自動で作成されます。

これにより、  
- 実行ごとの結果を上書きせず保存  
- 税率や条件を変えたレポートを後から比較  
が可能になります。

```text
output/
└─ report_YYYYMMDD_HHMMSS/
   ├─ merged_sales.csv
   ├─ daily_sales.csv
   ├─ product_sales.csv
   ├─ top5_products.csv
   ├─ daily_sales.png
   └─ top5_products.png
   ```

   - `merged_sales.csv`  
  入力された複数の売上CSVをすべて結合した元データです。  
  税抜売上（sales）・税込売上（sales_with_tax）を含みます。

- `daily_sales.csv`  
  日付ごとの売上合計を集計したCSVです。  
  日別の売上推移確認や、月次レポートの元データとして利用できます。

- `product_sales.csv`  
  商品ごとの売上合計を集計したCSVです。  
  売れ筋商品や主力商品の把握に利用できます。

- `top5_products.csv`  
  売上金額の高い商品を上位N件（デフォルト5件）抽出したCSVです。  
  `--top` オプションで件数を変更できます。

### グラフ出力内容（PNG）

- `daily_sales.png`  
  日別売上の推移を折れ線グラフで可視化します。  
  売上の増減やトレンドを直感的に確認できます。

- `top5_products.png`  
  売上上位商品の売上金額を棒グラフで表示します。  
  どの商品が売上に貢献しているかを一目で把握できます。

  ※ `--tax-rate` を指定した場合、  
　CSV・グラフの売上金額は **指定した税率を反映した金額** で出力されます。

例：
- `--tax-rate 0.0` → 税抜売上
- `--tax-rate 0.08` → 税込（8%）売上