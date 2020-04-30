## Main Notebooks
1. PreProcess weather data.ipynb: Transform ALL.csv into a parquet file (no cleaning)
1. S1 Partition Parquet.ipynb  : Keep only the common measurements and partition the stations in the US into 256 with the same number of measurements each.
1. Split into small parquet files.ipynb1. Big_PCA_computation.ipynb Create 256 256 small parquet files
1. PCA_computation.ipynb: compute the statistics (STAT) for a given file.

## misc notebooks
1. Selecting good stations for HW5.ipynb
