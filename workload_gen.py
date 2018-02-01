import logging 

from stressor.workload import StressorWorkload

logger = logging.getLogger(__name__)

StressorWorkload.reduce_logging()

def run(context):
    stressor_workload = StressorWorkload(context)
    stressor_workload.run()

def collect(context):
    pass

def clean(context):
    pass
