## Steps for starting a spark cluster with Weather Data.

1. Start a cluster using `spark-notebook/run.py`
2. When the cluster is up, start a jupyter notebook.
3. From the jupyter console, start a terminal.
4. go to the main working directory: `cd /mntls/workspace/`
5. `ls` should show one file: `FilesIO.ipynb`
6. Clone your code directory (here we are cloning the main public repo):  
`git clone https://github.com/yoavfreund/Public-DSC291.git`
7. Go back to the Files console and open the notebook `aws-jupyter-scripts/FilesIO-for-DSC291.ipynb`
8. Executing the commands in this notebook will load the data into dataframes and will copy the meta-information files into the directory.
9. Use `sc.stop` before continuing to other notebooks.
10. Go to the directory `notebooks/Section2-PCA/PCA/data_preparation/` to start working with the dataframes.
11. Remember that you need to add the commands to load the dataframes (given at the end of `FilesIO-for-DSC291.ipynb` to the start of each of those notebooks.