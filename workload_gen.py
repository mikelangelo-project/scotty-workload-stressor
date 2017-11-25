import logging
import datetime
import os

from scotty import utils

from stressor_execution import StressorExecution

logger = logging.getLogger(__name__)


def result(context):
    pass


def run(context):
    workload = context.v1.workload
    experiment_helper = utils.ExperimentHelper(context)
    resource = experiment_helper.get_resource(workload.resources['resource'])
    arguments = _get_benchmark_arguments(resource, workload)
    stressor = StressorExecution(**arguments)
    start_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    stressor.execute()
    end_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
   # _write_time_interval(start_time, end_time, arguments)


def _get_benchmark_arguments(resource, workload):
    arguments = {
        'experiment_name': workload.params['experiment_name'],
        'tag': workload.params['tag'],
        'vm_ip': resource.endpoint['ip'],
        'params': workload.params['stressor_params']
    }
    return arguments


def _write_time_interval(start_time, end_time, arguments):
    log_path = os.path.join(os.sep, 'tmp', arguments['experiment_name'],
                            arguments['tag'])
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    log_file = os.path.join(log_path, 'PostRunInfo.txt')
    with open(log_file, 'w+') as file:
        file.write('{}\n{}\n{}'.format(arguments['experiment_name'],
                                       str(start_time), str(end_time)))
