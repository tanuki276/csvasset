# Balance Model

## Enemy tiers

敵の基準値はTierごとに指数成長させ、役割ごとの係数を乗算しています。

- HP base: `24 * 1.62^(tier-1)`
- ATK base: `5.5 * 1.50^(tier-1)`
- DEF base: `1.5 * 1.65^(tier-1)`
- XP base: `6 * 2.0^(tier-1)`

Bossは通常敵より大きなHP係数を持ち、XPはさらに4倍。属性耐性の極端さはBossだけ60%に圧縮して、単一属性での完封を避けています。

## Player progression

Lv1–30。基礎HPは線形、必要XPは `80 * level^1.55` を10刻みに丸めています。
装備Tierはおおむね次の到達域を想定します。

- Tier 1: Lv1–4
- Tier 2: Lv5–8
- Tier 3: Lv9–13
- Tier 4: Lv14–19
- Tier 5: Lv20+

## Damage mitigation

推奨式:

`reduction = min(max_damage_reduction, armor / (armor + armor_k))`

`armor_k=50`, `max_damage_reduction=0.75` は `data/system/game_constants.csv` にあります。

## Loot

`chance` は各エントリ独立抽選です。したがってテーブル全体で合計1.0にする必要はありません。
`chance=1.0` は確定ドロップです。

## Difficulty

難易度は基礎データを上書きせず乗算します。コンテンツ自体を難易度別CSVに複製しない方針です。
