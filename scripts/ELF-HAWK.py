import pandas as pd

df = pd.read_csv("ELF-HAWK-dump.csv", dtype=str)
df = df.loc[:, df.applymap(lambda x: x in ['TRUE', 'FALSE']).all()]
df = df[~df.apply(lambda row: (row == 'FALSE').all(), axis=1)]
df = df.replace({'TRUE': '1', 'FALSE': '0'})

with open("outdata", 'w') as f:
    for _, row in df.iterrows():
        row_values = ''.join(str(value) for value in row)
        f.write(row_values)