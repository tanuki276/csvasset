#!/usr/bin/env python3
"""Validate schema, types, ranges, formulas, provenance and complete shard coverage."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import json
import math
from pathlib import Path
import re

from generate_mass_assets import BOOL_FIELDS, VERSION, columns, derive, make_row, sha, write_csv
from schema import SPECS


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def row_errors(row, spec):
    errors = []
    if list(row) != columns(spec) or any(v is None for v in row.values()):
        return ['column count/order mismatch']
    if row['archetype'] not in spec['archetypes']:
        errors.append('unknown archetype')
    numeric = {}
    for name in ['tier', 'grade', 'tuning_bias'] + [f[0] for f in spec['fields']] + list(spec['derived']):
        try:
            numeric[name] = float(row[name])
            if not math.isfinite(numeric[name]):
                raise ValueError('non-finite')
        except (ValueError, TypeError):
            errors.append(f'{name}: expected finite number')
    if errors:
        return errors
    for name, low, high, _ in [('tier',1,20,''), ('grade',0,4,''),
                               ('tuning_bias',-.05,.05,''), *spec['fields']]:
        value = numeric[name]
        if not low <= value <= high:
            errors.append(f'{name}: outside [{low}, {high}]')
        if isinstance(low, int) and isinstance(high, int) and not re.fullmatch(r'-?\d+', str(row[name])):
            errors.append(f'{name}: expected integer')
        if name in BOOL_FIELDS and value not in (0, 1):
            errors.append(f'{name}: expected boolean 0/1')
    for lower, upper in spec['ordered']:
        if numeric[lower] > numeric[upper]:
            errors.append(f'{lower} > {upper}')
    for name, rule in spec['derived'].items():
        try:
            if not math.isclose(numeric[name], derive(rule, row), rel_tol=1e-9, abs_tol=1e-6):
                errors.append(f'{name}: derived formula mismatch')
        except (ZeroDivisionError, ValueError):
            errors.append(f'{name}: invalid formula input')
    return errors


def validate(root):
    root = Path(root).resolve()
    errors = []
    try:
        summary = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
        expected_keys = {'generator_version','seed','dataset_count','rows_per_dataset','total_rows',
                         'shard_rows','tiers','grades','packs'}
        if set(summary) != expected_keys or summary['generator_version'] != VERSION:
            raise ValueError('unsupported summary schema/version')
        for key in ['seed','dataset_count','rows_per_dataset','total_rows','shard_rows','tiers','grades']:
            if type(summary[key]) is not int:
                raise ValueError(f'{key} must be an integer')
        if summary['rows_per_dataset'] < 100 or summary['shard_rows'] < 1:
            raise ValueError('invalid row/shard count')
        if summary['tiers'] != 20 or summary['grades'] != 5:
            raise ValueError('unsupported tier/grade coverage')
        packs = summary['packs']
        if not isinstance(packs, list) or not packs or len(set(packs)) != len(packs):
            raise ValueError('invalid pack list')
        if not set(packs) <= {key[0] for key in SPECS}:
            raise ValueError('unknown pack')
        expected = {key for key in SPECS if key[0] in packs}
        if summary['dataset_count'] != len(expected):
            raise ValueError('summary dataset count mismatch')
        if summary['total_rows'] != len(expected) * summary['rows_per_dataset']:
            raise ValueError('summary total mismatch')
        headers, manifest = read_csv(root / 'manifest.csv')
        if headers != ['pack','dataset','file','rows','sha256'] or not manifest:
            raise ValueError('invalid manifest header/empty manifest')
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [f'metadata: {error}'], []
    expected_files = {}
    for pack, dataset in sorted(expected):
        for start in range(0, summary['rows_per_dataset'], summary['shard_rows']):
            relative = f'{pack}/{dataset}/part-{start // summary["shard_rows"]:05d}.csv'
            expected_files[relative] = (pack, dataset, start,
                min(summary['shard_rows'], summary['rows_per_dataset'] - start))
    if [r.get('file') for r in manifest] != list(expected_files):
        return ['manifest shard order/coverage mismatch (missing, duplicate or unknown file)'], []
    seen = set()
    stats = defaultdict(lambda: dict(rows=0, tiers=Counter(), grades=Counter(), arches=Counter(), signatures=set()))
    for item in manifest:
        relative = item.get('file')
        if relative not in expected_files or relative in seen:
            errors.append(f'unknown/duplicate shard: {relative}')
            continue
        seen.add(relative)
        pack, dataset, start, expected_count = expected_files[relative]
        if item['pack'] != pack or item['dataset'] != dataset or item['rows'] != str(expected_count):
            errors.append(f'{relative}: manifest identity/count mismatch')
        path = root / relative
        if not path.resolve().is_relative_to(root) or path.is_symlink():
            errors.append(f'{relative}: unsafe path')
            continue
        try:
            if sha(path) != item['sha256']:
                errors.append(f'{relative}: sha256 mismatch')
            with path.open(encoding='utf-8', newline='') as stream:
                reader = csv.DictReader(stream)
                spec = SPECS[pack, dataset]
                if reader.fieldnames != columns(spec):
                    errors.append(f'{relative}: schema mismatch')
                    continue
                count = 0
                state = stats[pack, dataset]
                for index, row in enumerate(reader, start):
                    count += 1
                    row_id = f'{pack}_{dataset}_{index + 1:06d}'
                    issues = row_errors(row, spec)
                    if row.get('id') != row_id:
                        issues.append('nonsequential/duplicate id')
                    if row.get('seed_key') != f'{summary["seed"]}:{index + 1}':
                        issues.append('seed/index mismatch')
                    if row.get('tier') != str(index % 20 + 1) or row.get('grade') != str((index // 20) % 5):
                        issues.append('tier/grade schedule mismatch')
                    if not issues and row != {k:str(v) for k,v in make_row(pack,dataset,index,summary['seed']).items()}:
                        issues.append('seed regeneration mismatch')
                    if issues:
                        if len(errors) < 100:
                            errors.append(f'{row_id}: {"; ".join(issues)}')
                        continue
                    state['rows'] += 1
                    state['tiers'][row['tier']] += 1
                    state['grades'][row['grade']] += 1
                    state['arches'][row['archetype']] += 1
                    # Do not count unique IDs, tiers, grades, seed or tiny bias noise as diversity.
                    state['signatures'].add(tuple(row[n] for n in ['archetype'] + [f[0] for f in spec['fields']]))
                if count != expected_count:
                    errors.append(f'{relative}: actual row count mismatch')
                if start + expected_count == summary['rows_per_dataset']:
                    state['unique_count'] = len(state['signatures'])
                    state['signatures'].clear()
        except (OSError, csv.Error, UnicodeError, ValueError) as error:
            errors.append(f'{relative}: {error}')
    if seen != set(expected_files):
        errors.append('missing expected shards')
    actual_files = {p.relative_to(root).as_posix() for p in root.rglob('*.csv')}
    if actual_files - (set(expected_files) | {'manifest.csv','quality_report.csv'}):
        errors.append('unlisted CSV files')
    report = []
    for key in sorted(expected):
        state = stats[key]
        issues = []
        if state['rows'] != summary['rows_per_dataset']:
            issues.append('rows')
        if len(state['tiers']) != 20 or len(state['grades']) != 5:
            issues.append('tier/grade coverage')
        if set(state['arches']) != set(SPECS[key]['archetypes']):
            issues.append('archetype coverage')
        unique_count = state.get('unique_count',len(state['signatures']))
        ratio = unique_count / max(1, state['rows'])
        # Discrete schemas have finite state spaces; report duplicates honestly rather
        # than treating IDs, grades or bias noise as new behavior. Reject collapsed data.
        if unique_count < min(state['rows'], 2 * len(SPECS[key]['archetypes'])):
            issues.append('collapsed behavioral diversity')
        if issues:
            errors.append(f'{key}: {", ".join(issues)}')
        report.append(dict(pack=key[0], dataset=key[1], rows=state['rows'],
                           tiers=len(state['tiers']), grades=len(state['grades']), archetypes=len(state['arches']),
                           unique_signature_ratio=f'{ratio:.6f}', unique_configurations=unique_count,
                           duplicate_rows=state['rows']-unique_count, status='failed' if issues else 'ok'))
    return errors, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?', default=Path('generated'))
    args = parser.parse_args()
    errors, report = validate(args.root)
    if report:
        write_csv(args.root / 'quality_report.csv', list(report[0]), report)
    if errors:
        for error in errors[:100]:
            print(f'ERROR {error}')
        raise SystemExit(f'{len(errors)} validation errors')
    print(f'CSVASSET generated validation OK: {sum(r["rows"] for r in report)} rows, {len(report)} datasets')


if __name__ == '__main__':
    main()
