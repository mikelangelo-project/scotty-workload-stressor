import logging
import os

import paramiko
from scotty.utils import WorkloadUtils

logger = logging.getLogger(__name__)


class StressorWorkload(object):
    def __init__(self, context):
        self.workload = context.v1.workload
        self.workload_utils = WorkloadUtils(context)

    @classmethod
    def reduce_logging(cls):
        reduce_loggers = {
            'keystoneauth.identity.v2',
            'keystoneauth.identity.v2.base',
            'keystoneauth.session',
            'urllib3.connectionpool',
            'stevedore.extension',
            'novaclient.v2.client'
        }
        for logger in reduce_loggers:
            logging.getLogger(logger).setLevel(logging.WARNING)

    def run(self):
        stressor_vms = self.workload_utils.resources['stressor_vms']
        stress_ng_params_list = self.workload.params['stress-ng-params']
        for index, stress_ng_params in enumerate(stress_ng_params_list):
            try:
                self._run_on(stressor_vms.endpoint[index], stress_ng_params)
            except IndexError:
                msg = 'No vm resource found for stress-ng-params[{}]'
                logger.warning(msg.format(index))

    def _run_on(self, endpoint, params):
        command = self._create_stress_ng_command(params)
        self._exec_remote_command(command, endpoint)

    def _create_stress_ng_command(self, params):
        command = []
        command.append('stress-ng')
        for key, value in params.items():
            command.append('--{} {}'.format(key, value))
        command.append('&')
        return ' '.join(command)

    def _exec_remote_command(self, command, endpoint):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                endpoint['ip'], 
                username=endpoint['user'], 
                key_filename=self._key_path(endpoint['private_key'])
            )
            stdin, stdout, stderr = ssh.exec_command(command)
            out = stdout.read()
            logger.info("Stressor {}:\r\n{}".format(endpoint['ip'], out))

    def _key_path(self, private_key_name):
        experiment_workspace_path = self.workload_utils.experiment_workspace.path
        key_path = os.path.join(experiment_workspace_path, private_key_name)
        return key_path
