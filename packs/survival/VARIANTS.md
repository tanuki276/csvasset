# survival: v2 reference presets

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/diseases.csv` | cold, fever, poisoning, infection, fatigue, dehydration, hypothermia, parasite |
| `variants/recipe_variants.csv` | tool, weapon, food, medicine, building_part, utility |
| `variants/resource_variants.csv` | wood, stone, fiber, metal, food, herb, fuel |
| `variants/structure_variants.csv` | wall, door, storage, workbench, turret, generator, bed |
| `variants/weather.csv` | clear, rain, blizzard, heatwave, sandstorm, fog, thunderstorm, drought |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
