# CSVASSET

**複数ジャンルの2Dゲームで再利用できる、CSVベースのゲームデータ・アセットライブラリ**です。

このリポジトリは「1本のゲームをCSV化したもの」ではありません。`shared/` の共通語彙と `packs/` のジャンル別データパックを組み合わせて使います。

## 設計原則

1. **Pack-first** — 各ジャンルは独立スキーマを持ち、不要な概念を強制しない。
2. **Composable** — 共通アセット、タグ、難易度、入力などは `shared/` から任意利用。
3. **Stable IDs** — ファイル名ではなく文字列IDを公開APIとして扱う。
4. **Explicit units** — sec / ms / px / tile / multiplier / chance を明示。
5. **Engine-neutral** — Phaser / Godot / Unity / 自作エンジンに依存しない。
6. **Validation-first** — 構造・主キー・参照・基本レンジをCI検証。
7. **Examples are data** — 空テンプレートではなく調整可能な実データ例を同梱。

## Packs

| Pack | 想定ジャンル | 主なデータ |
|---|---|---|
| `action_rpg` | 2D ARPG / Zelda-like | 敵、戦闘、装備、クエスト、NPC、マップ、クラフト |
| `platformer` | 横スクロール / Metroidvania | 移動、敵、ハザード、収集物、チェックポイント |
| `shmup` | 縦/横STG | 自機、武器、弾、敵、ウェーブ、スコア |
| `roguelike` | ローグライク / ローグライト | 部屋、遭遇、アイテムプール、Affix、メタ進行 |
| `tactics` | SRPG / Grid tactics | ユニット、クラス、地形、アビリティ、勝利条件 |
| `survival` | Survival / Crafting | 資源、Needs、レシピ、建築、スポーン、時間帯 |
| `tower_defense` | Tower Defense | タワー、敵、ウェーブ、経路、アップグレード |
| `racing` | 2D top-down racing | 車両、路面、トラック、AI、アップグレード |
| `puzzle` | Puzzle / Sokoban系 | ピース、ルール、レベル、目標、難易度 |
| `brawler` | Beat'em up / arena | ファイター、技、コンボ、ヒットボックス、アリーナ |

## Shared

`shared/` は全ゲームへ強制する基底クラスではありません。必要なものだけ使います。

- `assets.csv` — 画像・音声・フォントの論理キー
- `tags.csv` — 共通タグ語彙
- `difficulties.csv` — 難易度プリセット
- `input_actions.csv` — 物理入力から独立した論理アクション
- `rarities.csv` — レアリティ
- `damage_channels.csv` — 汎用ダメージチャネル
- `currencies.csv` — 通貨
- `localization.csv` — ローカライズ文字列例

## 組み合わせ例

- Platformer → `shared/` + `packs/platformer/`
- Roguelite STG → `packs/shmup/` + `packs/roguelike/`
- Action platformer → `packs/platformer/` + `packs/brawler/`
- Base-defense survival → `packs/survival/` + `packs/tower_defense/`
- SRPG → `shared/` + `packs/tactics/`

複数Packを混ぜる場合はID名前空間を維持してください。詳細は `catalog/compatibility.csv` を参照します。

## Validation

```bash
python tools/validate_csvasset.py
```

GitHub Actionsでもpush / pull request時に検証します。規約は `docs/PACK_CONTRACT.md` と `docs/CONVENTIONS.md` を参照してください。
