#!/usr/bin/env python3
"""Check committed variants, catalog, integration foreign keys and regeneration parity."""
from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'generator'))
from generate_mass_assets import columns, make_row, sha
from schema import SPECS
from validate_generated import read_csv, row_errors


def validate(root=ROOT):
    root = Path(root)
    errors = []
    metadata = json.loads((root / 'catalog/reference_summary.json').read_text(encoding='utf-8'))
    fields, manifest = read_csv(root / 'catalog/reference_manifest.csv')
    expected = set(SPECS)
    if {(m['pack'],m['dataset']) for m in manifest} != expected or len(manifest) != len(expected):
        errors.append('reference manifest dataset coverage')
    catalog_fields, catalog = read_csv(root / 'catalog/generated_datasets.csv')
    if {(r['pack_id'],r['dataset_id']) for r in catalog} != expected or len(catalog) != len(expected):
        errors.append('generated catalog mismatch')
    _, field_catalog = read_csv(root / 'catalog/fields.csv')
    actual_fields = {(r['pack'],r['dataset'],r['field']) for r in field_catalog}
    expected_fields = {(p,d,n) for (p,d),s in SPECS.items() for n in columns(s)[6:]}
    if actual_fields != expected_fields or len(field_catalog) != len(expected_fields):
        errors.append('field catalog mismatch')
    for row in field_catalog:
        key = row['pack'], row['dataset']
        if key not in SPECS:
            continue
        source = next((f for f in SPECS[key]['fields'] if f[0] == row['field']), None)
        if source:
            _, low, high, unit = source
            kind = 'int' if isinstance(low,int) and isinstance(high,int) else 'float'
            if (row['type'], row['minimum'], row['maximum'], row['unit'],row['formula']) != (kind,str(low),str(high),unit,''):
                errors.append(f'field contract mismatch: {key}/{row["field"]}')
        elif row['formula'] != '|'.join(SPECS[key]['derived'][row['field']]):
            errors.append(f'derived formula catalog mismatch: {key}')
    tables = {}
    actual_paths = set()
    for item in manifest:
        key = item['pack'], item['dataset']
        if key not in SPECS:
            continue
        expected_path = f'packs/{key[0]}/variants/{key[1]}.csv'
        if item['file'] != expected_path:
            errors.append(f'noncanonical reference path: {key}')
            continue
        actual_paths.add(item['file'])
        path = root / item['file']
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            errors.append(f'unsafe reference path: {key}')
            continue
        if sha(path) != item['sha256']:
            errors.append(f'reference hash mismatch: {key}')
        header, rows = read_csv(path)
        spec = SPECS[key]
        if header != columns(spec):
            errors.append(f'reference schema mismatch: {key}')
            continue
        if len(rows) != metadata['rows_per_dataset'] or item['rows'] != str(len(rows)):
            errors.append(f'reference count mismatch: {key}')
        tables[key] = {row['id'] for row in rows}
        for index, row in enumerate(rows):
            issues = row_errors(row,spec)
            expected_row = {k:str(v) for k,v in make_row(*key,index,metadata['seed']).items()}
            if row != expected_row:
                issues.append('not reproducible from declared seed')
            if issues:
                errors.append(f'{key}/{index + 1}: {issues}')
    found = {p.relative_to(root).as_posix() for p in (root/'packs').glob('*/variants/*.csv')}
    if actual_paths != found:
        errors.append('unlisted/missing reference CSV')
    presets = 0
    packs = sorted({p for p,d in SPECS})
    for pack in packs:
        datasets = sorted(d for p,d in SPECS if p == pack)
        header, rows = read_csv(root / 'packs' / pack / 'reference_presets.csv')
        if header != ['id'] + [d+'_id' for d in datasets]:
            errors.append(f'{pack}: preset schema')
            continue
        if len(rows) != metadata['rows_per_dataset'] or len({r['id'] for r in rows}) != len(rows):
            errors.append(f'{pack}: preset count/unique IDs')
        presets += len(rows)
        for index, row in enumerate(rows):
            if row['id'] != f'{pack}_preset_{index+1:02d}':
                errors.append(f'{pack}: preset namespace/order')
            for dataset in datasets:
                if row[dataset+'_id'] not in tables.get((pack,dataset),set()):
                    errors.append(f'{pack}/{row["id"]}: dangling {dataset}_id')
    if (metadata['packs'], metadata['datasets'],metadata['reference_rows'],metadata['integration_presets'],metadata['fields']) != (
            len(packs),len(SPECS),metadata['rows_per_dataset']*len(SPECS),presets,len(expected_fields)):
        errors.append('reference summary mismatch')
    return errors


if __name__ == '__main__':
    issues = validate()
    if issues:
        print('\n'.join('ERROR '+issue for issue in issues[:100]))
        raise SystemExit(f'{len(issues)} reference validation errors')
    print('CSVASSET reference validation OK: 130 datasets, 13000 variants, 3000 linked presets')
