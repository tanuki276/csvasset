# Pack Contract

CSVASSETのPackは「ゲーム1本」ではなく、ゲームシステムのまとまりです。

各Packは `manifest.csv` を持ち、`pack_id,schema_version,genre,perspective,time_model,coordinate_model,dependencies,entrypoints,description` を宣言します。

## ID namespace

Pack内IDは `snake_case`。複数Packを混ぜる場合は外部公開時に `<pack_id>:<local_id>` として扱える設計を推奨します。

例: `shmup:falcon`, `tactics:vanguard`, `platformer:spikes`。

## 自己完結性

Pack内参照は原則としてPack内部で解決します。`shared/` は便利な共通語彙であり、全Packへ強制する基底スキーマではありません。

ARPGのmana、STGのgraze、レースのgripなど、ジャンル固有概念は無理に共通化しません。
