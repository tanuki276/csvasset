# Adding a Pack

1. `packs/<pack_id>/manifest.csv` を作る
2. 主キーと外部キーを決める
3. ジャンル固有概念を無理にsharedへ移さない
4. 空テンプレートではなく調整可能な実データ例を入れる
5. `catalog/packs.csv` を更新する
6. `python tools/validate_csvasset.py` を通す
7. 既存Packへ不要な互換性破壊がないか確認する
