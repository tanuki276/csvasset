# Mass CSVASSET Generator v2

30 packs / 130 datasets / 991 dataset-archetype definitions。
既定で各10,000行、合計1,300,000行、5,000行/shardを生成します。Python 3.10以上、標準ライブラリのみ。

```bash
python generator/generate_mass_assets.py --out generated
python generator/validate_generated.py generated

# 選択したPackのみ
python generator/generate_mass_assets.py --packs rhythm farming --out generated-subset

# 全種類を小規模に検査。100行で20 Tier × 5 Gradeを網羅
python generator/generate_mass_assets.py --rows-per-dataset 100 --shard-rows 37 --out generated-small
python generator/validate_generated.py generated-small
```

- `--rows-per-dataset`: 100以上。全種類を20,000行ずつなら2,600,000行。
- `--shard-rows`: 1以上。最後のshardの端数も検査。
- `--seed`: 整数、既定 `2762026`。同じコード・seed・行番号から同じ行を再現。
- `--packs`: 1つ以上のPack名。存在しない名前はエラー。
- `--out`: 新規または空のディレクトリ。既存出力の消去や上書きは行いません。

`schema.py` が型・範囲・単位・順序制約・計算式、`archetype_profiles.py` が役割別の基準値を定義します。`legacy_specs.py` はv1の30表の列名と範囲を保持します。

`summary.json` と `manifest.csv` から完全性を検査し、全行をseedから再生成して照合します。追加の列、NaN、整数でない整数列、範囲外、式の不一致、欠落shard、重複manifest、未知CSV、外へのシンボリックリンクは失敗します。

`quality_report.csv` は実際の設定のユニーク数・重複行数を含みます。署名にID・seed・Tier・Grade・tuning_bias・派生列を含めません。整数中心の表では設定の空間が有限なので、重複率を任意の95%閾値で不合格にしません。全役割の網羅と、設定が少数に潰れていないことは別途検査します。

全種類の小規模版を `packs/*/variants/` に同梱します。再構築は `python tools/build_reference_assets.py`。生成器v1から数値は変わるため、v1生成物とのID照合だけで同じ設定だと判断しないでください。詳細は [品質モデル](../docs/QUALITY_V2.md)。
