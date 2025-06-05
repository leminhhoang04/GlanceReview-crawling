import pandas as pd

df = pd.read_csv("icore-conf-rank.csv", encoding="utf-8")
print(df['rank'].value_counts())

df_filtered = df[df['rank'].isin(['A', 'A*'])]
df_filtered.to_csv("icore-conf-rank-A-Astar.csv", index=False, encoding="utf-8")
print(df_filtered['rank'].value_counts())
