import pandas as pd

df = pd.read_excel('./timesheet/timesheet.xlsx')

for index, row in df.iterrows():
    print(row["Date"])
