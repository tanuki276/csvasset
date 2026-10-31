# naval: v2 reference presets

海戦用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/missions.csv` | convoy, patrol, blockade, rescue, interception, escort, reconnaissance, siege |
| `variants/sea_states.csv` | calm, breeze, chop, swell, rough, storm, fog, hurricane |
| `variants/vessels.csv` | patrol, corvette, frigate, destroyer, cruiser, carrier, submarine, battleship |
| `variants/weapons.csv` | cannon, torpedo, missile, depth_charge, mine, flak, railgun, rocket |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
