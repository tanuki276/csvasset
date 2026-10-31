# tower_defense: v2 reference presets

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/enemy_variants.csv` | grunt, fast, tank, shield, flying, boss |
| `variants/status_effects.csv` | slow, burn, poison, stun, armor_break, vulnerability, freeze, mark |
| `variants/targeting.csv` | first, last, strongest, weakest, nearest, fastest, armored, flying |
| `variants/tower_variants.csv` | cannon, rapid, sniper, splash, slow, beam |
| `variants/wave_variants.csv` | standard, rush, tank_push, air, mixed, boss |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
