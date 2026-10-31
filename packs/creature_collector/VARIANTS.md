# creature_collector: v2 reference presets

育成・収集用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/creatures.csv` | fire, water, leaf, electric, stone, wind, ice, shadow, light, metal |
| `variants/habitats.csv` | forest, lake, mountain, desert, cave, tundra, coast, ruins |
| `variants/moves.csv` | strike, blast, drain, buff, debuff, heal, shield, trap |
| `variants/training.csv` | strength, agility, endurance, defense, focus, bonding, exploration, technique |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
