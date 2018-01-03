import logging
import datetime
import os
import time
from scotty import utils

from stressor_executor import StressorExecutor

logger = logging.getLogger(__name__)


def result(context):
    pass


def run(context):
    workload = context.v1.workload
    experiment_helper = utils.ExperimentHelper(context)
    resource = experiment_helper.get_resource(workload.resources['resource'])
    arguments = _get_stressor_arguments(resource, workload)
    stressor = StressorExecutor(**arguments)
    stressor.execute()
    sleep_time = workload.params['sleep_time']
    time.sleep(sleep_time)

def _get_stressor_arguments(resource, workload):
    arguments = {
        'experiment_name': workload.params['experiment_name'],
        'tag': workload.params['tag'],
        'stressors_ip': resource.endpoint['ip'],
        'params': workload.params['stressor_params']
    }
    return arguments
