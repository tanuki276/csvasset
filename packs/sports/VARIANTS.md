# sports: v2 reference presets

スポーツ用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/arenas.csv` | grass, turf, hardwood, clay, ice, sand, indoor, street |
| `variants/athletes.csv` | striker, defender, keeper, winger, playmaker, sprinter, anchor, allrounder |
| `variants/balls.csv` | football, basketball, volleyball, tennis, baseball, hockey, golf, rugby |
| `variants/training.csv` | sprint, endurance, shooting, passing, tackling, positioning, recovery, technique |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
