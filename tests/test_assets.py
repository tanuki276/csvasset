"""Regression tests for actual failure modes, using temporary external output trees."""
import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'generator'),str(ROOT/'tools')]
from generate_mass_assets import generate, make_row, sha, write_csv
from schema import SPECS
from validate_generated import read_csv, row_errors, validate
from validate_integrity import validate as validate_integrity
from validate_reference_assets import validate as validate_reference


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root/'generated'
        generate(self.out,100,37,123,['platformer'])

    def first_shard(self):
        _, manifest = read_csv(self.out/'manifest.csv')
        path = self.out/manifest[0]['file']
        return manifest,path

    def mutate_row(self, field, value):
        manifest,path = self.first_shard()
        header, rows = read_csv(path)
        rows[0][field] = value
        write_csv(path,header,rows)
        manifest[0]['sha256'] = sha(path)  # Test semantics even if the hash is updated.
        write_csv(self.out/'manifest.csv',list(manifest[0]),manifest)

    def test_complete_nondivisible_shards(self):
        self.assertEqual(validate(self.out)[0],[])
        _,manifest=read_csv(self.out/'manifest.csv')
        self.assertEqual([int(r['rows']) for r in manifest[:3]],[37,37,26])

    def test_reproducible_across_shard_boundaries(self):
        other=self.root/'other'
        generate(other,100,100,123,['platformer'])
        for key in [key for key in SPECS if key[0]=='platformer']:
            a=[]
            for file in sorted((self.out/key[0]/key[1]).glob('*.csv')):
                a.extend(read_csv(file)[1])
            b=read_csv(other/key[0]/key[1]/'part-00000.csv')[1]
            self.assertEqual(a,b)
        self.assertNotEqual(make_row('platformer','enemy_variants',0,123),
                            make_row('platformer','enemy_variants',0,124))

    def test_no_overwrite_or_recursive_deletion(self):
        sentinel=self.out/'keep.txt'
        sentinel.write_text('user file')
        with self.assertRaises(ValueError):
            generate(self.out,100,10)
        self.assertEqual(sentinel.read_text(),'user file')

    def test_invalid_arguments_leave_destination_absent(self):
        for rows,shards,packs in [(0,10,None),(99,10,None),(100,0,None),(100,-1,None),(100,10,['typo'])]:
            path=self.root/'absent'
            with self.assertRaises(ValueError):
                generate(path,rows,shards,1,packs)
            self.assertFalse(path.exists())

    def test_reject_symlink_destination(self):
        link=self.root/'link'
        link.symlink_to(self.out,target_is_directory=True)
        with self.assertRaises(ValueError):
            generate(link,100,10)

    def test_checksum_corruption(self):
        _,path=self.first_shard()
        with path.open('a') as f:
            f.write('garbage\n')
        self.assertTrue(validate(self.out)[0])

    def test_nan_and_out_of_bounds_rejected_with_valid_hash(self):
        self.mutate_row('hp','NaN')
        self.assertTrue(validate(self.out)[0])
        self.mutate_row('hp','999999')
        self.assertTrue(validate(self.out)[0])

    def test_changed_in_range_stat_fails_seed_verification(self):
        self.mutate_row('hp','5')
        self.assertTrue(any('regeneration' in x for x in validate(self.out)[0]))

    def test_duplicate_manifest_shard(self):
        manifest,_=self.first_shard()
        write_csv(self.out/'manifest.csv',list(manifest[0]),manifest+[manifest[0]])
        self.assertTrue(validate(self.out)[0])

    def test_missing_dataset_and_forged_counts(self):
        manifest,_=self.first_shard()
        manifest=manifest[3:]
        write_csv(self.out/'manifest.csv',list(manifest[0]),manifest)
        self.assertTrue(validate(self.out)[0])
        summary=json.loads((self.out/'summary.json').read_text())
        summary['dataset_count']=0
        (self.out/'summary.json').write_text(json.dumps(summary))
        self.assertTrue(validate(self.out)[0])

    def test_path_traversal_and_symlink(self):
        manifest,path=self.first_shard()
        canonical=manifest[0]['file']
        manifest[0]['file']='../outside.csv'
        write_csv(self.out/'manifest.csv',list(manifest[0]),manifest)
        self.assertTrue(validate(self.out)[0])
        # A canonical filename may still point outside via a symlink.
        manifest[0]['file']=canonical
        write_csv(self.out/'manifest.csv',list(manifest[0]),manifest)
        outside=self.root/'outside.csv'
        shutil.copy(path,outside)
        path.unlink()
        path.symlink_to(outside)
        self.assertTrue(any('unsafe path' in error for error in validate(self.out)[0]))

    def test_unknown_extra_csv_rejected(self):
        (self.out/'unlisted.csv').write_text('id\nextra\n')
        self.assertTrue(validate(self.out)[0])


class DomainTests(unittest.TestCase):
    def test_all_schema_rows_across_seeds(self):
        for seed in [-7,0,2762026]:
            for key,spec in SPECS.items():
                for index in range(100):
                    row={k:str(v) for k,v in make_row(*key,index,seed).items()}
                    self.assertEqual(row_errors(row,spec),[],(key,seed,index))

    def test_coupled_values_and_booleans(self):
        for index in range(1000):
            resource=make_row('survival','resource_variants',index,7)
            self.assertLessEqual(resource['yield_min'],resource['yield_max'])
            room=make_row('roguelike','encounter_variants',index,7)
            self.assertLessEqual(room['min_room_area'],room['max_room_area'])
            objective=make_row('puzzle','objective_variants',index,7)
            self.assertIn(objective['optional'],[0,1])
            self.assertIn(objective['fail_on_timeout'],[0,1])

    def test_formula_tampering(self):
        row={k:str(v) for k,v in make_row('platformer','movement_variants',0,7).items()}
        row['jump_height_px']='999'
        self.assertIn('jump_height_px: derived formula mismatch',row_errors(row,SPECS['platformer','movement_variants']))

    def test_role_profiles_affect_behavior(self):
        values={}
        for i in range(100):
            r=make_row('racing','surface_variants',i,7)
            values.setdefault(r['archetype'],[]).append(r['grip_mult'])
        self.assertLess(max(values['ice']),min(values['asphalt']))
        for i in range(100):
            r=make_row('platformer','enemy_variants',i,7)
            if r['archetype']=='turret':
                self.assertEqual(r['jump_power_px_sec'],0)

    def test_committed_references_and_authored_graph(self):
        self.assertEqual(validate_reference(),[])
        self.assertEqual(validate_integrity(),[])

    def test_authored_foreign_key_and_collision_corruption(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            shutil.copytree(ROOT/'packs/action_rpg',root/'packs/action_rpg')
            path=root/'packs/action_rpg/data/npc/npcs.csv'
            fields,rows=read_csv(path)
            rows[0]['shop_id']='missing_shop'
            rows[0]['x']='0'
            rows[0]['y']='0'
            write_csv(path,fields,rows)
            errors=validate_integrity(root)
            self.assertTrue(any('blocked/out-of-bounds' in e for e in errors))
            # shop reference must be checked as well as placement.
            self.assertTrue(any('missing_shop' in e for e in errors))

    def test_reference_preset_dangling_key(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'repo'
            shutil.copytree(ROOT/'catalog',root/'catalog')
            shutil.copytree(ROOT/'packs',root/'packs')
            path=root/'packs/farming/reference_presets.csv'
            fields,rows=read_csv(path)
            rows[0]['crops_id']='missing_crop'
            write_csv(path,fields,rows)
            self.assertTrue(any('dangling crops_id' in e for e in validate_reference(root)))


if __name__=='__main__':
    unittest.main()
