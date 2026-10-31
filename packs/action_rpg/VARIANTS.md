# action_rpg: v2 reference presets

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/companions.csv` | healer, guardian, archer, mage, wolf, golem, sprite, falcon |
| `variants/enemy_variants.csv` | brute, skirmisher, ranger, caster, tank, assassin |
| `variants/item_variants.csv` | sword, axe, bow, staff, armor, ring, potion |
| `variants/skill_variants.csv` | melee, projectile, aoe, dash, heal, control |
| `variants/weather.csv` | clear, rain, snow, fog, storm, heat, ash, aurora |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
