"""Typed, unit-bearing tuning domains. These are design candidates, not measured facts.

Field tuple: name, minimum, maximum, unit. Integer endpoints mean integer output.
Archetypes are scheduled evenly; tier/grade are independent design axes.
"""
from legacy_specs import PACKS as LEGACY

SPECS = {}
NEW_PACKS = {}


def dataset(pack, name, archetypes, fields, *, derived=None, ordered=(), profiles=None):
    SPECS[pack, name] = dict(archetypes=archetypes.split(), fields=fields,
                             derived=derived or {}, ordered=ordered, profiles=profiles or {})


def pack(pid, title, time_model, coordinate_model, definitions):
    NEW_PACKS[pid] = dict(title=title, time_model=time_model, coordinate_model=coordinate_model)
    for name, archetypes, fields in definitions:
        dataset(pid, name, archetypes, fields)


def unit(name):
    for suffix, value in [('_px_sec2', 'px/s^2'), ('_px_sec', 'px/s'), ('_tiles_sec', 'tile/s'),
                          ('_sec', 's'), ('_ms', 'ms'), ('_frames', 'frame'),
                          ('_turns', 'turn'), ('_tiles', 'tile'), ('_px', 'px'),
                          ('_kph', 'km/h'), ('_mps2', 'm/s^2'), ('_kg', 'kg')]:
        if name.endswith(suffix):
            return value
    if 'chance' in name or name in ('armor', 'curse_chance', 'logic_tolerance', 'damage_scale_end'):
        return 'ratio'
    if 'mult' in name or name.endswith('_bonus'):
        return 'multiplier'
    return 'design_unit'


for pid, datasets in LEGACY.items():
    for name, (archetypes, names, bounds) in datasets.items():
        fields = [(n, lo, hi, unit(n)) for n, (lo, hi) in zip(names.split(), bounds)]
        dataset(pid, name, archetypes, fields)

# Fix coupled quantities without changing the v1 column names.
SPECS['survival', 'resource_variants']['ordered'] = [('yield_min', 'yield_max')]
SPECS['roguelike', 'encounter_variants']['ordered'] = [('min_room_area', 'max_room_area')]
SPECS['platformer', 'movement_variants']['derived'] = {
    'jump_height_px': ('ballistic_height', 'jump_speed_px_sec', 'gravity_px_sec2'),
    'airtime_sec': ('ballistic_time', 'jump_speed_px_sec', 'gravity_px_sec2')}
SPECS['brawler', 'move_variants']['derived'] = {
    'total_frames': ('sum', 'startup_frames', 'active_frames', 'recovery_frames')}
SPECS['shmup', 'weapon_variants']['derived'] = {
    'nominal_dps': ('dps', 'damage', 'projectile_count', 'fire_interval_sec')}
SPECS['tower_defense', 'tower_variants']['derived'] = {
    'nominal_dps': ('quotient', 'damage', 'fire_interval_sec')}
SPECS['racing', 'vehicle_variants']['derived'] = {
    'ideal_0_to_100_sec': ('acceleration_time', 'accel_mps2')}

# Multipliers describe role tradeoffs; all outputs remain inside declared bounds.
SPECS['action_rpg', 'enemy_variants']['profiles'] = {
    'brute': {'hp': 1.4, 'damage': 1.35, 'move_speed_px_sec': .75},
    'tank': {'hp': 1.5, 'defense': 1.5, 'move_speed_px_sec': .65},
    'assassin': {'hp': .65, 'damage': 1.3, 'move_speed_px_sec': 1.4},
    'ranger': {'hp': .8, 'attack_range_tiles': 1.5},
    'caster': {'defense': .7, 'attack_range_tiles': 1.4}}
SPECS['tactics', 'unit_variants']['profiles'] = {
    'guardian': {'hp': 1.4, 'defense': 1.5, 'move_tiles': .7},
    'scout': {'hp': .75, 'defense': .7, 'move_tiles': 1.4},
    'mage': {'hp': .7, 'attack': 1.4, 'defense': .6},
    'healer': {'attack': .65, 'action_points': 1.2}}
SPECS['racing', 'vehicle_variants']['profiles'] = {
    'speed': {'max_speed_kph': 1.2, 'grip_mult': .85},
    'grip': {'max_speed_kph': .85, 'grip_mult': 1.25},
    'heavy': {'mass_kg': 1.3, 'accel_mps2': .75},
    'accel': {'max_speed_kph': .9, 'accel_mps2': 1.3},
    'drift': {'grip_mult': .85, 'drift_mult': 1.25}}

pack('farming', '農業・牧場', 'day_based', 'tile_grid', [
 ('crops', 'turnip potato carrot tomato corn pumpkin wheat rice strawberry grape', [('growth_days',2,28,'day'),('regrow_days',0,7,'day'),('seed_cost',5,200,'coin'),('harvest_value',15,600,'coin'),('water_per_day',1,4,'water_unit')]),
 ('livestock', 'chicken duck cow goat sheep alpaca rabbit bee', [('maturity_days',3,30,'day'),('feed_per_day',1,6,'feed_unit'),('produce_interval_days',1,7,'day'),('produce_value',20,450,'coin'),('purchase_cost',100,6000,'coin')]),
 ('soil', 'loam clay sand peat volcanic silt chalk compost', [('water_retention_mult',.4,1.6,'multiplier'),('growth_rate_mult',.7,1.3,'multiplier'),('fertility',0.0,1.0,'ratio'),('tilling_energy',1,12,'energy')]),
 ('seasons', 'spring summer autumn winter monsoon dry', [('duration_days',14,60,'day'),('rain_chance',0.0,.8,'probability'),('temperature_c',-15.0,38.0,'degC'),('daylight_hours',6.0,18.0,'hour')])])
pack('fishing', '釣り', 'realtime', 'water_2d', [
 ('fish', 'trout carp salmon bass tuna marlin eel catfish pike sardine', [('mass_kg',.1,80.0,'kg'),('bite_window_sec',.4,4.0,'s'),('stamina',10,500,'stamina'),('value',5,1800,'coin')]),
 ('rods', 'bamboo fiberglass carbon telescopic surf fly spinning heavy', [('tension_limit_n',15.0,800.0,'N'),('cast_range_m',5.0,90.0,'m'),('reel_speed_m_sec',.2,3.5,'m/s'),('durability',20,500,'use')]),
 ('lures', 'spinner spoon jig fly minnow popper worm baitfish', [('attraction_radius_m',1.0,12.0,'m'),('sink_speed_m_sec',0.0,1.0,'m/s'),('bite_chance',.05,.7,'probability'),('cost',2,150,'coin')]),
 ('waters', 'river lake pond coast reef estuary deep_sea marsh', [('depth_m',1.0,120.0,'m'),('current_m_sec',0.0,2.0,'m/s'),('clarity',.1,1.0,'ratio'),('spawn_weight',1,100,'weight')])])
pack('card_battler', 'カード戦闘', 'turn_based', 'board', [
 ('cards', 'strike block draw burn poison heal summon discard counter exhaust', [('energy_cost',0,5,'energy'),('power',1,30,'power'),('draw_count',0,3,'card'),('upgrade_cost',20,300,'coin')]),
 ('relics', 'thorns lifesteal energy draw armor discard poison summon', [('trigger_interval_turns',1,5,'turn'),('effect_power',1,12,'power'),('shop_cost',50,500,'coin')]),
 ('encounters', 'swarm bruiser sentinel ritualist duelist summoner elite boss', [('hp',20,400,'hp'),('attack',3,45,'damage'),('reward_gold',10,180,'coin'),('intent_cycle_turns',1,6,'turn')]),
 ('events', 'shrine merchant healer gamble sacrifice library forge treasure', [('gold_cost',0,200,'coin'),('hp_cost',0,20,'hp'),('reward_power',1,20,'power'),('weight',1,50,'weight')])])
pack('rhythm', 'リズム', 'audio_clock', 'lane_2d', [
 ('timing_windows', 'beginner casual standard strict expert master', [('perfect_ms',15,90,'ms'),('great_ms',35,130,'ms'),('good_ms',70,200,'ms'),('miss_ms',100,250,'ms')]),
 ('charts', 'four_lane six_lane seven_lane drum guitar dance touch taiko', [('bpm',60,240,'beat/min'),('duration_sec',30,300,'s'),('notes_per_beat',.25,4.0,'note/beat'),('scroll_px_sec',120,900,'px/s')]),
 ('notes', 'tap hold slide flick mine roll trace scratch', [('score_base',100,1000,'point'),('hold_duration_beats',0.0,8.0,'beat'),('health_delta',-10,5,'health'),('combo_weight',1,4,'count')]),
 ('scoring', 'accuracy combo survival dance tournament marathon practice challenge', [('perfect_points',500,1000,'point'),('great_points',200,500,'point'),('good_points',50,200,'point'),('miss_penalty',0,1000,'point')])])
pack('city_builder', '都市建設', 'fixed_tick', 'tile_grid', [
 ('buildings', 'residential commercial industrial civic hospital school park station', [('build_cost',100,20000,'coin'),('capacity',5,500,'person'),('power_kw',1.0,200.0,'kW'),('upkeep_per_day',1,200,'coin/day')]),
 ('utilities', 'solar wind coal gas hydro battery water sewage', [('capacity_kw',10.0,5000.0,'kW'),('build_cost',1000,100000,'coin'),('emissions_kg_day',0.0,2000.0,'kg/day'),('upkeep_per_day',5,1000,'coin/day')]),
 ('roads', 'street avenue highway alley bridge tunnel tram boulevard', [('capacity_vehicles_hour',100,6000,'vehicle/hour'),('speed_kph',10,120,'km/h'),('cost_per_tile',10,2000,'coin/tile')]),
 ('policies', 'tax_relief green_energy tourism education healthcare transit zoning recycling', [('tax_rate',0.0,.3,'ratio'),('happiness_delta',-20,20,'point'),('upkeep_per_day',10,1000,'coin/day')])])
pack('factory', '工場自動化', 'fixed_tick', 'tile_grid', [
 ('machines', 'smelter assembler crusher refinery loom press centrifuge recycler', [('cycle_sec',.5,30.0,'s'),('input_qty',1,8,'item'),('output_qty',1,6,'item'),('power_kw',5.0,500.0,'kW')]),
 ('belts', 'basic fast express armored underground splitter filter stacker', [('items_per_sec',1.0,60.0,'item/s'),('power_kw',0.0,5.0,'kW'),('cost_per_tile',1,100,'coin/tile')]),
 ('deposits', 'iron copper coal stone oil uranium crystal sulfur', [('richness',100,100000,'item'),('mining_sec',.2,10.0,'s'),('hardness',1,10,'rank')]),
 ('research', 'logistics metallurgy automation energy chemistry robotics circuits recycling', [('science_cost',10,5000,'science'),('duration_sec',10,1200,'s'),('unlock_tier',1,20,'tier')])])
pack('space_trader', '宇宙交易', 'realtime', 'sector_2d', [
 ('ships', 'shuttle freighter courier tanker explorer escort hauler yacht', [('cargo_tons',5,2000,'t'),('fuel_capacity',20,1000,'fuel_unit'),('jump_range_ly',1.0,20.0,'ly'),('hull_hp',50,5000,'hp')]),
 ('commodities', 'food ore medicine machinery fuel textiles electronics luxury', [('base_price',10,2000,'coin/t'),('volatility',.01,.4,'ratio'),('mass_tons',.1,10.0,'t'),('legality_rank',0,3,'rank')]),
 ('ports', 'mining agricultural industrial research military tourist frontier hub', [('docking_fee',0,1000,'coin'),('market_capacity',100,20000,'t'),('security',0.0,1.0,'ratio')]),
 ('contracts', 'delivery escort survey rescue salvage courier patrol bounty', [('distance_ly',1.0,100.0,'ly'),('deadline_days',2,60,'day'),('reward',100,50000,'coin'),('reputation_required',0,100,'point')])])
pack('stealth', 'ステルス', 'realtime', 'world_2d', [
 ('guards', 'patrol sentry sniper handler camera drone elite civilian', [('vision_range_px',80,600,'px'),('vision_angle_deg',30,160,'degree'),('hearing_radius_px',40,400,'px'),('reaction_sec',.2,3.0,'s')]),
 ('gadgets', 'smoke decoy emp lockpick noise_dart cloak camera_mine tripwire', [('duration_sec',1.0,30.0,'s'),('radius_px',16,200,'px'),('cooldown_sec',2.0,90.0,'s'),('charges',1,8,'count')]),
 ('surfaces', 'carpet wood stone metal gravel water glass grass', [('noise_radius_px',10,250,'px'),('speed_mult',.4,1.2,'multiplier'),('visibility_mult',.3,1.3,'multiplier')]),
 ('alert_states', 'idle suspicious searching investigating alerted combat lockdown cooldown', [('duration_sec',2.0,120.0,'s'),('speed_mult',.5,1.8,'multiplier'),('reinforcement_delay_sec',5.0,120.0,'s')])])
pack('horror', 'ホラー探索', 'realtime', 'world_2d', [
 ('threats', 'stalker watcher crawler phantom mimic swarm hunter lurker', [('speed_px_sec',20,180,'px/s'),('detection_radius_px',50,500,'px'),('damage',5,80,'hp'),('stun_sec',.2,8.0,'s')]),
 ('sanity_effects', 'whispers blur tremor hallucination panic tunnel_vision echo blackout', [('threshold',5,90,'sanity'),('duration_sec',2.0,40.0,'s'),('intensity',.1,1.0,'ratio')]),
 ('supplies', 'battery bandage candle flare antidote sedative match ration', [('uses',1,6,'count'),('duration_sec',1.0,600.0,'s'),('inventory_slots',1,4,'slot'),('spawn_weight',1,100,'weight')]),
 ('rooms', 'corridor basement attic ward chapel library vault safe_room', [('light_level',0.0,1.0,'ratio'),('noise_floor',0.0,1.0,'ratio'),('threat_weight',1,100,'weight'),('search_sec',1.0,30.0,'s')])])
pack('visual_novel', 'ビジュアルノベル', 'event_based', 'screen_2d', [
 ('characters', 'friend rival mentor stranger partner sibling guardian antagonist', [('affinity_start',-20,20,'point'),('trust_start',0,50,'point'),('route_priority',1,10,'rank')]),
 ('choices', 'support challenge investigate confess conceal leave negotiate comfort', [('affinity_delta',-15,20,'point'),('trust_delta',-10,15,'point'),('time_cost_min',0,120,'minute')]),
 ('scenes', 'introduction conflict discovery bonding turning_point climax epilogue interlude', [('reading_time_sec',30,600,'s'),('affinity_required',0,100,'point'),('priority',1,10,'rank')]),
 ('presentation', 'dialogue narration thought flashback phone letter monologue choice', [('text_chars_sec',15,90,'char/s'),('auto_wait_sec',.5,5.0,'s'),('fade_sec',.1,2.0,'s')])])
pack('dungeon_crawler', 'ダンジョン探索', 'turn_based', 'tile_grid', [
 ('rooms', 'combat treasure trap shrine library prison fountain boss', [('width_tiles',3,15,'tile'),('height_tiles',3,15,'tile'),('encounter_budget',1,100,'point')]),
 ('traps', 'spike dart pit gas flame alarm snare teleport', [('damage',1,60,'hp'),('detect_dc',5,25,'DC'),('disarm_dc',5,25,'DC'),('reset_turns',0,10,'turn')]),
 ('doors', 'wood iron stone locked secret portcullis magical cracked', [('hp',10,500,'hp'),('lock_dc',0,30,'DC'),('noise_radius_tiles',1,12,'tile')]),
 ('shrines', 'healing strength wisdom fortune sacrifice curse cleansing resurrection', [('offering_cost',5,500,'coin'),('effect_turns',1,100,'turn'),('power',1,30,'power')])])
pack('metroidvania', '探索アクション', 'realtime', 'pixel_2d', [
 ('abilities', 'double_jump wall_jump dash grapple swim glide morph charge', [('cooldown_sec',.1,5.0,'s'),('energy_cost',0,30,'energy'),('range_px',16,400,'px')]),
 ('gates', 'high_ledge narrow_tunnel water heat dark breakable grapple_point wind', [('threshold_rank',1,5,'rank'),('damage_per_sec',0,30,'hp/s'),('width_px',16,160,'px')]),
 ('rooms', 'shaft corridor hub arena save_room secret traversal boss', [('width_tiles',10,80,'tile'),('height_tiles',8,60,'tile'),('enemy_budget',1,100,'point')]),
 ('upgrades', 'health energy missile armor speed map radar recovery', [('capacity_gain',1,30,'capacity'),('pickup_radius_px',8,64,'px'),('rarity_weight',1,100,'weight')])])
pack('sports', 'スポーツ', 'fixed_tick', 'field_2d', [
 ('athletes', 'striker defender keeper winger playmaker sprinter anchor allrounder', [('speed_m_sec',3.0,10.0,'m/s'),('stamina',40,100,'point'),('accuracy',.3,.95,'probability'),('strength',20,100,'point')]),
 ('balls', 'football basketball volleyball tennis baseball hockey golf rugby', [('mass_kg',.04,.7,'kg'),('restitution',.3,.9,'ratio'),('drag_mult',.01,.2,'multiplier')]),
 ('arenas', 'grass turf hardwood clay ice sand indoor street', [('length_m',20.0,110.0,'m'),('width_m',10.0,75.0,'m'),('friction_mult',.1,1.2,'multiplier')]),
 ('training', 'sprint endurance shooting passing tackling positioning recovery technique', [('duration_min',10,120,'minute'),('stamina_cost',5,50,'point'),('skill_gain',.1,3.0,'point')])])
pack('naval', '海戦', 'fixed_tick', 'sea_2d', [
 ('vessels', 'patrol corvette frigate destroyer cruiser carrier submarine battleship', [('hull_hp',100,10000,'hp'),('speed_knots',10.0,45.0,'knot'),('turn_deg_sec',1.0,15.0,'degree/s'),('armor_mult',.1,.8,'ratio')]),
 ('weapons', 'cannon torpedo missile depth_charge mine flak railgun rocket', [('damage',20,1000,'hp'),('reload_sec',1.0,60.0,'s'),('range_m',100,20000,'m')]),
 ('sea_states', 'calm breeze chop swell rough storm fog hurricane', [('wave_height_m',0.0,12.0,'m'),('visibility_m',100,20000,'m'),('speed_mult',.3,1.0,'multiplier')]),
 ('missions', 'convoy patrol blockade rescue interception escort reconnaissance siege', [('duration_min',5,60,'minute'),('enemy_budget',10,1000,'point'),('reward',100,10000,'coin')])])
pack('flight', '飛行', 'fixed_tick', 'air_2d', [
 ('aircraft', 'trainer fighter bomber interceptor glider cargo scout seaplane', [('mass_kg',300,30000,'kg'),('stall_speed_kph',45,250,'km/h'),('cruise_speed_kph',100,900,'km/h'),('fuel_capacity_l',20,10000,'L')]),
 ('engines', 'piston turbojet turbofan turboprop electric ramjet radial rotary', [('thrust_n',500,150000,'N'),('fuel_l_hour',5.0,5000.0,'L/hour'),('mass_kg',20,3000,'kg')]),
 ('weather', 'clear crosswind headwind tailwind rain snow storm thermal', [('wind_m_sec',0.0,35.0,'m/s'),('visibility_m',500,50000,'m'),('turbulence',0.0,1.0,'ratio')]),
 ('missions', 'training delivery rescue dogfight bombing survey race patrol', [('distance_km',10,2000,'km'),('time_limit_min',10,180,'minute'),('reward',100,20000,'coin')])])
pack('colony', 'コロニー運営', 'fixed_tick', 'tile_grid', [
 ('colonists', 'builder farmer doctor soldier scientist miner cook engineer', [('work_speed_mult',.6,1.5,'multiplier'),('hunger_per_day',1.0,3.0,'ration/day'),('morale',20,100,'point')]),
 ('jobs', 'construct harvest heal defend research mine cook repair', [('work_units',5,500,'work'),('skill_required',0,10,'rank'),('priority',1,9,'rank')]),
 ('facilities', 'bedroom kitchen clinic laboratory workshop greenhouse barracks warehouse', [('capacity',1,30,'person'),('build_cost',20,1000,'material'),('power_kw',.1,50.0,'kW')]),
 ('incidents', 'raid blight fire trader refugee storm disease meteor', [('severity',1,10,'rank'),('duration_hours',1,72,'hour'),('weight',1,100,'weight')])])
pack('restaurant', 'レストラン経営', 'realtime', 'tile_grid', [
 ('dishes', 'soup salad steak pasta sushi curry burger dessert', [('prep_sec',5,120,'s'),('ingredient_cost',2,40,'coin'),('sale_price',5,100,'coin'),('quality',1,5,'rank')]),
 ('staff', 'chef sous_chef waiter host dishwasher barista cashier manager', [('speed_mult',.6,1.5,'multiplier'),('wage_per_hour',8,40,'coin/hour'),('stamina',30,100,'point')]),
 ('equipment', 'stove oven grill fryer refrigerator mixer espresso sink', [('capacity',1,8,'dish'),('cycle_sec',5,180,'s'),('purchase_cost',100,10000,'coin')]),
 ('customers', 'regular tourist critic family student business gourmet impatient', [('patience_sec',30,300,'s'),('budget',10,150,'coin'),('tip_chance',.05,.9,'probability')])])
pack('idle', '放置・インクリメンタル', 'elapsed_time', 'abstract', [
 ('producers', 'miner lumberjack farmer workshop factory lab portal reactor', [('base_cost',10,100000,'coin'),('output_per_sec',.1,1000.0,'coin/s'),('cost_growth_mult',1.05,1.25,'multiplier')]),
 ('upgrades', 'efficiency automation storage speed synergy critical discount offline', [('cost',100,1000000,'coin'),('output_mult',1.1,3.0,'multiplier'),('required_level',1,100,'level')]),
 ('prestige', 'reset ascension rebirth transcendence legacy evolution awakening eternity', [('threshold',10000,100000000,'coin'),('reward_mult',1.1,5.0,'multiplier'),('exponent',.2,.7,'exponent')]),
 ('offline', 'casual standard premium expedition rest reserve capped extended', [('cap_hours',1,48,'hour'),('efficiency',.1,1.0,'ratio'),('claim_bonus_mult',1.0,1.5,'multiplier')])])
pack('auto_battler', 'オートバトラー', 'round_based', 'hex_grid', [
 ('units', 'tank assassin ranger mage support bruiser summoner duelist', [('hp',300,2000,'hp'),('attack',20,150,'damage'),('attack_interval_sec',.5,2.0,'s'),('mana_cost',20,150,'mana')]),
 ('synergies', 'guardian mystic ranger rogue beast machine celestial infernal', [('units_required',2,6,'count'),('attack_bonus',.05,.6,'ratio'),('health_bonus',.05,.6,'ratio')]),
 ('shop', 'common uncommon rare epic legendary reroll economy streak', [('unit_cost',1,5,'coin'),('offer_weight',1,100,'weight'),('unlock_level',1,9,'level')]),
 ('rounds', 'pve pvp carousel boss treasure duel elite finale', [('duration_sec',20,90,'s'),('base_gold',2,10,'coin'),('player_damage',1,20,'hp')])])
pack('creature_collector', '育成・収集', 'turn_based', 'world_2d', [
 ('creatures', 'fire water leaf electric stone wind ice shadow light metal', [('base_hp',30,150,'hp'),('attack',10,120,'point'),('defense',10,120,'point'),('speed',10,120,'point')]),
 ('moves', 'strike blast drain buff debuff heal shield trap', [('power',10,120,'power'),('accuracy',.5,1.0,'probability'),('uses',5,40,'count')]),
 ('habitats', 'forest lake mountain desert cave tundra coast ruins', [('encounter_chance',.05,.5,'probability'),('min_level',1,60,'level'),('max_level',5,100,'level')]),
 ('training', 'strength agility endurance defense focus bonding exploration technique', [('duration_min',5,120,'minute'),('stat_gain',1,12,'point'),('energy_cost',5,40,'energy')])])

# Existing packs gain actual new systems, not just more variants of the same tables.
EXTRA = {
 'action_rpg': [('companions','healer guardian archer mage wolf golem sprite falcon',[('hp',30,300,'hp'),('follow_distance_tiles',1,5,'tile'),('assist_cooldown_sec',1.0,15.0,'s')]),('weather','clear rain snow fog storm heat ash aurora',[('visibility_mult',.3,1.0,'multiplier'),('move_speed_mult',.6,1.1,'multiplier'),('duration_sec',30,600,'s')])],
 'platformer': [('moving_platforms','horizontal vertical orbit pendulum falling conveyor elevator bounce',[('speed_px_sec',20,220,'px/s'),('travel_px',32,512,'px'),('pause_sec',0.0,3.0,'s')]),('grapple_points','fixed moving timed fragile swing retract magnetic chain',[('radius_px',8,32,'px'),('reach_px',80,400,'px'),('release_boost_px_sec',0,250,'px/s')])],
 'shmup': [('bullet_patterns','radial aimed spiral fan ring wave cross random',[('bullet_count',3,48,'count'),('angular_speed_deg_sec',0.0,180.0,'degree/s'),('speed_px_sec',60,500,'px/s'),('interval_sec',.2,5.0,'s')]),('boss_phases','opening sweep aimed barrage summon enrage retreat finale',[('hp_threshold',.05,1.0,'ratio'),('duration_sec',5,60,'s'),('score_bonus',100,10000,'point')])],
 'roguelike': [('room_events','altar gamble rescue curse fountain forge portal sacrifice',[('risk',.05,.9,'probability'),('reward_budget',5,100,'point'),('weight',1,50,'weight')]),('mutators','darkness haste famine abundance elite_swarm fragile chaos mirror',[('threat_mult',.5,2.0,'multiplier'),('reward_mult',.5,2.0,'multiplier'),('weight',1,40,'weight')])],
 'tactics': [('formations','line wedge square flank column scatter shield_wall pincer',[('spacing_tiles',1,4,'tile'),('defense_bonus',0.0,.3,'ratio'),('move_cost_ap',1,4,'AP'),('command_delay_sec',.1,2.0,'s')]),('reactions','overwatch counter intercept parry riposte assist suppress evade',[('range_tiles',1,8,'tile'),('trigger_chance',.2,1.0,'probability'),('ap_cost',1,3,'AP')])],
 'survival': [('weather','clear rain blizzard heatwave sandstorm fog thunderstorm drought',[('temperature_c',-30.0,45.0,'degC'),('exposure_per_sec',0.0,2.0,'exposure/s'),('duration_sec',30,1200,'s')]),('diseases','cold fever poisoning infection fatigue dehydration hypothermia parasite',[('duration_sec',30,900,'s'),('damage_per_sec',0.0,1.5,'hp/s'),('recovery_chance',.01,.2,'probability')])],
 'tower_defense': [('status_effects','slow burn poison stun armor_break vulnerability freeze mark',[('duration_sec',.2,10.0,'s'),('potency',.05,.8,'ratio'),('max_stacks',1,8,'count')]),('targeting','first last strongest weakest nearest fastest armored flying',[('switch_delay_sec',0.0,.5,'s'),('retarget_radius_tiles',1,12,'tile'),('priority_weight',1,100,'weight')])],
 'racing': [('tires','slick sport touring rain snow gravel drift endurance',[('dry_grip_mult',.6,1.5,'multiplier'),('wet_grip_mult',.3,1.3,'multiplier'),('wear_per_km',.001,.02,'ratio/km')]),('race_rules','sprint circuit endurance drift time_trial elimination rally pursuit',[('laps',1,50,'lap'),('time_limit_sec',60,7200,'s'),('penalty_sec',1,30,'s')])],
 'puzzle': [('generators','corridor rooms maze symmetry spiral islands clusters rings',[('width_tiles',5,30,'tile'),('height_tiles',5,30,'tile'),('obstacle_density',.05,.4,'ratio')]),('hints','highlight nudge undo path reveal preview explain checkpoint',[('cooldown_sec',0.0,30.0,'s'),('cost',0,100,'coin'),('max_uses',1,10,'count')])],
 'brawler': [('throws','forward backward suplex slam toss aerial wall ground',[('damage',5,60,'hp'),('range_px',12,64,'px'),('recovery_frames',10,50,'frame')]),('defense','block parry dodge roll counter armor reflect escape',[('startup_frames',1,10,'frame'),('active_frames',2,20,'frame'),('recovery_frames',4,30,'frame'),('stamina_cost',5,30,'stamina')])],
}
for pid, definitions in EXTRA.items():
    for name, archetypes, fields in definitions:
        dataset(pid, name, archetypes, fields)

for key, pairs in {
    ('rhythm','timing_windows'): [('perfect_ms','great_ms'),('great_ms','good_ms'),('good_ms','miss_ms')],
    ('rhythm','scoring'): [('good_points','great_points'),('great_points','perfect_points')],
    ('flight','aircraft'): [('stall_speed_kph','cruise_speed_kph')],
    ('restaurant','dishes'): [('ingredient_cost','sale_price')],
    ('creature_collector','habitats'): [('min_level','max_level')],
}.items():
    SPECS[key]['ordered'] = pairs
SPECS['rhythm','charts']['derived'] = {'estimated_notes': ('notes','bpm','duration_sec','notes_per_beat')}
SPECS['factory','machines']['derived'] = {'output_per_sec': ('quotient','output_qty','cycle_sec')}
SPECS['idle','producers']['derived'] = {'base_payback_sec': ('quotient','base_cost','output_per_sec')}
SPECS['auto_battler','units']['derived'] = {'nominal_dps': ('quotient','attack','attack_interval_sec')}

from archetype_profiles import apply_profiles
apply_profiles(SPECS)
