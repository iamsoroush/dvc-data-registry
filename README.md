# dvc-data-registry
1. pip install 'dvc[gdrive]'
2. dvc init
3. dvc add mnist
4. dvc remote add -d storage gdrive://1oSwpexBh_OosVi-SQVE8MSvSZmALpz5b
5. dvc push
6. git add mnist.dvc .gitignore .dvcignore
7. 