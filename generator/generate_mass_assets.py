#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,math,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PACKS={
"action_rpg":{
 "enemy_variants":("brute skirmisher ranger caster tank assassin","hp damage defense move_speed_px_sec attack_range_tiles",[(60,160),(8,35),(1,20),(55,150),(1,7)]),
 "item_variants":("sword axe bow staff armor ring potion","power attack_speed_mult crit_chance value stack_max",[(5,45),(.7,1.3),(0,.18),(10,2500),(1,50)]),
 "skill_variants":("melee projectile aoe dash heal control","power cooldown_sec cost range_tiles effect_rank",[(5,55),(.15,6),(0,40),(0,8),(1,6)])},
"platformer":{
 "enemy_variants":("walker hopper flyer charger turret crusher","hp contact_damage move_speed_px_sec patrol_range_px jump_power_px_sec",[(1,18),(8,70),(0,180),(64,512),(0,620)]),
 "hazard_variants":("spikes lava saw crusher laser falling_block","damage active_sec inactive_sec move_speed_px_sec telegraph_ms",[(5,80),(.2,8),(0,5),(0,260),(150,1000)]),
 "movement_variants":("tight floaty speed heavy precision","max_speed_px_sec acceleration_px_sec2 jump_speed_px_sec gravity_px_sec2 coyote_ms",[(160,340),(650,1700),(320,560),(850,1500),(60,220)])},
"shmup":{
 "enemy_variants":("drone interceptor bomber sniper carrier mini_boss","hp speed_px_sec fire_interval_sec projectile_speed_px_sec score",[(10,900),(35,210),(.15,4),(100,520),(50,9000)]),
 "weapon_variants":("straight spread laser missile orbital piercing","damage fire_interval_sec projectile_speed_px_sec projectile_count energy_cost",[(2,60),(.04,1),(180,950),(1,7),(0,12)]),
 "wave_variants":("line vee arc swarm escort boss_intro","enemy_count duration_sec spawn_interval_sec intensity path_rank",[(3,45),(4,45),(.1,1.4),(.2,1.5),(1,5)])},
"roguelike":{
 "item_variants":("weapon armor trinket consumable relic tool","power curse_chance shop_value pool_weight rarity_rank",[(3,70),(0,.2),(10,5000),(1,100),(0,4)]),
 "affix_variants":("damage speed health crit armor cooldown risk_reward","value is_multiplier weight rarity_rank risk_score",[(-.4,.5),(0,1),(1,100),(0,4),(0,1)]),
 "encounter_variants":("combat elite treasure shop event rest","threat_budget reward_budget min_room_area max_room_area weight",[(1,80),(1,100),(16,120),(24,260),(1,100)])},
"tactics":{
 "unit_variants":("vanguard archer mage healer scout guardian","hp attack defense move_tiles action_points",[(30,240),(6,55),(1,35),(3,9),(2,10)]),
 "ability_variants":("strike shot blast heal guard dash debuff","power range_tiles area_tiles ap_cost cooldown_turns",[(3,65),(1,8),(0,3),(1,6),(0,4)]),
 "terrain_variants":("plain forest ruins water mud high_ground hazard","move_cost defense_bonus accuracy_bonus damage_per_turn traversal_mult",[(1,4),(-.1,.3),(-.15,.2),(0,30),(.5,1.1)])},
"survival":{
 "resource_variants":("wood stone fiber metal food herb fuel","harvest_time_sec yield_min yield_max stack_max value",[(.3,12),(1,6),(2,16),(20,500),(1,300)]),
 "recipe_variants":("tool weapon food medicine building_part utility","ingredient_count craft_time_sec station_level output_qty tech_cost",[(1,6),(1,40),(1,5),(1,8),(5,4000)]),
 "structure_variants":("wall door storage workbench turret generator bed","hp build_cost power_draw storage_slots repair_efficiency",[(40,900),(5,600),(-30,15),(0,80),(.4,1.2)])},
"tower_defense":{
 "tower_variants":("cannon rapid sniper splash slow beam","damage fire_interval_sec range_tiles build_cost special_rank",[(2,90),(.05,2),(2,10),(25,1200),(1,6)]),
 "enemy_variants":("grunt fast tank shield flying boss","hp speed_tiles_sec armor bounty lives_damage",[(15,1800),(.25,2.2),(0,.5),(2,200),(1,15)]),
 "wave_variants":("standard rush tank_push air mixed boss","enemy_count spawn_interval_sec budget reward break_after_sec",[(5,80),(.12,1.2),(10,250),(10,500),(3,20)])},
"racing":{
 "vehicle_variants":("balanced speed grip drift heavy accel","max_speed_kph accel_mps2 grip_mult drift_mult mass_kg",[(130,290),(4,14),(.6,1.35),(.55,1.35),(650,1600)]),
 "surface_variants":("asphalt gravel dirt ice wet sand","grip_mult rolling_resistance damage_chance visibility_mult roughness",[(.3,1.2),(.8,1.5),(0,.05),(.65,1.05),(0,1)]),
 "upgrade_variants":("engine tires suspension brakes gearbox weight_reduction","stat_gain downside install_cost required_tier efficiency",[(-.02,.35),(-.06,.02),(50,12000),(1,20),(.5,1.4)])},
"puzzle":{
 "level_variants":("sokoban match route switch block_push logic","width height objective_count move_par solution_depth",[(5,30),(5,30),(1,8),(8,120),(5,90)]),
 "mechanic_variants":("push toggle teleport rotate gravity color_lock timed","complexity interaction_radius state_count cooldown_turns logic_tolerance",[(1,7),(1,3),(2,6),(0,4),(.05,.65)]),
 "objective_variants":("reach collect clear activate survive_moves optimize","target_count move_limit optional score_weight fail_on_timeout",[(1,20),(0,140),(0,1),(.7,2),(0,1)])},
"brawler":{
 "fighter_variants":("balanced rushdown grappler zoner tank counter","hp attack_mult defense_mult move_speed_mult meter_gain_mult",[(60,260),(.7,1.5),(.7,1.5),(.6,1.4),(.7,1.5)]),
 "move_variants":("jab heavy launcher sweep special grab air","damage startup_frames active_frames recovery_frames knockback_mult",[(3,55),(2,25),(1,10),(4,35),(.2,1.7)]),
 "combo_variants":("ground air launcher corner meter grab","hit_count execution_window_frames damage_scale_end meter_cost difficulty",[(2,12),(2,14),(.45,.9),(0,60),(1,8)])}}

def u(seed,*parts):
 h=hashlib.blake2b("|".join(map(str,(seed,*parts))).encode(),digest_size=8).digest()
 return int.from_bytes(h,"big")/((1<<64)-1)
def pick(seed,key,s):
 a=s.split();return a[min(int(u(seed,key)*len(a)),len(a)-1)]
def val(seed,key,lo,hi,tier,grade):
 q=u(seed,key)
 if isinstance(lo,int) and isinstance(hi,int):
  return int(round(lo+(hi-lo)*min(1,(tier-1)/24+grade*.06+q*.25)))
 return round(lo+(hi-lo)*min(1,(tier-1)/24+grade*.06+q*.25),6)
def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--out",type=Path,default=ROOT/"generated")
 ap.add_argument("--rows-per-dataset",type=int,default=10000)
 ap.add_argument("--shard-rows",type=int,default=5000)
 ap.add_argument("--seed",type=int,default=2762026)
 a=ap.parse_args()
 if a.out.exists():shutil.rmtree(a.out)
 a.out.mkdir(parents=True)
 manifest=[];total=0
 for pack,dsmap in PACKS.items():
  for ds,(arches,fields,ranges) in dsmap.items():
   cols=["id","tier","grade","seed_key","archetype","tuning_bias",*fields.split()]
   d=a.out/pack/ds;d.mkdir(parents=True)
   for start in range(0,a.rows_per_dataset,a.shard_rows):
    end=min(start+a.shard_rows,a.rows_per_dataset);p=d/f"part-{start//a.shard_rows:05d}.csv"
    with p.open("w",encoding="utf-8",newline="") as f:
     w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
     for i in range(start,end):
      tier=i%20+1;grade=(i//20)%5
      row={"id":f"{pack}_{ds}_{i+1:06d}","tier":tier,"grade":grade,"seed_key":f"{a.seed}:{i+1}","archetype":pick(a.seed,(pack,ds,i),arches),"tuning_bias":round((u(a.seed,pack,ds,"bias",i)-.5)*.1,7)}
      for j,(name,(lo,hi)) in enumerate(zip(fields.split(),ranges)):
       row[name]=val(a.seed,(pack,ds,name,i),lo,hi,tier,grade)
      w.writerow(row)
    manifest.append({"pack":pack,"dataset":ds,"file":p.relative_to(a.out).as_posix(),"rows":end-start,"sha256":sha(p)});total+=end-start
 with (a.out/"manifest.csv").open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=["pack","dataset","file","rows","sha256"]);w.writeheader();w.writerows(manifest)
 summary={"generator_version":"1.0.0","seed":a.seed,"dataset_count":sum(map(len,PACKS.values())),"rows_per_dataset":a.rows_per_dataset,"total_rows":total,"shard_rows":a.shard_rows,"tiers":20,"packs":sorted(PACKS)}
 (a.out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(summary))
if __name__=="__main__":main()
