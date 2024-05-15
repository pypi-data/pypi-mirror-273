# Data Package for "Surrogates for Fair-Weather Photovoltaic Module Output"

## Overview

For a detailed explanation of how the data was obtained / preprocessed please refer to the paper (Citation at the bottom). For a quick overview see the extended abstract in the data package.

- Around 40GB worth of Fair-Weather photovoltaic from PVGIS
- Distribution of module parameters from privately owned modules (obtained using maestr and fused with pvoutput data)
- Additional data for fixed-location (module parameters are still sampled)
- Additional data for fixed-parameters (location increases)
- Easy data access using dataloaders (PACKAGE_LINK)
- Challenge data set including downward trend
- Downloadable from [archive.org](https://archive.org/details/pv-surrogate-data_dfalkner) (ID: `pv-surrogate-data_dfalkner`)

## Usage

Install using your favorite package manager:

```bash
pip install pv_surrogate_data
```

Then you can use the data access layer to load the data:

```python
from pv_surrogate_data import download_data, PVGISGermanyDataset, PVGISDataPackage

def main():
  # downloads all the data from archive.org, may take a while ~60GB
  data_path = Path(__file__) / '.pv_surrogate_data'
  data_path.mkdir(exist_ok=True, parents=True)
  download_data(data_path)

  # lazily loads the data, for more information see constructor
  # Alternatively supports `FixedLocationPVGISGermanyDataset`, `OutwardPointsPVGISGermanyDataset` and `ChallengePVGISGermanyDataset`
  data = PVGISGermanyDataset(PVGISDataPackage(data_path))

  # access all static data via `data.get_all_static_data()`
  all_static = data.get_all_static_data()

  # iterate over dataframe. Support collections.abc.Sequence 
  # additionally supports retreiving parameters (`get_static_data` and `get_all_static_data`)
  for index, sample in enumerate(data):
    print(sample)
    print(data.get_static_data(index))


if __name__ == '__main__':
  main()
```

## Data Package Structure

```
- <top-level-folder>
  - extended_abstract.pdf
  - figures/
    - # contains additional figures of the data 
  # the following directories relate strictly to the data
  - pvgis/  # metadata: german_enriched_{test,train}.parquet
  - pvgis_fixed_location/  # metadata: german_fixed_location.parquet
  - pvgis_outward/  # metadata: german_outward.parquet
  - system_data/
    # necessary for data access
    - german_outward.parquet
    - german_enriched_train.parquet
    - german_enriched_test.parquet
    - german_fixed_location.parquet

    # intermediate results
    - german_starting_points.parquet  # equally spaced starting points for germany
    - german_total_system_parameter_distribution.parquet  # full parameter distribution from germany
    - mastr_filtered.parquet  # prefiltered results from the Meldestammregister
    - pvoutput_austrian_systems.parquet  # austrian systems from pvoutput
    - pvoutput_austrian_systems_meta.parquet  # meta data for austrian systems
    - pvoutput_german_systems.parquet  # german systems from pvoutput
    - pvoutput_german_systems_meta.parquet  # german system meta data from pvoutput
```

- The request in the folders `{pvgis, pvgis_fixed_location, pvgis_outward}` can contain errors (which means some of the requests failed). The data access layers filters those out.
- Samples from a module are always saved as a single `parquet` file using the sample id in the corresponding `system_data` file. The exception is the `pvgis_outward` data. It's file name is defined as `f'{sample_id}_{bearing}_{distance}.parquet'`.


## License

You are free to use the produced data or produce your own data using the scripts provided in [the main repo](https://github.com/prescriptiveanalytics/paper_pv_surrogate_eurocast).

---

### Authors

Made in Austria by dominik.falkner@risc-software.at

If you use my work please cite me (for details please refer to the paper)!

```
Falkner, D., Bögl, M., Langthallner, I., Zenisek, J., Affenzeller, M., 2023, Surrogates for Fair-Weather Photovoltaic Module Output. Lecture Notes in Computer Science
```

