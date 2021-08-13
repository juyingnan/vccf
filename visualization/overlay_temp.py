import csv
import math
import os
import sys
import pandas as pd
import numpy as np
from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool

sys.path.insert(1, r'C:\Users\bunny\PycharmProjects\vccf_visualization')
import utils.kidney_nuclei_vessel_calculate as my_csv


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        _headers = next(reader, None)

        # get column
        _columns = {}
        for h in _headers:
            _columns[h] = []
        for row in reader:
            for h, v in zip(_headers, row):
                _columns[h].append(v)

        for item in _headers:
            print(item)

        return _headers, _columns


tools_list = "pan," \
             "box_select," \
             "lasso_select," \
             "box_zoom, " \
             "wheel_zoom," \
             "reset," \
             "save," \
             "help"
# "hover," \

nuclei_id_list = list()
nuclei_type_list = list()
nuclei_x_list = list()
nuclei_y_list = list()
nuclei_distance_list = list()
nuclei_nearest_vessel_x_list = list()
nuclei_nearest_vessel_y_list = list()
vessel_x_list = list()
vessel_y_list = list()
z_list = [77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101]
micro_per_pixel = 0.325
scale = 16 * micro_per_pixel

top_left = [0, 0]
bottom_right = [1000000, 1000000]
# top_left = [5350 * micro_per_pixel, 3900 * micro_per_pixel]
# bottom_right = [7150 * micro_per_pixel, 4700 * micro_per_pixel]


region_index = 6

if len(sys.argv) >= 2:
    region_index = sys.argv[1]

nuclei_root_path = rf'G:\GE\skin_12_data\region_{region_index}'
nuclei_file_name = rf'centroids.csv'

nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)

if len(sys.argv) >= 3:
    nuclei_file_path = sys.argv[2]

n_headers, n_columns = my_csv.read_csv(nuclei_file_path)
for i in range(0, 5):  # len(n_headers)):
    n_columns[n_headers[i]] = [value for value in n_columns[n_headers[i]]]
# n_columns['Y'] = [float(value) for value in n_columns['Y']]
# n_columns['X'] = [float(value) for value in n_columns['X']]
for i in range(len(n_columns['X'])):
    if top_left[0] < float(n_columns['X'][i]) * scale < bottom_right[0] and \
            top_left[1] < float(n_columns['Y'][i]) * scale < bottom_right[1]:
        temp_z = float(n_columns['Z'][i])
        if temp_z < 0 or temp_z > 3:
            continue
        if n_columns['cell_type'][i] == 'CD31':
            vessel_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            vessel_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
        else:
            nuclei_id_list.append(i)
            nuclei_type_list.append(n_columns['cell_type'][i])
            nuclei_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            nuclei_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
# nuclei_class_list = [int(value) for value in n_columns['Class']]

# nuclei_image = io.imread('../images/nuclei_ml.png')  # [::-1, :]
# _nid = 0
# for i in range(len(nuclei_image)):
#     row = nuclei_image[i]
#     for j in range(len(row)):
#         pixel = row[j]
#         if pixel[0] > 200:
#             # each nuclear is 2x2 pixels
#             # get the average (+0.5)
#             # and erase other 3 points
#             nuclei_y_list.append((i + 0.5) / pixel_per_um)
#             nuclei_x_list.append((j + 0.5) / pixel_per_um)
#             nuclei_image[i][j + 1] *= 0
#             nuclei_image[i + 1][j] *= 0
#             nuclei_image[i + 1][j + 1] *= 0
#             nuclei_id_list.append(_nid)
#             _nid += 1
print(len(nuclei_x_list))

output_root_path = nuclei_root_path
nuclei_output_name = 'nuclei.csv'
nuclei_output_path = os.path.join(output_root_path, nuclei_output_name)
vessel_output_name = 'vessel.csv'
vessel_output_path = os.path.join(output_root_path, vessel_output_name)

for nid in range(len(nuclei_id_list)):
    _min_dist = 100 * scale
    _min_vessel_x = 0
    _min_vessel_y = 0
    _nx = nuclei_x_list[nid]
    _ny = nuclei_y_list[nid]
    _has_near = False
    for v in range(len(vessel_x_list)):
        _vx = vessel_x_list[v]
        _vy = vessel_y_list[v]
        if abs(_nx - _vx) < _min_dist and abs(_ny - _vy) < _min_dist:
            _dist = math.sqrt((_nx - _vx) ** 2 + (_ny - _vy) ** 2)
            if _dist < _min_dist:
                _has_near = True
                _min_dist = _dist
                _min_vessel_x = _vx
                _min_vessel_y = _vy
    if not _has_near:
        print("NO NEAR")
    nuclei_distance_list.append(_min_dist)
    nuclei_nearest_vessel_x_list.append(_min_vessel_x)
    nuclei_nearest_vessel_y_list.append(_min_vessel_y)
    if nid % 100 == 0:
        print('\r' + str(nid), end='')

print(len(nuclei_id_list), len(nuclei_x_list), len(nuclei_y_list), len(nuclei_distance_list),
      len(nuclei_nearest_vessel_x_list), len(nuclei_nearest_vessel_y_list))

my_csv.write_csv(nuclei_output_path,
                 [nuclei_id_list,
                  nuclei_x_list,
                  nuclei_y_list,
                  nuclei_type_list,
                  nuclei_distance_list,
                  nuclei_nearest_vessel_x_list,
                  nuclei_nearest_vessel_y_list, ],
                 ['id', 'x', 'y',
                  'type',
                  'distance', 'vx', 'vy', ])

my_csv.write_csv(vessel_output_path,
                 [vessel_x_list, vessel_y_list, ],
                 ['x', 'y', ])

# import matplotlib.pyplot as plt
#
# # plt.scatter(vessel_x_list, vessel_y_list, c='r')
# # plt.scatter(nuclei_x_list, nuclei_y_list, c='b')
# plt.hist(nuclei_distance_list, bins=100)
# plt.show()

color_dict = {
    'CD68': "#ffcc00",
    'Machrophage': "#ffcc00",
    'CD31': "#00e0e0",  # CD31
    'Blood Vessel': "#00e0e0",  # CD31
    'T-Helper': "#ffe000",  # CD3
    'T-Reg': "#ff00e0",  # CD4
    'T-Regulatory': "#ff00e0",  # CD4
}
n_color = [color_dict[cell_type] for cell_type in nuclei_type_list]
v_color = [color_dict['CD31']] * len(vessel_x_list)

size_dict = {
    'CD68': 15.89,
    'Machrophage': 15.89,
    'CD31': 16.83,
    'Blood Vessel': 16.83,
    'T-Helper': 16.96,
    'T-Reg': 17.75,
    'T-Regulatory': 17.75,
}

cell_type_dict = {
    'CD68': "Machrophage / CD68",
    'Machrophage': "Machrophage / CD68",
    'CD31': "Blood Vessel",
    'Blood Vessel': "Blood Vessel",
    'T-Helper': "T-Helper",
    'T-Reg': "T-Regulatory",
    'T-Regulatory': "T-Regulatory",
}

n_size = [size_dict[cell_type] / 2 for cell_type in nuclei_type_list]
v_size = [size_dict['CD31'] / 2] * len(vessel_x_list)
# fig = plt.figure(figsize=(20, 20))
# ax = fig.add_subplot(111, projection='3d')
# ax._axis3don = False
#
# color_max = max(nuclei_distance_list)
# colors = ['#%02x%02x%02x' % (0, int(255 * value / color_max), int(255 * (color_max - value) / color_max))
#           for value in nuclei_distance_list]
#
# ax.scatter(nuclei_x_list, nuclei_y_list, nuclei_z_list, color=color, marker="o", s=15)
# ax.scatter(vessel_x_list, vessel_y_list, vessel_z_list, color='r', marker="o", s=15)
#
# for i in range(len(nuclei_id_list)):
#     ax.plot([nuclei_x_list[i], nuclei_nearest_vessel_x_list[i]],
#             [nuclei_y_list[i], nuclei_nearest_vessel_y_list[i]],
#             [nuclei_z_list[i], nuclei_nearest_vessel_z_list[i]],
#             color='k', linewidth=0.1)
#
# ax.set_xlim3d(0, 3000)
# ax.set_ylim3d(0, 3000)
# ax.set_zlim3d(0, 3000)
#
# plt.show()
#
# # plt.scatter(vessel_x_list, vessel_y_list, c='r')
# # plt.scatter(nuclei_x_list, nuclei_y_list, c='b')
# plt.hist(nuclei_distance_list, bins=100)
# plt.show()


n_data = dict()
n_data["nx"] = nuclei_x_list
n_data["ny"] = nuclei_y_list
n_data["size"] = n_size
n_data["type"] = nuclei_type_list
n_data["distance"] = nuclei_distance_list
n_data["color"] = n_color

n_df = pd.DataFrame(n_data)

print(n_df)
# https://stackoverflow.com/questions/56723792/plotly-how-to-efficiently-plot-a-large-number-of-line-shapes-where-the-points-a

line_x = [None] * (len(nuclei_x_list) + len(nuclei_nearest_vessel_x_list))
line_y = [None] * (len(nuclei_y_list) + len(nuclei_nearest_vessel_y_list))
line_x[::2] = nuclei_nearest_vessel_x_list
line_x[1::2] = nuclei_x_list
line_y[::2] = nuclei_nearest_vessel_y_list
line_y[1::2] = nuclei_y_list
v_data = dict()
v_data["vx"] = line_x
v_data["vy"] = line_y
# v_color = ['red'] * len(vessel_x_list)
# v_data["color"] = v_color
v_df = pd.DataFrame(v_data)

v_gap = (v_df.iloc[1::2]
         .assign(vx=np.nan, vy=np.nan)
         .rename(lambda x: x + .5))
v_df_one = pd.concat([v_df, v_gap], sort=False).sort_index().reset_index(drop=True)
v_df_one.loc[v_df_one.isnull().any(axis=1), :] = np.nan

print(v_df_one)

output_file("result/distance.html")

index = 1
p = figure(match_aspect=True,
           plot_width=int(3727 * index), plot_height=int(2348 * index),
           tools=tools_list, output_backend="svg",
           # title='nuclei/vessel distance',
           )

p.background_fill_color = None
p.border_fill_color = None

p.xgrid.visible = False
p.ygrid.visible = False
p.axis.visible = False
p.background_fill_alpha = 0.0
p.outline_line_color = None

data = dict()

v_df = pd.DataFrame(v_data)

p.circle(x='vx', y='vy', source=v_df, color=color_dict['CD31'], size=4, alpha=1)

n_df = pd.DataFrame(n_data)

p.line(v_df_one['vx'], v_df_one['vy'], line_width=1, alpha=0.7, color='grey')
# p.segment(x0='nx', y0='ny', x1='vx', source=n_df, y1='vy', color="red", alpha=0.2, line_width=1)
circle = p.circle(x='nx', y='ny', source=n_df, color='color', alpha=0.7, size=5)
# g1_hover = HoverTool(renderers=[circle], tooltips=[('X', "@x"), ('Y', "@y"), ('distance', "@distance")])
# p.add_tools(g1_hover)

# p.legend.location = "bottom_right"

show(p)
