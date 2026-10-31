"""Authored role anchors in declared units, aligned with schema archetype order.

Values are fictional gameplay defaults, with bounded variation in the generator.
A profile is stronger than a label: at least one domain-specific field changes.
"""
ANCHORS = {
 'action_rpg': {
  'enemy_variants': ('attack_range_tiles', [1,2,6,7,1,1]),
  'item_variants': ('stack_max', [1,1,1,1,1,1,50]),
  'skill_variants': ('range_tiles', [1,7,4,5,3,6]),
  'companions': ('assist_cooldown_sec', [8,5,3,6,2,10,12,4]),
  'weather': ('visibility_mult', [1,.8,.7,.3,.5,.9,.4,.85])},
 'platformer': {
  'enemy_variants': ('jump_power_px_sec', [0,520,0,0,0,0]),
  'hazard_variants': ('move_speed_px_sec', [0,0,180,120,0,220]),
  'movement_variants': ('gravity_px_sec2', [1400,850,1200,1500,1300]),
  'moving_platforms': ('speed_px_sec', [100,80,120,150,200,60,50,180]),
  'grapple_points': ('release_boost_px_sec', [0,40,80,20,180,100,50,120])},
 'shmup': {
  'enemy_variants': ('hp', [30,80,200,60,600,850]),
  'weapon_variants': ('projectile_count', [1,5,1,2,4,1]),
  'wave_variants': ('enemy_count', [12,9,15,40,6,3]),
  'bullet_patterns': ('angular_speed_deg_sec', [0,0,120,30,60,45,0,160]),
  'boss_phases': ('hp_threshold', [1,.85,.7,.55,.4,.25,.15,.05])},
 'roguelike': {
  'item_variants': ('curse_chance', [.02,.02,.08,0,.15,.01]),
  'affix_variants': ('value', [.3,.2,.4,.1,.25,-.2,.5]),
  'encounter_variants': ('threat_budget', [35,70,5,2,15,1]),
  'room_events': ('risk', [.25,.7,.4,.8,.1,.2,.6,.9]),
  'mutators': ('threat_mult', [1.4,1.3,1.5,.7,2,1.6,1.8,1.2])},
 'tactics': {
  'unit_variants': ('move_tiles', [4,5,4,4,9,3]),
  'ability_variants': ('range_tiles', [1,7,5,4,1,6,5]),
  'terrain_variants': ('move_cost', [1,2,2,4,3,2,3]),
  'formations': ('defense_bonus', [.1,.05,.25,0,.05,0,.3,.1]),
  'reactions': ('range_tiles', [7,1,3,1,1,4,6,1])},
 'survival': {
  'resource_variants': ('harvest_time_sec', [3,6,1,10,2,1,5]),
  'recipe_variants': ('craft_time_sec', [10,15,5,8,20,30]),
  'structure_variants': ('storage_slots', [0,0,80,8,0,0,0]),
  'weather': ('temperature_c', [20,12,-25,42,35,10,18,38]),
  'diseases': ('damage_per_sec', [.1,.3,1.4,1,.05,.5,1.2,.4])},
 'tower_defense': {
  'tower_variants': ('fire_interval_sec', [1,.08,2,1.5,.7,.1]),
  'enemy_variants': ('speed_tiles_sec', [1,2.2,.4,.6,1.5,.3]),
  'wave_variants': ('spawn_interval_sec', [.6,.15,1.2,.4,.5,1.1]),
  'status_effects': ('max_stacks', [1,5,8,1,3,2,1,1]),
  'targeting': ('switch_delay_sec', [.1,.1,.3,.1,.05,.05,.2,.1])},
 'racing': {
  'vehicle_variants': ('mass_kg', [1100,900,1000,850,1600,750]),
  'surface_variants': ('grip_mult', [1.2,.75,.65,.3,.6,.45]),
  'upgrade_variants': ('stat_gain', [.25,.2,.15,.18,.12,.1]),
  'tires': ('wet_grip_mult', [.3,.65,.8,1.3,1.1,.9,.4,.75]),
  'race_rules': ('laps', [1,5,50,3,1,10,1,3])},
 'puzzle': {
  'level_variants': ('solution_depth', [30,15,40,25,35,65]),
  'mechanic_variants': ('state_count', [2,2,4,4,2,6,3]),
  'objective_variants': ('target_count', [1,12,20,4,15,1]),
  'generators': ('obstacle_density', [.1,.2,.4,.25,.3,.05,.35,.15]),
  'hints': ('cost', [5,10,0,50,100,20,10,30])},
 'brawler': {
  'fighter_variants': ('move_speed_mult', [1,1.4,.7,1,.6,1.1]),
  'move_variants': ('startup_frames', [2,18,12,9,20,5,7]),
  'combo_variants': ('hit_count', [4,6,3,8,12,2]),
  'throws': ('damage', [15,15,45,50,20,30,35,25]),
  'defense': ('active_frames', [20,3,8,12,4,16,5,6])},
 'farming': {
  'crops': ('growth_days', [3,6,5,8,12,16,10,14,6,24]),
  'livestock': ('produce_interval_days', [1,1,1,2,4,5,3,7]),
  'soil': ('water_retention_mult', [1,1.6,.4,1.4,.8,1.2,.6,1.3]),
  'seasons': ('temperature_c', [16,32,14,-10,27,35])},
 'fishing': {
  'fish': ('mass_kg', [2,5,8,3,60,80,4,20,10,.2]),
  'rods': ('tension_limit_n', [30,150,250,120,500,80,200,800]),
  'lures': ('sink_speed_m_sec', [.2,.4,.8,0,.3,0,.1,.5]),
  'waters': ('depth_m', [8,30,3,20,15,10,120,2])},
 'card_battler': {
  'cards': ('energy_cost', [1,1,1,2,1,2,3,0,1,0]),
  'relics': ('shop_cost', [100,250,400,300,180,150,200,350]),
  'encounters': ('hp', [30,100,140,80,120,90,220,400]),
  'events': ('hp_cost', [0,0,0,5,20,0,0,0])},
 'rhythm': {
  'timing_windows': ('perfect_ms', [90,70,50,35,25,15]),
  'charts': ('scroll_px_sec', [300,400,450,350,380,200,500,280]),
  'notes': ('hold_duration_beats', [0,4,2,0,0,8,6,1]),
  'scoring': ('miss_penalty', [500,200,1000,300,800,600,0,900])},
 'city_builder': {
  'buildings': ('capacity', [80,40,100,50,200,300,500,20]),
  'utilities': ('emissions_kg_day', [0,0,2000,1000,0,0,50,100]),
  'roads': ('speed_kph', [30,60,120,10,70,80,40,50]),
  'policies': ('tax_rate', [.05,.15,.12,.18,.2,.1,.25,.12])},
 'factory': {
  'machines': ('cycle_sec', [4,3,2,15,6,5,20,10]),
  'belts': ('items_per_sec', [5,15,30,10,15,20,12,60]),
  'deposits': ('hardness', [3,3,2,4,1,10,8,2]),
  'research': ('unlock_tier', [1,3,5,7,9,15,10,12])},
 'space_trader': {
  'ships': ('cargo_tons', [10,1200,20,2000,50,30,1800,15]),
  'commodities': ('base_price', [30,60,800,500,150,100,1200,2000]),
  'ports': ('security', [.3,.5,.7,.9,1,.8,.1,.95]),
  'contracts': ('deadline_days', [20,10,40,2,30,5,15,25])},
 'stealth': {
  'guards': ('vision_angle_deg', [100,120,30,100,160,140,110,80]),
  'gadgets': ('duration_sec', [15,10,5,3,2,20,30,30]),
  'surfaces': ('noise_radius_px', [10,80,100,200,160,140,250,30]),
  'alert_states': ('speed_mult', [.5,.7,1,1.1,1.4,1.8,1.6,.8])},
 'horror': {
  'threats': ('speed_px_sec', [80,20,60,120,50,150,180,30]),
  'sanity_effects': ('threshold', [80,70,60,40,30,20,50,5]),
  'supplies': ('duration_sec', [600,3,180,30,5,60,10,2]),
  'rooms': ('light_level', [.4,.1,.2,.6,.3,.5,.1,1])},
 'visual_novel': {
  'characters': ('affinity_start', [15,-15,10,0,20,15,5,-20]),
  'choices': ('affinity_delta', [12,-8,2,20,-5,-10,5,15]),
  'scenes': ('affinity_required', [0,10,20,30,50,80,100,15]),
  'presentation': ('text_chars_sec', [40,30,35,25,60,20,30,50])},
 'dungeon_crawler': {
  'rooms': ('encounter_budget', [40,10,20,5,15,25,1,100]),
  'traps': ('damage', [20,10,30,5,40,1,2,1]),
  'doors': ('hp', [30,200,500,80,100,300,400,10]),
  'shrines': ('offering_cost', [50,100,100,200,300,5,150,500])},
 'metroidvania': {
  'abilities': ('range_px', [100,80,180,400,120,300,16,160]),
  'gates': ('damage_per_sec', [0,0,5,30,0,0,0,2]),
  'rooms': ('height_tiles', [60,8,20,16,10,8,40,24]),
  'upgrades': ('capacity_gain', [20,15,5,2,1,1,1,10])},
 'sports': {
  'athletes': ('speed_m_sec', [8,6,4,9,7,10,5,7]),
  'balls': ('mass_kg', [.43,.62,.27,.058,.145,.17,.046,.45]),
  'arenas': ('friction_mult', [.8,1,.9,.7,.1,1.2,.85,.95]),
  'training': ('stamina_cost', [40,50,20,15,35,10,5,20])},
 'naval': {
  'vessels': ('hull_hp', [100,400,1000,1800,3500,7000,800,10000]),
  'weapons': ('reload_sec', [5,40,30,15,60,1,20,8]),
  'sea_states': ('wave_height_m', [0,.3,1,2,4,8,.5,12]),
  'missions': ('duration_min', [40,20,60,15,10,30,25,50])},
 'flight': {
  'aircraft': ('cruise_speed_kph', [180,700,500,900,100,400,250,200]),
  'engines': ('thrust_n', [2000,80000,150000,30000,500,120000,5000,3000]),
  'weather': ('turbulence', [0,.3,.1,.1,.4,.5,1,.6]),
  'missions': ('distance_km', [50,800,200,100,500,2000,300,400])},
 'colony': {
  'colonists': ('work_speed_mult', [1.2,1.1,.9,1,.8,1.3,1.1,1.4]),
  'jobs': ('skill_required', [3,1,8,5,10,2,4,6]),
  'facilities': ('capacity', [2,10,5,4,6,30,20,10]),
  'incidents': ('severity', [8,6,7,1,2,5,9,10])},
 'restaurant': {
  'dishes': ('prep_sec', [30,10,90,60,80,45,40,120]),
  'staff': ('wage_per_hour', [35,25,15,18,10,20,12,40]),
  'equipment': ('cycle_sec', [30,180,90,60,5,20,25,15]),
  'customers': ('patience_sec', [180,120,240,150,100,60,300,30])},
 'idle': {
  'producers': ('output_per_sec', [.1,.5,2,8,30,100,400,1000]),
  'upgrades': ('output_mult', [2,1.5,1.1,1.8,2.5,3,1.2,1.3]),
  'prestige': ('exponent', [.5,.45,.4,.35,.6,.55,.3,.25]),
  'offline': ('cap_hours', [4,8,24,12,6,10,1,48])},
 'auto_battler': {
  'units': ('hp', [2000,600,700,500,650,1400,800,1000]),
  'synergies': ('units_required', [2,3,2,3,4,4,6,6]),
  'shop': ('unit_cost', [1,2,3,4,5,2,1,3]),
  'rounds': ('player_damage', [1,5,1,10,1,8,12,20])},
 'creature_collector': {
  'creatures': ('speed', [80,60,40,120,10,110,50,100,90,20]),
  'moves': ('power', [60,120,40,10,10,50,10,20]),
  'habitats': ('encounter_chance', [.3,.2,.15,.1,.4,.08,.25,.5]),
  'training': ('energy_cost', [30,25,40,20,15,5,35,20])},
}


def apply_profiles(specs):
    for (pack, dataset), spec in specs.items():
        field, anchors = ANCHORS[pack][dataset]
        assert len(anchors) == len(spec['archetypes']), (pack, dataset)
        bounds = next(f for f in spec['fields'] if f[0] == field)
        assert all(bounds[1] <= value <= bounds[2] for value in anchors), (pack, dataset, field)
        spec['anchors'] = {archetype: {field: value}
                           for archetype, value in zip(spec['archetypes'], anchors)}
