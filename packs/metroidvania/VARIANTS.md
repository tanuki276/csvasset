# metroidvania: v2 reference presets

探索アクション用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/abilities.csv` | double_jump, wall_jump, dash, grapple, swim, glide, morph, charge |
| `variants/gates.csv` | high_ledge, narrow_tunnel, water, heat, dark, breakable, grapple_point, wind |
| `variants/rooms.csv` | shaft, corridor, hub, arena, save_room, secret, traversal, boss |
| `variants/upgrades.csv` | health, energy, missile, armor, speed, map, radar, recovery |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
