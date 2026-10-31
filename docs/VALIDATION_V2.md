# v2検証記録

検証日: 2026-10-31。Python標準ライブラリのみで実行しました。

## 実行結果

| 検査 | 結果 |
|---|---|
| Pack数 | 30 |
| 生成データ種類 | 130 |
| 型・単位・計算式の定義 | 498フィールド |
| 種類別Archetype定義 | 991 |
| 同梱参照行 | 13,000、全列再生成一致 |
| 参照プリセット | 3,000、全IDの参照先が実在 |
| 元データと追加CSVの検査 | 305 CSV、成功 |
| ARPGの寸法・タイル・配置・到達性 | 8マップ、成功 |
| 回帰テスト | 19テスト、成功 |
| 負数・0・既定seedでの型/範囲/式検査 | 39,000候補、成功 |
| 全種類・既定規模の生成/全行再生成照合 | 1,300,000行、260 shards、成功 |
| 設定のユニーク署名数 | 1,251,445 |
| 設定の重複行数 | 48,555 |

[種類別の品質レポート](validation/quality_report.csv)。署名は役割と元パラメータの組み合わせです。ID、Tier、Grade、seed、bias、派生値は含みません。上記件数を「ユニークな130万種類」とは解釈しないでください。

## 再現コマンド

```bash
python tools/validate_csvasset.py
python -m unittest discover -s tests -v
python tools/build_reference_assets.py
git diff --exit-code -- catalog packs
python generator/generate_mass_assets.py --out /tmp/csvasset-full-v2
python generator/validate_generated.py /tmp/csvasset-full-v2
```

使用seed `2762026`、各表10,000行、shard 5,000行。出力先には未使用のパスを指定してください。

テストには、範囲外・NaN・式の改ざん・seed不一致・重複/欠落manifest・パス逸脱・symlink・外部キー破損・マップ上の不正配置・出力先の非破壊性を含みます。CIにも同じ検査とPython 3.10/3.12の検査を設定しました。

この記録はデータの構造的・数値的整合性についての検証です。完成ゲームでのバランスやプレイヤー体験の評価は含みません。
