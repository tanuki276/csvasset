#!/usr/bin/env python3
"""Refresh the checked-in v2 reference library and schema catalog deterministically."""
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'generator'))
from generate_mass_assets import columns, make_row, sha, write_csv
from schema import NEW_PACKS, SPECS

SEED = 2762026
REFERENCE_ROWS = 100


def build():
    with (ROOT / 'catalog/packs.csv').open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        pack_fields = reader.fieldnames
        existing = {row['pack_id']: row for row in reader if row['pack_id'] not in NEW_PACKS}
    for pack, metadata in sorted(NEW_PACKS.items()):
        datasets = sorted(ds for pid, ds in SPECS if pid == pack)
        record = dict(pack_id=pack, schema_version='2.0.0', genre=pack.replace('_', '-'),
                      perspective='engine_defined', time_model=metadata['time_model'],
                      coordinate_model=metadata['coordinate_model'], dependencies='',
                      entrypoints='reference_presets.csv|' + '|'.join(f'variants/{ds}.csv' for ds in datasets),
                      description=metadata['title'] + ' deterministic tuning presets')
        write_csv(ROOT / 'packs' / pack / 'manifest.csv', pack_fields, [record])
        existing[pack] = record
    write_csv(ROOT / 'catalog/packs.csv', pack_fields, existing.values())
    write_csv(ROOT / 'catalog/generated_datasets.csv',
              ['pack_id','dataset_id','default_rows','shard_rows','tiers','grades','generation_model'],
              (dict(pack_id=p, dataset_id=d, default_rows=10000, shard_rows=5000,
                    tiers=20, grades=5, generation_model='typed_role_anchors_v2') for p,d in sorted(SPECS)))
    field_rows, reference_manifest = [], []
    for (pack, dataset), spec in sorted(SPECS.items()):
        relative = f'packs/{pack}/variants/{dataset}.csv'
        path = ROOT / relative
        write_csv(path, columns(spec), (make_row(pack, dataset, i, SEED) for i in range(REFERENCE_ROWS)))
        reference_manifest.append(dict(pack=pack, dataset=dataset, file=relative,
                                       rows=REFERENCE_ROWS, sha256=sha(path)))
        for name, low, high, unit in spec['fields']:
            field_rows.append(dict(pack=pack, dataset=dataset, field=name,
                                   type='int' if isinstance(low,int) and isinstance(high,int) else 'float',
                                   unit=unit, minimum=low, maximum=high, formula=''))
        for name, formula in spec['derived'].items():
            units = {'jump_height_px':'px','airtime_sec':'s','total_frames':'frame',
                     'nominal_dps':'damage/s','ideal_0_to_100_sec':'s','estimated_notes':'note',
                     'output_per_sec':'item/s','base_payback_sec':'s'}
            field_rows.append(dict(pack=pack,dataset=dataset,field=name,type='derived',
                                   unit=units[name],minimum='',maximum='',formula='|'.join(formula)))
    write_csv(ROOT / 'catalog/fields.csv',
              ['pack','dataset','field','type','unit','minimum','maximum','formula'], field_rows)
    write_csv(ROOT / 'catalog/reference_manifest.csv',
              ['pack','dataset','file','rows','sha256'], reference_manifest)
    # Named integration presets resolve each optional v2 dataset to a real row ID.
    # They are neutral selection bundles, not assertions of play-tested balance.
    for pack in sorted({pid for pid, ds in SPECS}):
        datasets = sorted(ds for pid, ds in SPECS if pid == pack)
        write_csv(ROOT / 'packs' / pack / 'reference_presets.csv', ['id'] + [ds+'_id' for ds in datasets],
                  (dict(id=f'{pack}_preset_{i+1:02d}',
                        **{ds+'_id': f'{pack}_{ds}_{i+1:06d}' for ds in datasets}) for i in range(REFERENCE_ROWS)))
        text = f'# {pack}: v2 reference presets\n\n'
        if pack in NEW_PACKS:
            text += NEW_PACKS[pack]['title'] + '用のエンジン非依存チューニング候補です。\n\n'
        text += ('`variants/` の各CSVは100行、20 Tier × 5 Gradeを含みます。'
                 '`reference_presets.csv` は各テーブルの実在IDを結ぶ100個の選択例です。\n\n'
                 '既存Packのv1データはそのまま利用できます。v2の列定義・単位・範囲・計算式は '
                 '`../../catalog/fields.csv`、役割の基準値は `../../generator/archetype_profiles.py` を参照。\n\n'
                 '## データ種類\n\n| CSV | Archetypes |\n|---|---|\n')
        for ds in datasets:
            text += f'| `variants/{ds}.csv` | {", ".join(SPECS[pack,ds]["archetypes"])} |\n'
        text += ('\n実測値や完成ゲームのバランスではありません。役割ごとの架空の基準値と範囲から'
                 '決定的に生成します。新規Packに画像・音声・完成マップは含みません。'
                 '実ゲームでは採用したIDのパラメータを調整してください。\n')
        (ROOT / 'packs' / pack / 'VARIANTS.md').write_text(text, encoding='utf-8')
    metadata = dict(version='2.0.0',seed=SEED,rows_per_dataset=REFERENCE_ROWS,
                    packs=len(existing),datasets=len(SPECS),reference_rows=REFERENCE_ROWS*len(SPECS),
                    integration_presets=REFERENCE_ROWS*len(existing),fields=len(field_rows))
    (ROOT / 'catalog/reference_summary.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(metadata))


if __name__ == '__main__':
    build()
