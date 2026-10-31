#!/usr/bin/env python3
"""Generate reproducible, typed design candidates; never erase an output directory."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from schema import SPECS

ROOT = Path(__file__).resolve().parents[1]
VERSION = '2.0.0'
BASE_COLUMNS = ['id', 'tier', 'grade', 'seed_key', 'archetype', 'tuning_bias']
BOOL_FIELDS = {'is_multiplier', 'optional', 'fail_on_timeout'}


def u(seed, *parts):
    # JSON encoding avoids ambiguous separator-containing seed keys.
    key = json.dumps([seed, *parts], separators=(',', ':'), ensure_ascii=True)
    return int.from_bytes(hashlib.blake2b(key.encode(), digest_size=8).digest(), 'big') / (1 << 64)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def columns(spec):
    return BASE_COLUMNS + [f[0] for f in spec['fields']] + list(spec['derived'])


def derive(rule, row):
    op, *names = rule
    values = [float(row[name]) for name in names]
    if op == 'sum':
        return int(sum(values))
    if op == 'ballistic_height':
        value = values[0] ** 2 / (2 * values[1])
    elif op == 'ballistic_time':
        value = 2 * values[0] / values[1]
    elif op == 'dps':
        value = values[0] * values[1] / values[2]
    elif op == 'quotient':
        value = values[0] / values[1]
    elif op == 'acceleration_time':
        value = (100 / 3.6) / values[0]
    elif op == 'notes':
        return round(values[0] / 60 * values[1] * values[2])
    else:
        raise ValueError(f'Unknown derived operation: {op}')
    return round(value, 6)


def make_row(pack, dataset, index, seed):
    spec = SPECS[pack, dataset]
    tier, grade = index % 20 + 1, (index // 20) % 5
    archetypes = spec['archetypes']
    offset = int(u(seed, pack, dataset, 'rotation') * len(archetypes))
    archetype = archetypes[(index + index // 20 + index // 100 + offset) % len(archetypes)]
    row = dict(id=f'{pack}_{dataset}_{index + 1:06d}', tier=tier, grade=grade,
               seed_key=f'{seed}:{index + 1}', archetype=archetype,
               tuning_bias=round((u(seed, pack, dataset, 'bias', index) - .5) * .1, 7))
    for name, low, high, _ in spec['fields']:
        q = u(seed, pack, dataset, name, index)
        if name in BOOL_FIELDS:
            value = int(q >= .5)
        else:
            # Tier is an authoring axis, not a claim that every stat should increase.
            # Keep spread at every tier; interval, cost, penalty and speed can trade off.
            fraction = .55 * q + .35 * (tier - 1) / 19 + .10 * grade / 4
            value = low + (high - low) * fraction
            anchor = spec['anchors'][archetype].get(name)
            if anchor is not None:
                value = anchor + (high - low) * (.12 * (q - .5) + .08 * ((tier - 1) / 19 - .5))
                # Preserve categorical zero (stationary actors, zero-cost cards, no emissions).
                if anchor == 0:
                    value = 0
            factor = spec['profiles'].get(archetype, {}).get(name, 1)
            value = max(low, min(high, value * factor))
            value = round(value) if isinstance(low, int) and isinstance(high, int) else round(value, 6)
        row[name] = value
    for lower, upper in spec['ordered']:
        row[upper] = max(row[lower], row[upper])
    for name, rule in spec['derived'].items():
        row[name] = derive(rule, row)
    return row


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def generate(out, rows_per_dataset=10000, shard_rows=5000, seed=2762026, packs=None):
    if rows_per_dataset < 100:
        raise ValueError('rows-per-dataset must be >= 100 for 20 tiers and 5 grades')
    if shard_rows < 1:
        raise ValueError('shard-rows must be positive')
    selected = {key: value for key, value in SPECS.items() if not packs or key[0] in packs}
    unknown = set(packs or ()) - {key[0] for key in SPECS}
    if unknown:
        raise ValueError(f'Unknown packs: {sorted(unknown)}')
    if not selected:
        raise ValueError('No datasets selected')
    out = Path(out)
    # A typo such as --out . must never delete source or unrelated user files.
    if out.is_symlink() or out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError(f'Output must be a new or empty directory: {out}')
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for (pack, dataset), spec in sorted(selected.items()):
        for start in range(0, rows_per_dataset, shard_rows):
            end = min(start + shard_rows, rows_per_dataset)
            path = out / pack / dataset / f'part-{start // shard_rows:05d}.csv'
            write_csv(path, columns(spec), (make_row(pack, dataset, i, seed) for i in range(start, end)))
            manifest.append(dict(pack=pack, dataset=dataset, file=path.relative_to(out).as_posix(),
                                 rows=end - start, sha256=sha(path)))
    write_csv(out / 'manifest.csv', ['pack', 'dataset', 'file', 'rows', 'sha256'], manifest)
    summary = dict(generator_version=VERSION, seed=seed, dataset_count=len(selected),
                   rows_per_dataset=rows_per_dataset, total_rows=rows_per_dataset * len(selected),
                   shard_rows=shard_rows, tiers=20, grades=5, packs=sorted({key[0] for key in selected}))
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'generated')
    parser.add_argument('--rows-per-dataset', type=int, default=10000)
    parser.add_argument('--shard-rows', type=int, default=5000)
    parser.add_argument('--seed', type=int, default=2762026)
    parser.add_argument('--packs', nargs='+', help='Generate only the named packs')
    args = parser.parse_args()
    try:
        result = generate(args.out, args.rows_per_dataset, args.shard_rows, args.seed, args.packs)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result))


if __name__ == '__main__':
    main()
