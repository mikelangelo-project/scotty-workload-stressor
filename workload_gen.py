import logging 

from stressor.workload import StressorWorkload

logger = logging.getLogger(__name__)

def run(context):
    logger.info("workload run")
    stressor_workload = StressorWorkload(context)
    stressor_workload.run()

def collect(context):
    pass

def clean(context):
    pass
