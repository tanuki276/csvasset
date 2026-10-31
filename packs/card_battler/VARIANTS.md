# card_battler: v2 reference presets

カード戦闘用のエンジン非依存チューニング候補です。

`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。

既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は `../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。

## データ種類

| CSV | Archetypes |
|---|---|
| `variants/cards.csv` | strike, block, draw, burn, poison, heal, summon, discard, counter, exhaust |
| `variants/encounters.csv` | swarm, bruiser, sentinel, ritualist, duelist, summoner, elite, boss |
| `variants/events.csv` | shrine, merchant, healer, gamble, sacrifice, library, forge, treasure |
| `variants/relics.csv` | thorns, lifesteal, energy, draw, armor, discard, poison, summon |

実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から決定的に生成します。新規Packに画像・音声・完成マップは含みません。実ゲームでは採用したIDのパラメータを調整してください。
