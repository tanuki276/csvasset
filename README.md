# CSVASSET

2Dゲーム向けの汎用CSVデータセット集です。

ゲームロジックとデータを分離し、敵・アイテム・武器・スキル・ステージ・スポーン・ドロップ・NPCなどをCSVから読み込める構成を想定しています。

## CSV files

- `data/enemies.csv` — 敵ステータス
- `data/items.csv` — アイテム
- `data/weapons.csv` — 武器
- `data/skills.csv` — スキル
- `data/tiles.csv` — タイル定義
- `data/stages.csv` — ステージ設定
- `data/spawns.csv` — 敵スポーン
- `data/loot_tables.csv` — ドロップテーブル
- `data/npcs.csv` — NPC
- `data/dialogues.csv` — 会話
- `maps/stage_001.csv` — サンプルタイルマップ

IDを文字列で統一し、別CSVから参照できるようにしています。