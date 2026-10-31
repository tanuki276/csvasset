#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
import csv,re,sys
R=Path(__file__).resolve().parents[1]; E=[]; ID=re.compile(r'^[a-z0-9][a-z0-9_:\-.]*$')
def rd(p):
    with (R/p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def fail(x):E.append(x)
def ids(p,k='id'):
    v=[r[k] for r in rd(p)]
    if len(v)!=len(set(v)):fail(f'{p}: duplicate {k}')
    return set(v)
# generic CSV structure; raw ARPG maps are headerless grids
csv_files = [p for directory in ('packs','shared','catalog') for p in (R/directory).rglob('*.csv')]
for p in csv_files:
    rel=p.relative_to(R)
    if rel.parts[:3]==('packs','action_rpg','maps'):continue
    with p.open(encoding='utf-8',newline='') as f: a=list(csv.reader(f))
    if not a: fail(f'{rel}: empty'); continue
    n=len(a[0])
    if len(a[0])!=len(set(a[0])):fail(f'{rel}: duplicate header')
    for i,row in enumerate(a[1:],2):
        if len(row)!=n:fail(f'{rel}:{i}: wrong field count')
    if any(len(row)!=n for row in a[1:]):continue
    if 'id' in a[0]:
        ix=a[0].index('id'); vals=[x[ix] for x in a[1:]]
        if len(vals)!=len(set(vals)):fail(f'{rel}: duplicate id')
        for v in vals:
            if not v or not ID.match(v):fail(f'{rel}: invalid id {v}')
if E:
    print('\n'.join(E)); sys.exit(1)
# pack contract
packs={r['pack_id']:r for r in rd('catalog/packs.csv')}; dirs={p.name for p in (R/'packs').iterdir() if p.is_dir()}
if set(packs)!=dirs:fail('catalog pack list != directories')
for pid in dirs:
    m=rd(f'packs/{pid}/manifest.csv')
    if len(m)!=1 or m[0]['pack_id']!=pid:fail(f'{pid}: bad manifest')
    for ep in m[0]['entrypoints'].split('|'):
        if ep and not (R/'packs'/pid/ep).exists():fail(f'{pid}: missing entrypoint {ep}')
# shared channels / rarity
channels=ids('shared/damage_channels.csv'); rarities=ids('shared/rarities.csv')
for p in ['packs/shmup/projectiles.csv','packs/tactics/abilities.csv','packs/tower_defense/towers.csv','packs/brawler/moves.csv']:
    for r in rd(p):
        if r['damage_channel'] not in channels:fail(f'{p}: bad damage channel')
for r in rd('packs/roguelike/item_pools.csv'):
    if r['rarity'] not in rarities:fail('roguelike: bad rarity')
# platformer
pt=ids('packs/platformer/stages.csv'); tun=ids('packs/platformer/player_tuning.csv'); mov=ids('packs/platformer/movement_profiles.csv')
for r in rd('packs/platformer/stages.csv'):
    if r['tuning_id'] not in tun or r['movement_profile_id'] not in mov:fail(f"platformer stage {r['id']}: bad profile")
for r in rd('packs/platformer/checkpoints.csv'):
    if r['stage_id'] not in pt:fail(f"platformer checkpoint {r['id']}: bad stage")
# shmup
wep=ids('packs/shmup/weapons.csv'); pro=ids('packs/shmup/projectiles.csv'); ene=ids('packs/shmup/enemies.csv'); sta=ids('packs/shmup/stages.csv'); paths=ids('packs/shmup/paths.csv')
for r in rd('packs/shmup/ships.csv'):
    if r['weapon_id'] not in wep:fail('shmup: ship weapon')
for r in rd('packs/shmup/weapons.csv'):
    if r['projectile_id'] not in pro:fail('shmup: weapon projectile')
for r in rd('packs/shmup/waves.csv'):
    if r['enemy_id'] not in ene or r['stage_id'] not in sta or r['path_id'] not in paths:fail(f"shmup wave {r['id']}: bad ref")
# roguelike
ents=ids('packs/roguelike/entities.csv'); its=ids('packs/roguelike/items.csv')
for r in rd('packs/roguelike/encounter_tables.csv'):
    if r['entry_id'] not in ents or int(r['weight'])<=0:fail('roguelike encounter')
for r in rd('packs/roguelike/item_pools.csv'):
    if r['item_id'] not in its:fail('roguelike item pool')
# tactics
cls=ids('packs/tactics/classes.csv'); abi=ids('packs/tactics/abilities.csv'); sets=defaultdict(set)
for r in rd('packs/tactics/ability_sets.csv'):
    if r['ability_id'] not in abi:fail('tactics ability set')
    sets[r['set_id']].add(r['ability_id'])
for r in rd('packs/tactics/units.csv'):
    if r['class_id'] not in cls or r['ability_set'] not in sets:fail(f"tactics unit {r['id']}: bad ref")
# survival
si=ids('packs/survival/items.csv')
for r in rd('packs/survival/recipes.csv'):
    if r['output_id'] not in si:fail(f"survival recipe {r['id']}: bad output")
    for t in r['ingredients'].split('|'):
        q=t.split(':',1)
        if len(q)!=2 or q[0] not in si or int(q[1])<1:fail(f"survival recipe {r['id']}: bad ingredient")
# tower defense
tde=ids('packs/tower_defense/enemies.csv'); tdt=ids('packs/tower_defense/towers.csv')
for r in rd('packs/tower_defense/waves.csv'):
    if r['enemy_id'] not in tde:fail('tower defense wave')
for r in rd('packs/tower_defense/upgrades.csv'):
    if r['tower_id'] not in tdt:fail('tower defense upgrade')
# racing
sur=ids('packs/racing/surfaces.csv'); tr=ids('packs/racing/tracks.csv'); lines=ids('packs/racing/ai_lines.csv')
for r in rd('packs/racing/tracks.csv'):
    if r['default_surface'] not in sur or r['ai_line_id'] not in lines:fail(f"racing track {r['id']}: bad ref")
for r in rd('packs/racing/ai_lines.csv'):
    if r['track_id'] not in tr:fail('racing ai line')
# puzzle
mech=ids('packs/puzzle/mechanics.csv'); goals=ids('packs/puzzle/goals.csv')
for r in rd('packs/puzzle/levels.csv'):
    if r['goal_id'] not in goals or any(x not in mech for x in r['mechanics'].split('|')):fail(f"puzzle level {r['id']}: bad ref")
# brawler
moves=ids('packs/brawler/moves.csv'); move_sets=defaultdict(int)
for r in rd('packs/brawler/moves.csv'):move_sets[r['move_set_id']]+=1
for r in rd('packs/brawler/fighters.csv'):
    if not move_sets[r['move_set_id']]:fail(f"brawler fighter {r['id']}: empty moveset")
for r in rd('packs/brawler/hitboxes.csv'):
    if r['move_id'] not in moves:fail('brawler hitbox')
for r in rd('packs/brawler/combos.csv'):
    if any(x not in moves for x in r['move_sequence'].split('|')):fail(f"brawler combo {r['id']}: bad move")
# action RPG: run legacy validator semantics from nested data for critical graph
A=R/'packs/action_rpg'
def ard(p):
    with (A/p).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def aids(p,k='id'):return {r[k] for r in ard(p)}
el=aids('data/core/elements.csv'); sk=aids('data/combat/skills.csv'); enemies=aids('data/enemies/enemies.csv'); ai=aids('data/enemies/ai_profiles.csv'); bio=aids('data/world/biomes.csv')
loot={r['table_id'] for r in ard('data/loot/loot_tables.csv')}; w=defaultdict(int); rc=defaultdict(int)
for r in ard('data/enemies/enemies.csv'):
    if r['element'] not in el or r['ai_profile'] not in ai or r['biome'] not in bio or r['loot_table'] not in loot:fail(f"action_rpg enemy {r['id']}: bad ref")
for r in ard('data/enemies/enemy_skills.csv'):
    if r['enemy_id'] not in enemies or r['skill_id'] not in sk:fail('action_rpg enemy skill')
    w[r['enemy_id']]+=int(r['weight'])
for r in ard('data/enemies/enemy_resistances.csv'):rc[r['enemy_id']]+=1
for e in enemies:
    if w[e]!=100 or rc[e]!=len(el-{'neutral'}):fail(f'action_rpg enemy {e}: incomplete weights/resistances')
# v2 semantic checks are part of the single public validation entrypoint.
from validate_integrity import validate as validate_integrity
from validate_reference_assets import validate as validate_reference
E.extend(validate_integrity(R))
E.extend(validate_reference(R))
if E:
    print('CSVASSET validation FAILED'); [print(' -',x) for x in E]; sys.exit(1)
print(f'CSVASSET validation OK: {len(csv_files)} CSV files across {len(packs)} packs')
