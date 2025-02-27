# GHL2024.D11.1E31 

Scripts to prepare data for the Influenza A outbreak in poultry, cattle and
humans in the USA.

To run the script, you need [`uv`](https://docs.astral.sh/uv/) installed. On
macOS, it is available from `brew`: `brew install uv`. For Linux, consult the
uv documentation. Once uv is installed, run:

```shell
uv run timeline_expand.py
```

This will produce an output (defined in the `OUTPUT` parameter in the script)
from the `INPUT` file, which has to be downloaded from the Influenza A Google
Sheets.
