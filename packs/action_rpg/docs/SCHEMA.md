# Schema / Relation Guide

## Primary IDs

原則として各マスタの `id` が主キーです。複合テーブルは列の組み合わせをキーとして扱います。

## Main relations

- `progression/classes.starter_weapon -> equipment/weapons.id`
- `progression/classes.starter_skill -> combat/skills.id`
- `combat/skills.status_id -> core/status_effects.id`
- `combat/skill_projectiles.skill_id -> combat/skills.id`
- `combat/skill_projectiles.projectile_id -> combat/projectiles.id`
- `enemies/enemies.element -> core/elements.id`
- `enemies/enemies.biome -> world/biomes.id`
- `enemies/enemies.ai_profile -> enemies/ai_profiles.id`
- `enemies/enemies.loot_table -> loot/loot_tables.table_id`
- `enemies/enemy_skills.enemy_id -> enemies/enemies.id`
- `enemies/enemy_skills.skill_id -> combat/skills.id`
- `enemies/enemy_resistances.enemy_id -> enemies/enemies.id`
- `enemies/enemy_resistances.element -> core/elements.id`
- `loot/loot_tables.item_id -> items/items.id OR equipment master id`
- `world/stages.biome -> world/biomes.id`
- `world/stages.next_stage_id -> world/stages.id`
- `world/spawns.stage_id -> world/stages.id`
- `world/spawns.group_id -> world/spawn_groups.id`
- `npc/npcs.stage_id -> world/stages.id`
- `npc/npcs.shop_id -> npc/shops.id`
- `npc/dialogues.speaker_id -> npc/npcs.id`
- `npc/dialogues.quest_id -> quests/quests.id`
- `quests/objectives.quest_id -> quests/quests.id`
- `crafting/recipe_ingredients.recipe_id -> crafting/recipes.id`

## Runtime defaults

暗黙デフォルトは最小限にしてください。特に戦闘値、耐性、クールダウン、スポーン半径はCSVの値を優先します。

## Map contract

`stages.csv` の `width,height` とマップCSVの列数・行数は一致させます。
セル値は `world/tiles.csv.id` でなければなりません。
`spawns.csv` と `npcs.csv` の座標はマップ範囲内かつ歩行可能セルに置くことを推奨します。
