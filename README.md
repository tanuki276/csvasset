# CSVASSET

複数ジャンルの2Dゲームで再利用できる、CSVベースのゲームデータ・チューニングライブラリです。画像・音声の素材集ではありません。

## v2: 種類と整合性の拡充

| 項目 | v1 | v2 |
|---|---:|---:|
| ジャンルPack | 10 | **30** |
| 大量生成データの種類 | 30 | **130** |
| 既定の生成行数 | 300,000 | **1,300,000** |
| Gitに同梱するv2参照候補 | 0 | **13,000** |
| 参照候補を結ぶプリセット | 0 | **3,000** |
| 種類別の役割定義 | 既存30表 | **991定義 / 130表** |

種類数は別スキーマのデータセット数です。生成行数には同じ設定の重複が含まれます。ID・Tier・Grade・微小な乱数を除いた重複数は `quality_report.csv` に明示します。

精度改善: 整数/真偽値/確率/単位の契約、全130表の役割別基準値、最小値≤最大値、派生値の計算式、seedからの全行再生成照合、ファイルハッシュ、プリセット外部キー、ARPGのタイル・歩行可能性・配置到達性・XP曲線を検証します。

## すぐに使う

追加インストール不要、Python 3.10以上の標準ライブラリだけで利用できます。CIはPython 3.10/3.12で検査します。

```bash
# 同梱CSVと全参照・計算式を検査
python tools/validate_csvasset.py

# 例: 農業用の各100候補と、それらをIDで選択するプリセット
# packs/farming/variants/crops.csv
# packs/farming/variants/soil.csv
# packs/farming/reference_presets.csv

# 30ジャンル × 合計130種類 × 各10,000行を生成
python generator/generate_mass_assets.py --out generated
python generator/validate_generated.py generated

# 必要なジャンルだけ、別フォルダへ生成
python generator/generate_mass_assets.py \
  --packs farming fishing restaurant --rows-per-dataset 1000 --out generated-life
python generator/validate_generated.py generated-life
```

出力先は**新規または空のディレクトリ**に限ります。既存ファイルは削除しません。生成ファイルはコミットせず、GitHub ActionsのArtifactに保存できます。

## Packs

既存Packのファイル・ID・列を保持しています。追加候補は `packs/<pack>/variants/` に分離し、各Packの `VARIANTS.md` から種類一覧を確認できます。

| Pack | ジャンル | v2の種類数 | 主な追加内容 |
|---|---|---:|---|
| [action_rpg](packs/action_rpg/VARIANTS.md) | ARPG | 5 | 敵・アイテム・スキル・仲間・天候 |
| [platformer](packs/platformer/VARIANTS.md) | 横スクロール | 5 | 敵・ハザード・移動・可動床・グラップル |
| [shmup](packs/shmup/VARIANTS.md) | STG | 5 | 敵・武器・ウェーブ・弾幕・ボスフェーズ |
| [roguelike](packs/roguelike/VARIANTS.md) | ローグライク | 5 | アイテム・Affix・遭遇・イベント・Mutator |
| [tactics](packs/tactics/VARIANTS.md) | SRPG | 5 | ユニット・能力・地形・陣形・リアクション |
| [survival](packs/survival/VARIANTS.md) | サバイバル | 5 | 資源・レシピ・構造物・天候・疾病 |
| [tower_defense](packs/tower_defense/VARIANTS.md) | TD | 5 | タワー・敵・ウェーブ・状態・標的選択 |
| [racing](packs/racing/VARIANTS.md) | レース | 5 | 車両・路面・強化・タイヤ・競技規則 |
| [puzzle](packs/puzzle/VARIANTS.md) | パズル | 5 | レベル候補・機構・目標・生成設定・ヒント |
| [brawler](packs/brawler/VARIANTS.md) | 格闘アクション | 5 | ファイター・技・コンボ・投げ・防御 |
| [farming](packs/farming/VARIANTS.md) | 農業・牧場 | 4 | 作物・家畜・土壌・季節 |
| [fishing](packs/fishing/VARIANTS.md) | 釣り | 4 | 魚・竿・ルアー・水域 |
| [card_battler](packs/card_battler/VARIANTS.md) | カード戦闘 | 4 | カード・遺物・遭遇・イベント |
| [rhythm](packs/rhythm/VARIANTS.md) | リズム | 4 | 判定幅・譜面設定・ノート・採点 |
| [city_builder](packs/city_builder/VARIANTS.md) | 都市建設 | 4 | 建物・公共設備・道路・政策 |
| [factory](packs/factory/VARIANTS.md) | 工場 | 4 | 機械・ベルト・鉱床・研究 |
| [space_trader](packs/space_trader/VARIANTS.md) | 宇宙交易 | 4 | 船・交易品・港・契約 |
| [stealth](packs/stealth/VARIANTS.md) | ステルス | 4 | 警備・道具・床材・警戒状態 |
| [horror](packs/horror/VARIANTS.md) | ホラー | 4 | 脅威・精神効果・物資・部屋 |
| [visual_novel](packs/visual_novel/VARIANTS.md) | VN | 4 | 人物・選択肢・シーン・表示設定 |
| [dungeon_crawler](packs/dungeon_crawler/VARIANTS.md) | ダンジョン探索 | 4 | 部屋・罠・扉・祭壇 |
| [metroidvania](packs/metroidvania/VARIANTS.md) | 探索アクション | 4 | 能力・ゲート・部屋・強化 |
| [sports](packs/sports/VARIANTS.md) | スポーツ | 4 | 選手・ボール・競技場・練習 |
| [naval](packs/naval/VARIANTS.md) | 海戦 | 4 | 艦艇・兵装・海況・任務 |
| [flight](packs/flight/VARIANTS.md) | 飛行 | 4 | 機体・エンジン・天候・任務 |
| [colony](packs/colony/VARIANTS.md) | コロニー | 4 | 住民・仕事・施設・事件 |
| [restaurant](packs/restaurant/VARIANTS.md) | 飲食店経営 | 4 | 料理・従業員・設備・客 |
| [idle](packs/idle/VARIANTS.md) | 放置 | 4 | 生産者・強化・転生・オフライン |
| [auto_battler](packs/auto_battler/VARIANTS.md) | オートバトラー | 4 | ユニット・シナジー・店・ラウンド |
| [creature_collector](packs/creature_collector/VARIANTS.md) | 育成収集 | 4 | 生物・技・生息地・訓練 |

`shared/` の入力・通貨・レアリティ等は任意で組み合わせます。Pack間ではID名前空間と単位を維持し、変換は利用側で実装してください。[組み合わせ例](catalog/compatibility.csv)。

## スキーマと再現

- [498フィールドの型・単位・範囲・計算式](catalog/fields.csv)
- [データセット一覧](catalog/generated_datasets.csv) / [参照CSVのSHA-256](catalog/reference_manifest.csv)
- [v2移行・品質モデル](docs/QUALITY_V2.md) / [大量生成](docs/MASS_GENERATION.md)
- [Pack契約](docs/PACK_CONTRACT.md) / [追加方法](docs/ADDING_A_PACK.md)

```bash
python tools/build_reference_assets.py  # 同梱13,000候補と3,000プリセットを再構築
python tools/validate_csvasset.py
python -m unittest discover -s tests -v
```

数値はオリジナルの架空ゲーム設計用候補です。整合性の検証は、プレイテストによる楽しさや難易度の保証とは異なります。パズル解の存在、完成したリズム譜面、物理シミュレーション、画像・音声の実ファイルは新規生成の対象に含みません。[データ方針](docs/DATA_POLICY.md)。
