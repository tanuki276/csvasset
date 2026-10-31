# 大量生成

30ジャンル、130種類、各10,000行で合計1,300,000行。種類別の役割定義は991個です。設定の重複を含むため「130万種類の固有アセット」とは呼びません。

```bash
python generator/generate_mass_assets.py --out generated
python generator/validate_generated.py generated
```

130万行の派生CSVはGitにはコミットしません。GitHub Actions `mass-generate-csvasset` を手動実行すると、seed・行数・shardサイズを指定して生成・全行検査し、`summary.json`・`manifest.csv`・`quality_report.csv` とCSV本体をArtifactに保存します。既定では約100MBの出力です。

任意規模:

```bash
python generator/generate_mass_assets.py \
  --rows-per-dataset 20000 --shard-rows 5000 --seed 2762026 --out generated-large
python generator/validate_generated.py generated-large
```

全種類の場合は2,600,000行。`--packs farming fishing` なら8種類だけを生成します。未知のPack名・100未満の行数・0以下のshardサイズは出力前に拒否します。既存フォルダの中身は削除せず、出力先が空でなければ終了します。

## 再現条件

同一バージョンのコード、seed、Pack、dataset、行番号を固定すると行内容は一致します。shardサイズや他Packの選択は値に影響しません。shard構成が変わるとファイル単位のSHA-256は変わります。

v2はv1と数値互換ではありません。生成器versionは `summary.json` に記録します。元の手書きPackは変更しません。型・単位・役割値・順序制約・計算式は [QUALITY_V2.md](QUALITY_V2.md) に記載します。

## 検査

検査はSHA-256、厳密な列、整数/真偽値、有限数、範囲、全種類・shard・行番号、Tier/Grade、役割、関連値、seedからの再生成を確認します。

品質レポートは `unique_configurations`, `duplicate_rows`, `unique_signature_ratio` を含みます。微小な`tuning_bias`やIDは多様性に数えません。ゲームとしてのバランスはプレイテストで決めてください。大量生成の検証メモリは1データセットずつ解放するため、全130万行を一括保持しません。
