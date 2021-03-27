import csv
import os
import pandas as pd
from collections import OrderedDict
from visualization.distance_bokeh import read_csv

root_path = r'../csv'
nuclei_file_name = 'nuclei.csv'
vessel_file_name = 'vessel.csv'
nuclei_file_path = os.path.join(root_path, nuclei_file_name)
vessel_file_path = os.path.join(root_path, vessel_file_name)

drug_color = OrderedDict([
    ("Item Category", "#0d33ff"),
    ("Item metadata", "#c64737"),
    ("User profile", "black"),
])

gram_color = OrderedDict([
    ("negative", "#e69584"),
    ("positive", "#aeaeb8"),
])

v_headers, v_columns = read_csv(vessel_file_path)
for i in range(0, len(v_headers)):
    v_columns[v_headers[i]] = [float(value) for value in v_columns[v_headers[i]]]
v_columns['y'] = [(1400 - float(value)) for value in v_columns['y']]

data = dict()
for header in v_headers:
    data[header] = v_columns[header]
v_df = pd.DataFrame(data)

n_headers, n_columns = read_csv(nuclei_file_path)
for i in range(1, len(n_headers)):
    n_columns[n_headers[i]] = [float(value) for value in n_columns[n_headers[i]]]
n_columns['y'] = [(1400 - float(value)) for value in n_columns['y']]

data = dict()
for header in n_headers:
    data[header] = n_columns[header]
n_df = pd.DataFrame(data)

import matplotlib.pyplot as plt
import numpy as np
import io
import skimage
from skimage import io as sio

fig = plt.figure(figsize=(16, 16), dpi=300)
ax=fig.add_axes([0,0,1,1])
ax.scatter(data['x'], data['y'], edgecolors='k', s=3, facecolors='none',)
plt.show()
fig.savefig('test.tif')
