# Mass Generation Strategy

CSVASSETを数十万〜数百万件へ拡張するための設計です。

## 原則

「行数」ではなく **検証可能なパラメトリック・バリアント数** を増やします。

悪い大量生成:
- IDだけ違うコピー
- 制約なしの乱数
- 参照切れ
- 単位不明
- 過剰な極端値
- 再生成不能

CSVASSETの大量生成:
- curated archetype
- deterministic seed
- tier/grade curve
- bounded variation
- domain validator
- shard hash
- reproducible manifest

## 現在の生成面

| Pack | Dataset 1 | Dataset 2 | Dataset 3 |
|---|---|---|---|
| action_rpg | enemy_variants | item_variants | skill_variants |
| platformer | enemy_variants | hazard_variants | movement_variants |
| shmup | enemy_variants | weapon_variants | wave_variants |
| roguelike | item_variants | affix_variants | encounter_variants |
| tactics | unit_variants | ability_variants | terrain_variants |
| survival | resource_variants | recipe_variants | structure_variants |
| tower_defense | tower_variants | enemy_variants | wave_variants |
| racing | vehicle_variants | surface_variants | upgrade_variants |
| puzzle | level_variants | mechanic_variants | objective_variants |
| brawler | fighter_variants | move_variants | combo_variants |

デフォルトで各10,000行、合計300,000行です。

## Scaling

- 10,000 / dataset = 300,000 rows
- 20,000 / dataset = 600,000 rows
- 50,000 / dataset = 1,500,000 rows

1つの巨大CSVではなく、`shard_rows` 単位で分割します。

## Precision limits

生成データは「プロトタイプ・探索・AI学習用の高整合性チューニング候補」です。
最終的な商用品質のゲームバランスは、実際のゲームループ、操作感、DPS/TTK、勝率、プレイテスト結果に依存します。

したがって高精度とは、
- 構造が正しい
- 制約を満たす
- 値域が妥当
- 役割ごとのトレードオフがある
- 重複が少ない
- 再現・監査できる

という意味で定義します。実ゲームの最終バランスを無根拠に保証するものではありません。
