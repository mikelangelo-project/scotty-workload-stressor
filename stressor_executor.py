import os
import logging

from fabric.api import run, settings

logger = logging.getLogger(__name__)


class StressorExecutor(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.key_path = os.path.join(os.sep, 'tmp', self.experiment_name, 'private.key')

    def execute(self):
        for index, vm_ip in enumerate(self.stressors_ip):
            with settings(host_string=vm_ip, connection_attempts=10, key_filename=self.key_path,
                          user='cloud'):
                instance_name = 'instance_'+(str)(index + 1)
                self._execute_command(self.params[instance_name])

    def _execute_command(self, command_list):
        commands = []
        commands.append('stress-ng')
        for key, value in command_list.items():
            commands.append('--' + key)
            commands.append(value)
        commands.append('&')
        execute_command = self._create_command(commands)
        run(execute_command)

    def _create_command(self, commands):
        output = ' '.join(commands)
        return output
