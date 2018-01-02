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
        for vm_ip in self.stressors_ip:
            with settings(host_string=vm_ip, connection_attempts=10,
                          key_filename=self.key_path, user='cloud'):
                self._execute_command()

    def _execute_command(self):
        commands = []
        commands.append('stress-ng')
        for key, value in self.params.items():
            commands.append('--' + key)
            commands.append(value)
        commands.append('&')
        execute_command = self._create_command(commands)
        run(execute_command)

    def _create_command(self, commands):
        output = ' '.join(commands)
        return output
