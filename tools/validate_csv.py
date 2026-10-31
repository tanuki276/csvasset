#!/usr/bin/env python3
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def read(rel):
    with (ROOT / rel).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def ids(rel, key="id"):
    rows = read(rel)
    vals = [r[key] for r in rows]
    if len(vals) != len(set(vals)):
        errors.append(f"{rel}: duplicate {key}")
    if any(not v for v in vals):
        errors.append(f"{rel}: empty {key}")
    return set(vals)

def require(value, allowed, where):
    if value and value not in allowed:
        errors.append(f"{where}: unknown reference {value}")

elements = ids("data/core/elements.csv")
statuses = ids("data/core/status_effects.csv")
skills = ids("data/combat/skills.csv")
projectiles = ids("data/combat/projectiles.csv")
weapons = ids("data/equipment/weapons.csv")
armors = ids("data/equipment/armor.csv")
items = ids("data/items/items.csv")
enemies = ids("data/enemies/enemies.csv")
ai = ids("data/enemies/ai_profiles.csv")
biomes = ids("data/world/biomes.csv")
tiles = ids("data/world/tiles.csv")
stages = ids("data/world/stages.csv")
groups = ids("data/world/spawn_groups.csv")
npcs = ids("data/npc/npcs.csv")
shops = ids("data/npc/shops.csv")
quests = ids("data/quests/quests.csv")
recipes = ids("data/crafting/recipes.csv")
dialogues = ids("data/npc/dialogues.csv")
all_assets = items | weapons | armors

for r in read("data/progression/classes.csv"):
    require(r["starter_weapon"], weapons, f"class {r['id']}")
    require(r["starter_skill"], skills, f"class {r['id']}")

for r in read("data/combat/skills.csv"):
    require(r["element"], elements, f"skill {r['id']}")
    require(r["status_id"], statuses, f"skill {r['id']}")
    if float(r["cooldown_sec"]) < 0 or float(r["range_tiles"]) < 0:
        errors.append(f"skill {r['id']}: invalid timing/range")

for r in read("data/combat/skill_projectiles.csv"):
    require(r["skill_id"], skills, "skill_projectiles")
    require(r["projectile_id"], projectiles, "skill_projectiles")

loot = read("data/loot/loot_tables.csv")
loot_tables = {r["table_id"] for r in loot}
for r in loot:
    require(r["item_id"], all_assets, f"loot {r['table_id']}")
    if not 0 <= float(r["chance"]) <= 1:
        errors.append(f"loot {r['table_id']}: chance outside 0..1")
    if int(r["min_qty"]) < 1 or int(r["max_qty"]) < int(r["min_qty"]):
        errors.append(f"loot {r['table_id']}: invalid quantity")

skill_weights = defaultdict(int)
res_count = defaultdict(int)
for r in read("data/enemies/enemies.csv"):
    require(r["element"], elements, f"enemy {r['id']}")
    require(r["biome"], biomes, f"enemy {r['id']}")
    require(r["ai_profile"], ai, f"enemy {r['id']}")
    require(r["loot_table"], loot_tables, f"enemy {r['id']}")
for r in read("data/enemies/enemy_skills.csv"):
    require(r["enemy_id"], enemies, "enemy_skills")
    require(r["skill_id"], skills, "enemy_skills")
    skill_weights[r["enemy_id"]] += int(r["weight"])
for r in read("data/enemies/enemy_resistances.csv"):
    require(r["enemy_id"], enemies, "enemy_resistances")
    require(r["element"], elements, "enemy_resistances")
    if float(r["damage_multiplier"]) <= 0:
        errors.append("enemy_resistances: multiplier must be > 0")
    res_count[r["enemy_id"]] += 1
for eid in enemies:
    if skill_weights[eid] != 100:
        errors.append(f"enemy {eid}: skill weights != 100")
    if res_count[eid] != len(elements - {"neutral"}):
        errors.append(f"enemy {eid}: incomplete elemental resistance rows")

for r in read("data/world/spawn_groups.csv"):
    total = 0
    for token in r["weighted_enemies"].split("|"):
        eid, weight = token.split(":", 1)
        require(eid, enemies, f"spawn_group {r['id']}")
        total += int(weight)
    if total != 100:
        errors.append(f"spawn_group {r['id']}: weights != 100")

stage_rows = {r["id"]: r for r in read("data/world/stages.csv")}
walkable = {r["id"]: bool(int(r["walkable"])) for r in read("data/world/tiles.csv")}
grids = {}
for sid, r in stage_rows.items():
    require(r["biome"], biomes, f"stage {sid}")
    require(r["next_stage_id"], stages, f"stage {sid}")
    p = ROOT / r["map_path"]
    if not p.exists():
        errors.append(f"stage {sid}: missing map")
        continue
    with p.open(encoding="utf-8", newline="") as f:
        g = list(csv.reader(f))
    grids[sid] = g
    h, w = len(g), len(g[0]) if g else 0
    if w != int(r["width"]) or h != int(r["height"]) or any(len(row) != w for row in g):
        errors.append(f"stage {sid}: map dimensions invalid")
    bad = {cell for row in g for cell in row if cell not in tiles}
    if bad:
        errors.append(f"stage {sid}: unknown tiles {sorted(bad)}")

def point(stage, x, y, where):
    if stage not in stage_rows or stage not in grids:
        return
    x, y = int(x), int(y)
    st = stage_rows[stage]
    if not (0 <= x < int(st["width"]) and 0 <= y < int(st["height"])):
        errors.append(f"{where}: out of bounds")
        return
    tile = grids[stage][y][x]
    if not walkable.get(tile, False):
        errors.append(f"{where}: non-walkable tile {tile}")

for r in read("data/world/spawns.csv"):
    require(r["stage_id"], stages, f"spawn {r['id']}")
    require(r["group_id"], groups, f"spawn {r['id']}")
    point(r["stage_id"], r["x"], r["y"], f"spawn {r['id']}")
for r in read("data/world/stage_connections.csv"):
    require(r["from_stage"], stages, "connection")
    require(r["to_stage"], stages, "connection")
    point(r["from_stage"], r["from_x"], r["from_y"], "connection-from")
    point(r["to_stage"], r["to_x"], r["to_y"], "connection-to")
for r in read("data/npc/npcs.csv"):
    require(r["stage_id"], stages, f"npc {r['id']}")
    require(r["shop_id"], shops, f"npc {r['id']}")
    point(r["stage_id"], r["x"], r["y"], f"npc {r['id']}")
for r in read("data/npc/dialogues.csv"):
    require(r["speaker_id"], npcs, f"dialogue {r['id']}")
    require(r["next_dialogue_id"], dialogues, f"dialogue {r['id']}")
    require(r["quest_id"], quests, f"dialogue {r['id']}")
for r in read("data/quests/objectives.csv"):
    require(r["quest_id"], quests, "objective")
    target = {"kill": enemies, "collect": all_assets, "reach": stages}.get(r["objective_type"])
    if target is None:
        errors.append(f"objective: unknown type {r['objective_type']}")
    else:
        require(r["target_id"], target, "objective")
for r in read("data/crafting/recipe_ingredients.csv"):
    require(r["recipe_id"], recipes, "ingredient")
    require(r["ingredient_id"], all_assets, "ingredient")

levels = read("data/progression/levels.csv")
if [int(r["level"]) for r in levels] != list(range(1, len(levels)+1)):
    errors.append("levels: levels are not contiguous")
if any(int(b["total_xp"]) <= int(a["total_xp"]) for a,b in zip(levels, levels[1:])):
    errors.append("levels: total_xp must strictly increase")
if int(levels[-1]["xp_to_next"]) != 0:
    errors.append("levels: cap xp_to_next must be 0")

if errors:
    print("CSVASSET validation failed")
    for e in errors:
        print("-", e)
    sys.exit(1)
print("CSVASSET validation OK")
print(f"enemies={len(enemies)} skills={len(skills)} stages={len(stages)} assets={len(all_assets)} quests={len(quests)}")
