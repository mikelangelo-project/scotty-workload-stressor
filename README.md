Stressor Workload
===================

[![N|Solid](https://www.gwdg.de/GWDG-Theme-1.0-SNAPSHOT/images/gwdg_logo.svg)](https://nodesource.com/products/nsolid)

## Overview
Here is the workload that stresses an specific resource

### Prerequisite
1. pip install -r requirement.txt

#### Notes
For adding stressor parameters checkout the [ubuntu help page](http://manpages.ubuntu.com/manpages/xenial/man1/stress-ng.1.htm).
Sample configuration for experiment.yaml
```yaml
resources:
  - name: stressor
    generator: file:workload/stressor
    params:
      experiment_name: 'csws_experiment'
      tag: 'stressor1'
      stressor_params:
        'cpu': '8'
        'timeout': '10s'
```
