import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
import re
from datetime import datetime

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

engineering_campaigns = pd.read_csv("engineering_campaigns.csv")

print(engineering_campaigns)

engineering_campaigns['amount'] = engineering_campaigns['amount'].astype(float)
print(engineering_campaigns)
print(engineering_campaigns.dtypes)

engineering_pivot = engineering_campaigns.pivot_table(values = 'amount', index = 'timestamp', columns = 'campaign_name')
print(engineering_pivot)
engineering_pivot.fillna(0, inplace=True)
print(engineering_pivot)

engineering_pivot.iloc[:, 0:-1] = engineering_pivot.iloc[:, 0:-1].cumsum()
print(engineering_pivot)

top_campaigns = set()

for index, row in engineering_pivot.iterrows():
    top_campaigns |= set(row[row > 0].sort_values(ascending=False).head(10).index)

engineering_pivot = engineering_pivot[top_campaigns]

print(engineering_pivot)

print(engineering_pivot.index[2])

indexes = list(engineering_pivot.index)

rename_dict = {}
for i in range(len(engineering_pivot)):
    string = indexes[i]
    numbers = re.findall(r'[0-9]+', string)
    #numbers[2] = int(numbers[2]) - 1
    if int(numbers[3]) - 5 < 0:
        numbers[2] = int(numbers[2]) - 1
    numbers[3] = (int(numbers[3]) - 5) % 24
    final_time = f"{numbers[3]}:{numbers[4]}:{numbers[5]}"
    string2 = (f"Apr {numbers[2]} @ {final_time}")
    rename_dict[string] = string2

#print(f"rename_dict {rename_dict}")

engineering_pivot = engineering_pivot.rename(index = rename_dict)
engineering_pivot = engineering_pivot.drop("Apr 14 @ 0:00:28")
print(engineering_pivot)
    
engineering_pivot.to_csv('viewing_pivot.csv')

bcr.bar_chart_race(df = engineering_pivot,
                   n_bars = 10,
                   sort='desc',
                   title='OU GCOE Giving Day 2023 Top 10',
                   period_length  = 75,
                   colors='light24',
                   period_label = {'size':6, 'x':1.1},
                   filter_column_colors = True,
                   filename = 'raceT10C.mp4',
                   )


