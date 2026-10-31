# Mass CSVASSET Generator

`generate_mass_assets.py` は、複数ジャンル向けの高ボリュームCSVアセットを決定的に生成します。

## Default target

- 10 packs
- 30 datasets
- 10,000 rows / dataset
- 300,000 total asset rows
- 5,000 rows / shard
- seed: `2762026`

## Generate

```bash
python generator/generate_mass_assets.py
python generator/validate_generated.py generated
```

任意件数:

```bash
python generator/generate_mass_assets.py \
  --rows-per-dataset 20000 \
  --shard-rows 5000 \
  --seed 2762026
```

20,000行/データセットなら合計600,000行になります。

## Quality model

この生成器は「意味のない完全乱数」を作りません。各行は以下の制約を持ちます。

1. **Archetype**: ジャンル固有の役割から生成。
2. **Tier curve**: Tier 1–20の成長曲線。
3. **Grade**: 0–4の品質段階。
4. **Trade-off**: 速度・火力・耐久・コストなどをアーキタイプごとに調整。
5. **Bounded jitter**: 小さな決定的変動だけを加え、極端値を防止。
6. **Explicit units**: `_sec`, `_ms`, `_px_sec`, `_tiles`, `_kph`, `_mult` 等。
7. **Stable IDs**: pack名を含む一意ID。
8. **Deterministic seed**: 同じseed/件数/コードから同じCSVとSHA-256を再現。

## Validation

`validate_generated.py` は全行を読み、以下を検証します。

- manifestのSHA-256
- shard / dataset / global row count
- グローバルID重複
- namespace
- Tier / Grade範囲
- NaN / infinity
- 主要値の範囲
- min/max整合性
- 20 Tier / 5 Gradeのcoverage
- archetype diversity
- tuning signatureの重複率
- datasetごとの論理制約

検証結果は `generated/quality_report.csv` に保存されます。

## Generated data policy

巨大な派生CSVは `main` に直接コミットしません。ソースコードと規約をGit管理し、GitHub Actionsで生成物をArtifactとして作ります。これにより履歴肥大化を避けつつ、seedから完全再現できます。
