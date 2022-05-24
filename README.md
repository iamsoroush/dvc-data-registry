# dvc-data-registry

## Initialize
1. `pip install 'dvc[gdrive]'`
2. `dvc init`
3. `dvc remote add -d storage gdrive://1oSwpexBh_OosVi-SQVE8MSvSZmALpz5b`

## Adding a new data-source
1. define your data-source name and the path to the data, which is a folder containing Dicom Studies, which are collections of dicom files.
2. run the pipeline -> `python add_to_data_source.py run --src-dir "/Users/soroush/Datasets/CT Brain/local/Other" --datasource-name test`

[//]: # (3. add and commit -> `DATA_ROOT="CTBrain Datasets" DS_NAME="test" sh dvcpush.sh`)
3. tag -> `git tag ctbrain-raw`
4. push -> `git push origin ctbrain-raw`


## Import a data-source (experimentation side)
1. install DVC -> `pip install "dvc[gdrive]"`
2. initialize DVC in the repository -> `dvc init`
3. list the tracked data in the data registry -> `dvc list https://github.com/iamsoroush/dvc-data-registry --rev main`
4. import the dataset (here the `test` dataset) -> `dvc import https://github.com/iamsoroush/dvc-data-registry.git "CTBrain Datasets/test" -o datasets/`
5. and update the dataset to the latest version -> `dvc update datasets/test.dvc` or use `--rev` for updating to a specific commit, tag or branch on data registry