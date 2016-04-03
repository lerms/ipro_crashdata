import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
from geopy import Nominatim
import numpy as np
import json
from collections import defaultdict

zip_dict = defaultdict(str)
with open('data/zips.txt') as zfile:
    lines = csv.reader(zfile, delimiter='\t')
    for row in lines:
        city = row[0]
        zips = row[1].split(',')
        for z in zips:
            zip_dict[z.replace(" ", "")] = city

with open('data/chicago_crashes.json') as file:
    data = json.load(file)

geolocator = Nominatim()
accidents = data['accidents']
# hood_info will store whatever we want to know about a given neighborhood
# ex: '
# {hood: [[incidents], total_incedents, severe, ...]
#  we can continue adding info to the dict
hood_info = defaultdict(list)
i = 0
for v in accidents:
    # if i == 50:
    #     break
    try:
        zippy = \
            geolocator.reverse(str(v['lat']) + ', ' + str(v['lng'])).raw['display_name'].split('Illinois')[1].split(
                ',')[1].replace(" ", "")
    except Exception:
        print('geolocator could not reverse.')
        i += 1
        continue

    if zippy not in zip_dict:
        print('zip:' + zippy + ' not in common neighborhoods')
        continue

    hood = zip_dict[zippy]  # the neighborhood name associated with a zip
    if hood in hood_info:
        hood_info[hood][0].append(v)
        hood_info[hood][1] += 1
    else:
        hood_info[hood] = [[v], 1, 0]

    if v['severity'] > 2:   # for getting severe incidents only
        hood_info[hood][2] += 1
    i += 1

xx = hood_info.items()  # [(hood, [[incidents], total, severe]), ..., ]
y_pos = np.arange(len(hood_info))
plt.barh(y_pos, [v[1][1] for v in xx], align='center', alpha=0.4)
plt.yticks(y_pos, [v[0] for v in xx])
plt.xlabel('Total Accidents')
plt.title('Accidents by Neighborhood')
plt.show()
