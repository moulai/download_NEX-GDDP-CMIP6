# download_NEX-GDDP-CMIP6
A simple script to download the specified files in NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6) dataset.

`gddp-cmip6-files.csv` is a csv file that contains the information of the files in NEX-GDDP-CMIP6 dataset. The file is downloaded from https://nex-gddp-cmip6.s3-us-west-2.amazonaws.com/gddp-cmip6-files.csv. The file has been modified to include three extra columns: `Model`, `Experiment`, and `Variable`, which are extracted from the `fileUrl` column.

Reference:
- https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6
- https://ds.nccs.nasa.gov/thredds/catalog/AMES/NEX/GDDP-CMIP6/catalog.html
- https://www.nccs.nasa.gov/sites/default/files/NEX-GDDP-CMIP6-Tech_Note.pdf
- https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index.html


## Usage
```
pip install -r requirements.txt
python download_NEX-GDDP-CMIP6.py
```

## License
MIT