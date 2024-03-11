# Outbreak data

## Contents

Users can access the latest data sets for each outbreak through this repository's [wiki](https://github.com/globaldothealth/outbreak-data/wiki).

The [wiki](https://github.com/globaldothealth/outbreak-data/wiki) contains dated records of curated cases from a number of outbreaks, the data dictionaries used for each outbreak, and curator changelogs for each data set.

The data dictionaries contain information about columns/fields in corresponding data sets.

## Getting the data

Please consult the [wiki](https://github.com/globaldothealth/outbreak-data/wiki) for links to line list and timeseries data sets.

### Python
```python
import pandas as pd
df = pd.read_csv(DATA_CSV_URL)
```
### R
```r
df <- read.csv(DATA_CSV_URL)
```

## Contributing

If you would like to request changes, [open an issue](https://github.com/globaldothealth/outbreak-data/issues/new) on this repository and we will happily consider your request. 
If requesting a fix please include steps to reproduce undesirable behaviors.

If you would like to contribute, assign an issue to yourself and/or reach out to a contributor and we will happily help you help us.

If you want to send data to us, you can use our template provided in the [wiki](https://github.com/globaldothealth/outbreak-data/wiki) which makes
it easier for us to add to our list. Just open an issue and attach a CSV / XLSX file in this repository,
or email data to info@global.health. Remove any Personally Identifiable Information.

## Visualizations

The [wiki](https://github.com/globaldothealth/outbreak-data/wiki) contains links to data visualizations for each outbreak.

## License and attribution

This repository and data exports are published under the CC BY 4.0 license.

Consult the [wiki](https://github.com/globaldothealth/outbreak-data/wiki) for outbreak attribution details.
