# pyDIOPT

This is the unofficial, opinionated DIOPT python wrapper for the [DIOPT](https://www.flyrnai.org/cgi-bin/DRSC_orthologs.pl) ortholog finder.

## Installation

```shell
pip install pyDIOPT
```

## Example

A couple examples of how to run the wrapper. The standard output is organized into pd.DataFrame for easier downstream manipulations and whatever you want (or can) do with ortholog data (?).

```python
from pyDIOPT import DIOPTRelease

release = DIOPTRelease("v8", "h sapiens")

# fetching single gene
example1 = release.fetch("ENSG00000085117", target_species=None)

# fetching several genes
example2 = release.fetch(
    ["MDM2", "TP53"], target_species="mouse", filter="best_match", condensed=False
)
```

## Acknowledgement

-   This repo is boilerplated from [py-package-template](https://github.com/AlexIoannides/py-package-template)

-   To retrieve the information on citing the original papers, run
    ```python
    import pyDIOPT
    pyDIOPT.citation()
    ```
