# factory: v2 reference presets

工場自動化用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/belts.csv` | basic, fast, express, armored, underground, splitter, filter, stacker |
| `variants/deposits.csv` | iron, copper, coal, stone, oil, uranium, crystal, sulfur |
| `variants/machines.csv` | smelter, assembler, crusher, refinery, loom, press, centrifuge, recycler |
| `variants/research.csv` | logistics, metallurgy, automation, energy, chemistry, robotics, circuits, recycling |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
