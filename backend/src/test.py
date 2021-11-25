import pandas as pd

from data_classes.Movie import Movie

df = pd.DataFrame.from_records([{"test": 1, "val": "val"}], index="test")
df2 = pd.DataFrame.from_records([{"test": 1, "val": "val"}, {"test": 2, "val": "val"}], index="test")
# df.set_index("test", inplace=True)
# df.set_index("test", inplace=True)


df3 = df.combine_first(df2)

print(df3)