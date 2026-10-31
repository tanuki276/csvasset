# CSV Conventions

- UTF-8 / comma-separated / LF推奨
- 通常の表CSVは1行目ヘッダー。タイルマップなどのグリッドCSVはPack側で明示
- 真偽値は `0/1`
- IDはASCII lowercase `snake_case`
- 外部キーは `<entity>_id` を推奨
- ファイルパスは `/` 区切り

## Units

曖昧な `speed`, `time`, `distance` を避け、列名に単位を含めます。

`_sec`, `_ms`, `_px`, `_px_sec`, `_tiles`, `_deg`, `_multiplier`, `_chance` を標準語彙として使います。

確率は0..1、倍率は1.0基準、角度は度数法です。

## Lists

単純なリストは `|`、重み付き要素は `id:weight|id:weight`。複雑なネストは別CSVへ分離します。
