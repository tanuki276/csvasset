# city_builder: v2 reference presets

都市建設用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/buildings.csv` | residential, commercial, industrial, civic, hospital, school, park, station |
| `variants/policies.csv` | tax_relief, green_energy, tourism, education, healthcare, transit, zoning, recycling |
| `variants/roads.csv` | street, avenue, highway, alley, bridge, tunnel, tram, boulevard |
| `variants/utilities.csv` | solar, wind, coal, gas, hydro, battery, water, sewage |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
