import pandas as pd

# read the csv file
df = pd.read_csv("./data/sample.csv")
# save as parquet
df.to_parquet("./data/sample.parquet", index=False)
