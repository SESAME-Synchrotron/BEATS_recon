# BEATS_recon

[TomoPy](https://tomopy.readthedocs.io/en/latest/) reconstruction scripts, notebooks and examples for the [ID10-BEATS beamline](https://www.sesame.org.jo/beamlines/beats) of [SESAME](https://www.sesame.org.jo/). <br />
Datasets for running the tests can be found on the [TomoBank](https://tomobank.readthedocs.io/en/latest/)
[![GitHub license](https://img.shields.io/github/license/SESAME-Synchrotron/BEATS_recon)](https://github.com/SESAME-Synchrotron/BEATS_recon/blob/master/LICENSE)


## Examples:


## Notes:

Activate TomoPy reconstruction environment
```commandline
conda activate tomopy
```

Lanuch Jupyter Notebook or Jupyter Lab
```commandline
jupyter notebook
```

```commandline
jupyter lab
```

Add and activate a TomoPy kernel in Jupyter:
> [!NOTE]  
> You probably don't need this.

1. Check and activate the environment where ipython is living 
```commandline
conda env list
source activate base
```

Install TomoPy kernel in it
```commandline
python -m ipykernel install --user --name tomopy --display-name "conda (tomopy_source)"
```

## Roadmap
[Roadmap and list of tested features](tests/README.md)
