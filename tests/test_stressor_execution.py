import unittest
import env
from mock import Mock, patch
from stressor_execution import StressorExecution


class TestStressorExecution(unittest.TestCase):

    def setUp(self):
        mock_kwargs = {
                'vm_ip': '1.1.1.1',
                'experiment_name': 'foo',
                'tag': 'foo',
                'params': {
                    'foo': 'bar'
                    }
                }
        self.key_path = 'foo'
        self.stressor = StressorExecution(**mock_kwargs)

    @patch('stressor_execution.run')
    @patch('stressor_execution.settings')
    def test_execute_check_ssh(self, api_settings, api_run):
        api_settings.return_value.__exit__ = Mock()
        api_settings.return_value.__enter__ = Mock()
        api_run.return_value = Mock()
        self.stressor.execute()
        api_settings.assert_called()
        api_run.assert_called()

    @patch('stressor_execution.run')
    @patch('stressor_execution.settings')
    @patch('stressor_execution.StressorExecution._execute_command')
    def test_execute_check_internal_calls(self, execute_command, api_settings, api_run):
        api_settings.return_value.__exit__ = Mock()
        api_settings.return_value.__enter__ = Mock()
        api_run.return_value = Mock()
        self.stressor.execute()
        execute_command.assert_called()

    @patch('stressor_execution.run')
    @patch('stressor_execution.StressorExecution._create_command')
    def test_execute_command(self, create_command, api_run):
        self.stressor._execute_command()
        create_command.assert_called()
        api_run.assert_called()

    def test_create_command(self):
        test_command_array = ('ls', '-al', '/var/log')
        test_command = 'ls -al /var/log'
        result = self.stressor._create_command(test_command_array)
        self.assertTrue(result == test_command)
