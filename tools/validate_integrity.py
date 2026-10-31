#!/usr/bin/env python3
"""Deeper integrity checks for the original authored game data (no engine needed)."""
from collections import deque
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    root = Path(root)
    errors = []
    base = root / 'packs/action_rpg'
    cache = {}

    def read(name):
        if name not in cache:
            with (base / 'data' / (name+'.csv')).open(encoding='utf-8',newline='') as stream:
                cache[name] = list(csv.DictReader(stream))
        return cache[name]

    def keys(name, field='id'):
        return {r[field] for r in read(name)}

    def reference(source, field, target, target_field='id', optional=False):
        allowed = keys(target, target_field)
        for row in read(source):
            value = row[field]
            if not value and optional:
                continue
            # Legacy elemental affinity cells contain comma-delimited IDs.
            values = value.split(',') if source == 'core/elements' else [value]
            for entry in values:
                if entry not in allowed:
                    errors.append(f'{source}.{field}: missing {target}:{entry}')

    relations = [
        ('progression/classes','starter_weapon','equipment/weapons'),
        ('progression/classes','starter_skill','combat/skills'),
        ('combat/skills','damage_type','core/damage_types'),
        ('combat/skills','element','core/elements'),
        ('combat/skill_projectiles','skill_id','combat/skills'),
        ('combat/skill_projectiles','projectile_id','combat/projectiles'),
        ('equipment/weapons','element','core/elements'),
        ('enemies/enemy_resistances','enemy_id','enemies/enemies'),
        ('enemies/enemy_resistances','element','core/elements'),
        ('crafting/recipe_ingredients','recipe_id','crafting/recipes'),
        ('world/stages','biome','world/biomes'),
        ('world/spawns','stage_id','world/stages'),
        ('world/spawns','group_id','world/spawn_groups'),
        ('world/biomes','default_floor_tile','world/tiles'),
        ('npc/npcs','stage_id','world/stages'),
        ('npc/npcs','dialogue_root','npc/dialogues'),
        ('npc/dialogues','speaker_id','npc/npcs'),
        ('npc/shop_inventory','shop_id','npc/shops'),
        ('quests/objectives','quest_id','quests/quests'),
        ('quests/quests','start_stage','world/stages'),
        ('quests/quests','target_stage','world/stages'),
        ('world/stage_connections','from_stage','world/stages'),
        ('world/stage_connections','to_stage','world/stages'),
    ]
    for relation in relations:
        reference(*relation)
    for source,field,target in [
        ('combat/skills','status_id','core/status_effects'),
        ('world/stages','next_stage_id','world/stages'),
        ('npc/npcs','shop_id','npc/shops'),
        ('npc/dialogues','next_dialogue_id','npc/dialogues'),
        ('npc/dialogues','quest_id','quests/quests'),
        ('quests/quests','prerequisite_quest','quests/quests'),
        ('core/elements','strong_vs','core/elements'),
        ('core/elements','weak_vs','core/elements')]:
        reference(source,field,target,optional=True)
    item_ids = keys('items/items') | keys('equipment/weapons') | keys('equipment/armor')
    for source,field in [('loot/loot_tables','item_id'),('crafting/recipes','output_id'),
                         ('crafting/recipe_ingredients','ingredient_id'),('npc/shop_inventory','asset_id')]:
        for row in read(source):
            if row[field] not in item_ids:
                errors.append(f'{source}.{field}: unknown item {row[field]}')
    for row in read('quests/quests'):
        for token in filter(None,row['item_rewards'].split('|')):
            parts = token.split(':')
            if len(parts)!=2 or parts[0] not in item_ids or not parts[1].isdigit() or int(parts[1])<1:
                errors.append(f'quest {row["id"]}: invalid reward {token}')
    target_domains = {'kill':keys('enemies/enemies'), 'reach':keys('world/stages'), 'collect':item_ids}
    for row in read('quests/objectives'):
        if row['objective_type'] not in target_domains or row['target_id'] not in target_domains[row['objective_type']]:
            errors.append(f'quest objective: invalid {row["objective_type"]}:{row["target_id"]}')
    for row in read('world/spawn_groups'):
        weight = 0
        for token in row['weighted_enemies'].split('|'):
            parts = token.split(':')
            if len(parts)!=2 or parts[0] not in keys('enemies/enemies') or not parts[1].isdigit() or int(parts[1])<=0:
                errors.append(f'spawn group {row["id"]}: invalid enemy/weight')
            else:
                weight += int(parts[1])
        if weight != 100:
            errors.append(f'spawn group {row["id"]}: weights != 100')
    for source,fields in [('enemies/enemy_resistances',['enemy_id','element']),
                           ('enemies/enemy_skills',['enemy_id','skill_id']),
                           ('crafting/recipe_ingredients',['recipe_id','ingredient_id']),
                           ('quests/objectives',['quest_id','sequence']),
                           ('combat/skill_projectiles',['skill_id','projectile_id'])]:
        seen = set()
        for row in read(source):
            key = tuple(row[f] for f in fields)
            if key in seen:
                errors.append(f'{source}: duplicate composite key {key}')
            seen.add(key)
    # Numeric domains inferred only where the name has an unambiguous contract.
    # Signed deltas, multipliers and design-specific power values are not guessed.
    for path in (root/'packs').rglob('*.csv'):
        if 'maps' in path.parts or 'variants' in path.parts or path.name=='reference_presets.csv':
            continue
        with path.open(encoding='utf-8',newline='') as stream:
            for index,row in enumerate(csv.DictReader(stream),2):
                for name,value in row.items():
                    probability = name == 'chance' or name.endswith('_chance') or name.endswith('_hp_ratio')
                    nonnegative = name.endswith(('_sec','_ms','_frames'))
                    boolean = name in {'walkable','blocks_projectiles','blocks_vision','can_crit','loop','completes_quest'}
                    if not (probability or nonnegative or boolean) or value == '':
                        continue
                    try:
                        number = float(value)
                        if not math.isfinite(number) or number < 0 or probability and number > 1 or boolean and value not in {'0','1'}:
                            raise ValueError('range')
                    except (TypeError,ValueError):
                        errors.append(f'{path.relative_to(root)}:{index} {name}: invalid {value}')
    for source,lower,upper in [
        ('equipment/affixes','min_value','max_value'),('equipment/affixes','min_tier','max_tier'),
        ('loot/loot_tables','min_qty','max_qty'),('world/spawn_groups','min_count','max_count'),
        ('enemies/enemy_skills','phase_min','phase_max')]:
        for row in read(source):
            if float(row[lower]) > float(row[upper]):
                errors.append(f'{source}: {lower} > {upper}')
    # Map coordinates are zero-based tiles; collision is four-neighbor walking.
    stages = {r['id']:r for r in read('world/stages')}
    tiles = {r['id']:r for r in read('world/tiles')}
    maps = {}
    for sid,stage in stages.items():
        path = base / stage['map_path']
        if not path.resolve().is_relative_to((base/'maps').resolve()):
            errors.append(f'{sid}: unsafe map path')
            continue
        with path.open(encoding='utf-8',newline='') as stream:
            grid = list(csv.reader(stream))
        w,h = int(stage['width']),int(stage['height'])
        if len(grid)!=h or any(len(row)!=w for row in grid):
            errors.append(f'{sid}: map dimensions mismatch')
            continue
        if any(cell not in tiles for row in grid for cell in row):
            errors.append(f'{sid}: unknown tile')
            continue
        maps[sid] = grid
    anchors = {sid:[] for sid in maps}

    def position(sid,x,y,label):
        if sid not in maps:
            return
        grid = maps[sid]
        try:
            x,y = int(x),int(y)
            valid = 0<=y<len(grid) and 0<=x<len(grid[0]) and tiles[grid[y][x]]['walkable']=='1'
        except ValueError:
            valid = False
        if not valid:
            errors.append(f'{label}: blocked/out-of-bounds position {sid}({x},{y})')
        else:
            anchors[sid].append((x,y,label))
    for source in ['world/spawns','npc/npcs']:
        for row in read(source):
            position(row['stage_id'],row['x'],row['y'],row['id'])
    for row in read('world/stage_connections'):
        for prefix in ['from','to']:
            position(row[prefix+'_stage'],row[prefix+'_x'],row[prefix+'_y'],f'{prefix} connection')
    for sid,points in anchors.items():
        if not points:
            continue
        grid = maps[sid]
        start = points[0][:2]
        seen = {start}
        queue = deque([start])
        while queue:
            x,y = queue.popleft()
            for nx,ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                if 0<=ny<len(grid) and 0<=nx<len(grid[0]) and (nx,ny) not in seen and tiles[grid[ny][nx]]['walkable']=='1':
                    seen.add((nx,ny))
                    queue.append((nx,ny))
        for x,y,label in points:
            if (x,y) not in seen:
                errors.append(f'{sid}: unreachable {label}')
    levels = read('progression/levels')
    for previous,current in zip(levels,levels[1:]):
        if int(current['level'])!=int(previous['level'])+1 or int(current['total_xp'])!=int(previous['total_xp'])+int(previous['xp_to_next']):
            errors.append('progression/levels: noncontinuous XP curve')
    return errors


if __name__ == '__main__':
    issues = validate()
    if issues:
        print('\n'.join('ERROR '+issue for issue in issues[:100]))
        raise SystemExit(f'{len(issues)} integrity errors')
    print('CSVASSET authored integrity OK: references, domains, map collision/reachability, XP curve')
