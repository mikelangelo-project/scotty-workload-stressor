import unittest
from mock import patch, MagicMock
import env
import sys
sys.modules['scotty'] = MagicMock()
with patch('scotty.utils') as mock_utils:
    import workload_gen as workload


class TestWorkloadGen(unittest.TestCase):
    def setUp(self):
        self.context = MagicMock()
        self.context.v1.workload.params = {
                'experiment_name': 'foo',
                'stressors_ip': 'foo',
                'tag': 'bar',
                'sleep_time': 1,
                'stressor_params':{
                    'foo': 'bar'
                    }
        }

    @patch('workload_gen.StressorExecutor.execute')
    def test_run_check_stressor_object(self, stressor_execute):
        workload.run(self.context)
        stressor_execute.assert_called()

    @patch('workload_gen.StressorExecutor')
    @patch('workload_gen._get_stressor_arguments')
    def test_run_check_internal_calls(self, stressor_args, stressor):
        workload.run(self.context)
        stressor_args.assert_called()

    def test_get_stressor_arguments(self):
        resource = MagicMock()
        result = workload._get_stressor_arguments(resource, self.context.v1.workload)
        self.assertEqual(len(result), 4)
