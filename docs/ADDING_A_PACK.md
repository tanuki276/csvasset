# Packを追加する

1. `packs/<pack_id>/manifest.csv` をPack契約のヘッダーで作成します。
2. `catalog/packs.csv` に同じ定義を登録し、entrypointsの実ファイルを用意します。
3. 公開するCSVの列・単位・ID・外部キーを定義します。
4. 手書きの参照関係は `tools/validate_csvasset.py` または `tools/validate_integrity.py` に検証を追加します。
5. `python tools/validate_csvasset.py` を実行します。

## v2生成データの追加

`generator/schema.py` の `pack()` / `dataset()` に型・範囲・単位・必要な順序制約・派生式を追加し、`generator/archetype_profiles.py` に**各役割の明示的な基準値**を定義します。Archetype名だけの追加は行わないでください。

```bash
python tools/build_reference_assets.py
python tools/validate_csvasset.py
python -m unittest discover -s tests -v
python generator/generate_mass_assets.py --out generated-check --rows-per-dataset 100 --shard-rows 37
python generator/validate_generated.py generated-check
```

参照CSV・プリセット・フィールド定義・カタログを再構築してから一緒にコミットします。表やフィールドを変更した場合は、その意味と移行方法をドキュメントへ記載してください。
