# stealth: v2 reference presets

ステルス用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/alert_states.csv` | idle, suspicious, searching, investigating, alerted, combat, lockdown, cooldown |
| `variants/gadgets.csv` | smoke, decoy, emp, lockpick, noise_dart, cloak, camera_mine, tripwire |
| `variants/guards.csv` | patrol, sentry, sniper, handler, camera, drone, elite, civilian |
| `variants/surfaces.csv` | carpet, wood, stone, metal, gravel, water, glass, grass |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
