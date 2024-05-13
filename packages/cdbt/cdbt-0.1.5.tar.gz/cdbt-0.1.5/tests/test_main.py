import unittest
from unittest.mock import patch
import json
from cdbt.main import ColdBoreCapitalDBT, MockCtx


class TestCdbt(unittest.TestCase):
    def setUp(self):
        self.cdbt = ColdBoreCapitalDBT()
        self.cdbt.test_mode = True
        self.incremental_ls_example = '''22:06:42 Running with dbt=1.7.9
22:06:43 Registered adapter: snowflake=1.7.2
22:06:43 Found 123 models, 26 snapshots, 118 tests, 9 seeds, 46 sources, 0 exposures, 0 metrics, 992 macros, 0 groups, 0 semantic models
{"name": "dim_patients", "resource_type": "model", "config": {"materialized": "incremental"}}'''

        self.non_incremental_ls_example = '''22:06:42 Running with dbt=1.7.9
22:06:43 Registered adapter: snowflake=1.7.2
22:06:43 Found 123 models, 26 snapshots, 118 tests, 9 seeds, 46 sources, 0 exposures, 0 metrics, 992 macros, 0 groups, 0 semantic models
{"name": "dim_patients", "resource_type": "model", "config": {"materialized": "view"}}'''

    def test_build_command_full_refresh(self):
        self.cdbt.build(full_refresh=True, select="model1", fail_fast=True)
        expected_command = ['dbt', 'build', '--select', 'model1', '--fail-fast', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_build_command_no_full_refresh(self):
        self.cdbt.build(full_refresh=False, select="model1", fail_fast=False)
        expected_command = ['dbt', 'build', '--select', 'model1']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_trun_command(self):
        self.cdbt.trun(full_refresh=True, select="model2", fail_fast=False)
        expected_command = ['dbt', 'build', '--exclude', 'resource_type:snapshot resource_type:seed', '--select',
                            'model2', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_run_command_full_refresh(self):
        self.cdbt.run(full_refresh=True, select="model3", fail_fast=True)
        expected_command = ['dbt', 'run', '--select', 'model3', '--fail-fast', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_test_command_selective(self):
        self.cdbt.test(select="model4", fail_fast=True)
        expected_command = ['dbt', 'test', '--select', 'model4', '--fail-fast']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_compile_command(self):
        self.cdbt.compile()
        expected_command = ['dbt', 'compile']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_sbuild_output(self):
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        self.cdbt.sbuild(ctx=MockCtx(), full_refresh=False)
        expected_command = ['dbt', 'build', '--select', 'state:modified', '--state', './_artifacts/', '--exclude', 'resource_type:snapshot resource_type:seed', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

        # Test build parents
        mc = MockCtx()
        mc.obj['build_parents'] = True
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        self.cdbt.sbuild(ctx=mc, full_refresh=False)
        expected_command = ['dbt', 'build', '--select', '+state:modified', '--state', './_artifacts/', '--exclude', 'resource_type:snapshot resource_type:seed', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

        # Test build parents graph count limit (i.e. 3+sbuild)
        mc = MockCtx()
        mc.obj['build_parents'] = True
        mc.obj['build_parents_count'] = 3
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        self.cdbt.sbuild(ctx=mc, full_refresh=False)
        expected_command = ['dbt', 'build', '--select', '3+state:modified', '--state', './_artifacts/', '--exclude', 'resource_type:snapshot resource_type:seed', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

        # Test build children
        mc = MockCtx()
        mc.obj['build_children'] = True
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        self.cdbt.sbuild(ctx=mc, full_refresh=False)
        expected_command = ['dbt', 'build', '--select', 'state:modified+', '--state', './_artifacts/', '--exclude', 'resource_type:snapshot resource_type:seed', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

        # Test build children graph count limit (i.e. sbuild+3)
        mc = MockCtx()
        mc.obj['build_children'] = True
        mc.obj['build_children_count'] = 2
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        self.cdbt.sbuild(ctx=mc, full_refresh=False)
        expected_command = ['dbt', 'build', '--select', 'state:modified+2', '--state', './_artifacts/', '--exclude', 'resource_type:snapshot resource_type:seed', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_pbuild_output(self):
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        self.cdbt.pbuild(ctx=MockCtx(), full_refresh=False)
        expected_command = ['dbt', 'build', '--select', 'state:modified', '--state', './logs/', '--exclude', 'resource_type:snapshot resource_type:seed', '--full-refresh']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

        self.cdbt.dbt_ls_test_mode_output = self.non_incremental_ls_example
        self.cdbt.pbuild(ctx=MockCtx(), full_refresh=False)
        expected_command = ['dbt', 'build', '--select', 'state:modified', '--state', './logs/', '--exclude', 'resource_type:snapshot resource_type:seed']
        self.assertEqual(self.cdbt.dbt_test_mode_command_check_value, expected_command)

    def test_dbt_ls_test_mode_output_incremental(self):
        self.cdbt.dbt_ls_test_mode_output = self.incremental_ls_example
        result = self.cdbt.test_full_refresh([json.loads(
            '''{"name": "dim_patients", "resource_type": "model", "config": {"materialized": "incremental"}}''')])
        self.assertTrue(result)

    def test_dbt_ls_test_mode_output_non_incremental(self):
        self.cdbt.dbt_ls_test_mode_output = self.non_incremental_ls_example
        result = self.cdbt.test_full_refresh(
            [json.loads('''{"name": "dim_patients", "resource_type": "model", "config": {"materialized": "view"}}''')])
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
