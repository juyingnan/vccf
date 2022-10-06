import math
import os
import sys
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from cell_defination import *

sys.path.insert(1, r'C:\Users\bunny\PycharmProjects\vccf_visualization')
import utils.kidney_nuclei_vessel_calculate as my_csv


def generate_one_line_df(df, key):
    line_x = [None] * (len(df) * 2)
    line_y = [None] * (len(df) * 2)
    line_z = [None] * (len(df) * 2)
    line_x[::2] = df[f"n{key}x"]
    line_y[::2] = df[f"n{key}y"]
    line_z[::2] = df[f"n{key}z"]
    line_x[1::2] = df["nx"]
    line_y[1::2] = df["ny"]
    line_z[1::2] = df["nz"]

    l_data = dict()
    l_data["x"] = line_x
    l_data["y"] = line_y
    l_data["z"] = line_z
    # v_color = ['red'] * len(vessel_x_list)
    # v_data["color"] = v_color
    l_df = pd.DataFrame(l_data)
    l_gap = (l_df.iloc[1::2]
             .assign(x=np.nan, y=np.nan)
             .rename(lambda x: x + .5))
    l_df_one = pd.concat([l_df, l_gap], sort=False).sort_index().reset_index(drop=True)
    l_df_one.loc[l_df_one.isnull().any(axis=1), :] = np.nan
    return l_df_one


def generate_nuclei_scatter(df, ct, visible=True, show_legend=True, legend_group=""):
    return go.Scatter3d(x=df[df['type'] == ct]["nx"],
                        y=df[df['type'] == ct]["ny"],
                        z=df[df['type'] == ct]["nz"],
                        mode="markers",
                        name=cell_dict[cell_type]['legend'],
                        showlegend=show_legend,
                        legendgroup=legend_group,
                        legendgrouptitle_text=legend_group,
                        marker=dict(
                            size=df[df['type'] == ct]["size"],
                            color=df[df['type'] == ct]["color"],
                            symbol=cell_dict[ct]['marker'],
                            opacity=0.75,
                            line=dict(
                                color=df[df['type'] == ct]["color"],
                                width=0
                            )),
                        visible=visible)


def generate_other_scatter(df, key, name, symbol_name, visible=True, show_legend=True, legend_group=""):
    return go.Scatter3d(x=df[f"{key}x"], y=df[f"{key}y"], z=df[f"{key}z"],
                        mode="markers",
                        name=name,
                        showlegend=show_legend,
                        legendgroup=legend_group,
                        legendgrouptitle_text=legend_group,
                        marker=dict(
                            size=df["size"],
                            color=df["color"],
                            symbol=cell_dict[symbol_name]['marker'],
                            opacity=0.5,
                            line=dict(
                                color=df["color"],
                                width=0)),
                        visible=visible)


def generate_line(df, name, color, visible=True, opacity=0.5, width=1, show_legend=True, legend_group=""):
    return go.Scatter3d(x=df["x"],
                        y=df["y"],
                        z=df["z"],
                        mode="lines",
                        name=name,
                        opacity=opacity,
                        showlegend=show_legend,
                        legendgroup=legend_group,
                        legendgrouptitle_text=legend_group,
                        line=dict(
                            color=color,
                            width=width, ),
                        visible=visible)


nuclei_id_list = list()
nuclei_type_list = list()
nuclei_x_list, nuclei_y_list, nuclei_z_list = [], [], []
nuclei_vessel_distance_list = list()
nuclei_skin_distance_list = list()
nuclei_nearest_vessel_x_list = list()
nuclei_nearest_vessel_y_list = list()
nuclei_nearest_vessel_z_list = list()
nuclei_nearest_skin_x_list = list()
nuclei_nearest_skin_y_list = list()
nuclei_nearest_skin_z_list = list()
vessel_x_list, vessel_y_list, vessel_z_list = [], [], []
skin_x_list, skin_y_list, skin_z_list = [], [], []
z_list = [77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101]
micro_per_pixel = 0.325
scale = 16 * micro_per_pixel

top_left = [0, 0]
bottom_right = [1000000, 1000000]

region_index = 3
show_html = True

if len(sys.argv) >= 2:
    region_index = int(sys.argv[1])
    show_html = False

nuclei_root_path = rf'G:\GE\skin_12_data_2d\region_{region_index}'
nuclei_file_name = rf'centroids.csv'

nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)

if len(sys.argv) >= 3:
    nuclei_file_path = sys.argv[2]

skin_threshold_dict = {
    1: 1000,
    2: 1500,
    3: 1000,
    4: 1000,
    5: 1000,
    6: 1000,
    7: 1000,
    8: 1000,
    9: 1000,
    10: 700,
    11: 1000,
    12: 1000,
}

skin_offset_dict = {
    1: [91, 71, 0],
    2: [25, 153, 0],
    3: [19, 54, 0],
    4: [34, 58, 0],
    5: [56, 30, 0],
    6: [0, 0, 0],
    7: [15, 43, 0],
    8: [25, 26, 0],
    9: [0, 42, 0],
    10: [20, 42, 0],
    11: [16, 54, 0],
    12: [29, 2, 0],
}

n_headers, n_columns = my_csv.read_csv(nuclei_file_path)
for i in range(0, 5):  # len(n_headers)):
    n_columns[n_headers[i]] = [value for value in n_columns[n_headers[i]]]
# n_columns['Y'] = [float(value) for value in n_columns['Y']]
# n_columns['X'] = [float(value) for value in n_columns['X']]
for i in range(len(n_columns['X'])):
    if top_left[0] < float(n_columns['X'][i]) * scale < bottom_right[0] and \
            top_left[1] < float(n_columns['Y'][i]) * scale < bottom_right[1]:
        # temp_z = float(n_columns['Z'][i])
        # temp_z_int = int(math.floor(temp_z))
        # z = z_list[temp_z_int] - z_list[0] + temp_z - temp_z_int
        z = float(n_columns['Z'][i])
        if n_columns['cell_type'][i] == 'CD31':
            vessel_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            vessel_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
            vessel_z_list.append(z * scale)
        elif n_columns['cell_type'][i] == 'Skin':
            offset_x, offset_y, offset_z = skin_offset_dict[region_index]
            x_temp = (float(n_columns['X'][i]) + offset_x) * scale - top_left[0]
            if x_temp < skin_threshold_dict[region_index]:
                skin_x_list.append(x_temp)
                skin_y_list.append((float(n_columns['Y'][i]) + offset_y) * scale - top_left[1])
                skin_z_list.append(z * scale)
        else:
            nuclei_id_list.append(i)
            nuclei_type_list.append(n_columns['cell_type'][i])
            nuclei_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            nuclei_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
            nuclei_z_list.append(z * scale)
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
print("Nuclei & Damage count: ", len(nuclei_x_list))
x_min, x_max = min(nuclei_x_list), max(nuclei_x_list)
y_min, y_max = min(nuclei_y_list), max(nuclei_y_list)
z_min, z_max = min(nuclei_z_list), max(nuclei_z_list)
margin_index = 0.05
x_margin = (x_max - x_min) * margin_index
y_margin = (y_max - y_min) * margin_index
z_margin = (z_max - z_min) * margin_index * 2

output_root_path = nuclei_root_path
nuclei_output_name = 'nuclei.csv'
nuclei_output_path = os.path.join(output_root_path, nuclei_output_name)
vessel_output_name = 'vessel.csv'
vessel_output_path = os.path.join(output_root_path, vessel_output_name)
skin_output_name = 'skin.csv'
skin_output_path = os.path.join(output_root_path, skin_output_name)

damage_type_list = ['P53', 'KI67', 'DDB2']

# reduce skin size
print(f"skin x min/max: {min(skin_x_list)} - {max(skin_x_list)}")
print(f"skin y min/max: {min(skin_y_list)} - {max(skin_y_list)}")
print(f"skin z min/max: {min(skin_z_list)} - {max(skin_z_list)}")
print(f"Original skin size: {len(skin_x_list)}")

temp_dict = {}
for i in range(len(skin_x_list)):
    if (skin_y_list[i], skin_z_list[i]) not in temp_dict:
        temp_dict[(skin_y_list[i], skin_z_list[i])] = skin_x_list[i]
    else:
        if temp_dict[(skin_y_list[i], skin_z_list[i])] > skin_x_list[i]:
            temp_dict[(skin_y_list[i], skin_z_list[i])] = skin_x_list[i]

skin_x_list, skin_y_list, skin_z_list = [], [], []
for key in temp_dict:
    skin_y_list.append(key[0])
    skin_z_list.append(key[1])
    skin_x_list.append(temp_dict[key])
print(f"Sampled skin size: {len(skin_x_list)}")

# calculate blood vessel distance
for nid in range(len(nuclei_id_list)):
    _min_vessel_dist = 1000 * scale
    _min_skin_dist = 50000 * scale
    _nx = nuclei_x_list[nid]
    _ny = nuclei_y_list[nid]
    _nz = nuclei_z_list[nid]
    _min_vessel_x = _nx
    _min_vessel_y = _ny
    _min_vessel_z = _nz
    _min_skin_x = _nx
    _min_skin_y = _ny
    _min_skin_z = _nz
    if nuclei_type_list[nid] in damage_type_list:
        _min_vessel_dist = -1
        _has_near = False
        z_threshold = 0.5
        y_threshold = 2
        while not _has_near:
            y_threshold += 0.5
            if y_threshold >= 7.5:
                print("NO NEAR")
                _min_skin_dist = 0
                break
            for v in range(len(skin_x_list)):
                _sx = skin_x_list[v]
                _sy = skin_y_list[v]
                _sz = skin_z_list[v]
                # add new criteria for skin
                # if abs(_sz - _nz <= 1) and abs(_nx - _sx) < _min_skin_dist and abs(_ny - _sy) < _min_skin_dist:
                if _sx < _nx \
                        and abs(_sz - _nz) <= z_threshold \
                        and abs(_nx - _sx) <= _min_skin_dist \
                        and abs(_ny - _sy) <= y_threshold:
                    _dist = math.sqrt((_nx - _sx) ** 2 + (_ny - _sy) ** 2 + (_nz - _sz) ** 2)
                    if _dist < _min_skin_dist:
                        _has_near = True
                        _min_skin_dist = _dist
                        _min_skin_x = _sx
                        _min_skin_y = _sy
                        _min_skin_z = _sz
    else:
        _min_skin_dist = -1
        _has_near = False
        for v in range(len(vessel_x_list)):
            _vx = vessel_x_list[v]
            _vy = vessel_y_list[v]
            _vz = vessel_z_list[v]
            if abs(_nx - _vx) < _min_vessel_dist and abs(_ny - _vy) < _min_vessel_dist and abs(_nz - _vz) <= 0.5:
                _dist = math.sqrt((_nx - _vx) ** 2 + (_ny - _vy) ** 2 + (_nz - _vz) ** 2)
                if _dist < _min_vessel_dist:
                    _has_near = True
                    _min_vessel_dist = _dist
                    _min_vessel_x = _vx
                    _min_vessel_y = _vy
                    _min_vessel_z = _vz
        if not _has_near:
            print("NO NEAR")
    nuclei_vessel_distance_list.append(_min_vessel_dist)
    nuclei_nearest_vessel_x_list.append(_min_vessel_x)
    nuclei_nearest_vessel_y_list.append(_min_vessel_y)
    nuclei_nearest_vessel_z_list.append(_min_vessel_z)
    nuclei_skin_distance_list.append(_min_skin_dist)
    nuclei_nearest_skin_x_list.append(_min_skin_x)
    nuclei_nearest_skin_y_list.append(_min_skin_y)
    nuclei_nearest_skin_z_list.append(_min_skin_z)
    if nid % 100 == 0:
        print('\r' + str(nid), end='')
print()

# calculate both distance
# for nid in range(len(nuclei_id_list)):
#     _min_vessel_dist = 100 * scale
#     _min_skin_dist = 50000 * scale
#     _nx = nuclei_x_list[nid]
#     _ny = nuclei_y_list[nid]
#     _nz = nuclei_z_list[nid]
#     _min_vessel_x = _nx
#     _min_vessel_y = _ny
#     _min_vessel_z = _nz
#     _min_skin_x = _nx
#     _min_skin_y = _ny
#     _min_skin_z = _nz
#     # if nuclei_type_list[nid] in damage_type_list:
#     # _min_vessel_dist = -1
#     _has_near = False
#     z_threshold = 1
#     y_threshold = 2
#     while not _has_near:
#         y_threshold += 0.5
#         if y_threshold >= 7.5:
#             print("NO NEAR")
#             _min_skin_dist = 0
#             break
#         for v in range(len(skin_x_list)):
#             _sx = skin_x_list[v]
#             _sy = skin_y_list[v]
#             _sz = skin_z_list[v]
#             # add new criteria for skin
#             # if abs(_sz - _nz <= 1) and abs(_nx - _sx) < _min_skin_dist and abs(_ny - _sy) < _min_skin_dist:
#             if _sx < _nx \
#                     and abs(_sz - _nz) <= z_threshold \
#                     and abs(_nx - _sx) <= _min_skin_dist \
#                     and abs(_ny - _sy) <= y_threshold:
#                 _dist = math.sqrt((_nx - _sx) ** 2 + (_ny - _sy) ** 2 + (_nz - _sz) ** 2)
#                 if _dist < _min_skin_dist:
#                     _has_near = True
#                     _min_skin_dist = _dist
#                     _min_skin_x = _sx
#                     _min_skin_y = _sy
#                     _min_skin_z = _sz
#     # else:
#     # _min_skin_dist = -1
#     _has_near = False
#     for v in range(len(vessel_x_list)):
#         _vx = vessel_x_list[v]
#         _vy = vessel_y_list[v]
#         _vz = vessel_z_list[v]
#         if abs(_nx - _vx) < _min_vessel_dist and abs(_ny - _vy) < _min_vessel_dist:
#             _dist = math.sqrt((_nx - _vx) ** 2 + (_ny - _vy) ** 2 + (_nz - _vz) ** 2)
#             if _dist < _min_vessel_dist:
#                 _has_near = True
#                 _min_vessel_dist = _dist
#                 _min_vessel_x = _vx
#                 _min_vessel_y = _vy
#                 _min_vessel_z = _vz
#     if not _has_near:
#         print("NO NEAR")
#     nuclei_vessel_distance_list.append(_min_vessel_dist)
#     nuclei_nearest_vessel_x_list.append(_min_vessel_x)
#     nuclei_nearest_vessel_y_list.append(_min_vessel_y)
#     nuclei_nearest_vessel_z_list.append(_min_vessel_z)
#     nuclei_skin_distance_list.append(_min_skin_dist)
#     nuclei_nearest_skin_x_list.append(_min_skin_x)
#     nuclei_nearest_skin_y_list.append(_min_skin_y)
#     nuclei_nearest_skin_z_list.append(_min_skin_z)
#     if nid % 100 == 0:
#         print('\r' + str(nid), end='')
# print()

assert len(nuclei_id_list) == len(nuclei_x_list) == len(nuclei_y_list) == len(nuclei_z_list) == \
       len(nuclei_vessel_distance_list) == len(nuclei_skin_distance_list) == \
       len(nuclei_nearest_vessel_x_list) == len(nuclei_nearest_vessel_y_list) == len(nuclei_nearest_vessel_z_list) == \
       len(nuclei_nearest_skin_x_list) == len(nuclei_nearest_skin_y_list) == len(nuclei_nearest_skin_z_list)

my_csv.write_csv(nuclei_output_path,
                 [nuclei_id_list,
                  nuclei_x_list,
                  nuclei_y_list,
                  nuclei_z_list,
                  nuclei_type_list,
                  nuclei_vessel_distance_list,
                  nuclei_nearest_vessel_x_list,
                  nuclei_nearest_vessel_y_list,
                  nuclei_nearest_vessel_z_list,
                  nuclei_skin_distance_list,
                  nuclei_nearest_skin_x_list,
                  nuclei_nearest_skin_y_list,
                  nuclei_nearest_skin_z_list],
                 ['id', 'x', 'y', 'z',
                  'type',
                  'vessel_distance', 'vx', 'vy', 'vz',
                  'skin_distance', 'sx', 'sy', 'sz'])

my_csv.write_csv(vessel_output_path,
                 [vessel_x_list, vessel_y_list, vessel_z_list],
                 ['x', 'y', 'z'])

my_csv.write_csv(skin_output_path,
                 [skin_x_list, skin_y_list, skin_z_list],
                 ['x', 'y', 'z'])

# import matplotlib.pyplot as plt
#
# # plt.scatter(vessel_x_list, vessel_y_list, c='r')
# # plt.scatter(nuclei_x_list, nuclei_y_list, c='b')
# plt.hist(nuclei_distance_list, bins=100)
# plt.show()


n_color = [cell_dict[cell_type]['color'] for cell_type in nuclei_type_list]
v_color = [cell_dict['CD31']['color']] * len(vessel_x_list)
s_color = [cell_dict['Skin']['color']] * len(skin_x_list)

# marker options:
# ['circle', 'circle-open', 'square', 'square-open', 'diamond', 'diamond-open', 'cross', 'x']


n_size = [cell_dict[cell_type]['size'] / 2 for cell_type in nuclei_type_list]
v_size = [cell_dict['CD31']['size'] / 2] * len(vessel_x_list)
s_size = [cell_dict['Skin']['size'] / 2] * len(skin_x_list)
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
n_data["nz"] = nuclei_z_list
n_data["nvx"] = nuclei_nearest_vessel_x_list
n_data["nvy"] = nuclei_nearest_vessel_y_list
n_data["nvz"] = nuclei_nearest_vessel_z_list
n_data["nsx"] = nuclei_nearest_skin_x_list
n_data["nsy"] = nuclei_nearest_skin_y_list
n_data["nsz"] = nuclei_nearest_skin_z_list
n_data["size"] = n_size
n_data["type"] = nuclei_type_list
n_data["vessel_distance"] = nuclei_vessel_distance_list
n_data["skin_distance"] = nuclei_skin_distance_list
n_data["color"] = n_color

n_df = pd.DataFrame(n_data)
print(n_df)

v_data = dict()
v_data["vx"] = vessel_x_list
v_data["vy"] = vessel_y_list
v_data["vz"] = vessel_z_list
v_data["color"] = v_color
v_data["size"] = v_size
v_df = pd.DataFrame(v_data)
print(v_df)

s_data = dict()
s_data["sx"] = skin_x_list
s_data["sy"] = skin_y_list
s_data["sz"] = skin_z_list
s_data["color"] = s_color
s_data["size"] = s_size
s_df = pd.DataFrame(s_data)
skin_display_rate = 1
s_df = s_df[s_df.index % skin_display_rate == 0]
print(s_df)
print(f"Displayed skin size: {len(s_df)}")

# https://stackoverflow.com/questions/56723792/plotly-how-to-efficiently-plot-a-large-number-of-line-shapes-where-the-points-a

# blood vessel distance
vd_df = n_df[n_df['vessel_distance'] >= 0]
v_df_one = generate_one_line_df(vd_df, key='v')
print(v_df_one)

# skin surface distance
sd_df = n_df[n_df['skin_distance'] >= 0]
s_df_one = generate_one_line_df(sd_df, key='s')
print(s_df_one)

traces_n = []
for cell_type in set(nuclei_type_list):
    traces_n.append(generate_nuclei_scatter(n_df, cell_type,
                                            legend_group=cell_dict[cell_type]['group']))
trace_v = generate_other_scatter(v_df, key='v', name=cell_dict['CD31']['legend'], symbol_name='CD31', visible=True,
                                 legend_group="Endothelial & Skin")
trace_s = generate_other_scatter(s_df, key='s', name=cell_dict['Skin']['legend'], symbol_name='Skin', visible=True,
                                 legend_group="Endothelial & Skin")
traces_vessel_line = generate_line(v_df_one, name=f"Distance-{cell_dict['CD31']['legend']}",
                                   color=cell_dict['CD31']['color'], visible=True, legend_group="Link")
traces_skin_line = generate_line(s_df_one, name=f"Distance-{cell_dict['Skin']['legend']}",
                                 color=cell_dict['Skin']['color'], visible='legendonly', legend_group="Link")
traces_n.extend([trace_v, trace_s, traces_vessel_line, traces_skin_line])
main_fig_count = len(traces_n)

image_hyperlink = f'https://raw.githubusercontent.com/hubmapconsortium/vccf-visualization-release/main/vheimages/S002_VHE_region_0{region_index:02d}.jpg'
main_subtitle = f'<br><sup>Region {region_index} / Donor {donor_dict[region_index]}  <a href="{image_hyperlink}">Virtual H&E Image Preview</a></sup>'
hist_subtitle = '<br><sup>Histogram</sup>'
horizontal_spacing = 0.03
fig = make_subplots(
    rows=3, cols=2,
    column_widths=[1.0, 0],
    row_heights=[0.7, 0.2, 0.1],
    specs=[
        [{"type": "Scatter3d", "colspan": 2}, None, ],
        [{"type": "Histogram"}, None],  # {"type": "Histogram"}
        [{"type": "Scatter"}, None],  # {"type": "Scatter"}
    ],
    horizontal_spacing=horizontal_spacing, vertical_spacing=0.02, shared_xaxes=True,
    subplot_titles=[f'Vascular Common Coordinate Framework 3D Visualization {main_subtitle}',
                    f'Distance to Endothelial Cells{hist_subtitle}', ],  # f'Distance to Skin Surface{hist_subtitle}',
)
for trace_n in traces_n:
    fig.add_trace(trace_n, 1, 1)

# layers display
layer_tol = 1
z_count = 24

for layer in range(0, z_count):
    zmin = (layer - layer_tol) * scale
    zmax = (layer + layer_tol) * scale
    zn_df = n_df[n_df['nz'].between(zmin, zmax, inclusive="neither")]
    zv_df = v_df[v_df['vz'].between(zmin, zmax, inclusive="neither")]
    zs_df = s_df[s_df['sz'].between(zmin, zmax, inclusive="neither")]

    # blood vessel distance
    zvd_df = zn_df[zn_df['vessel_distance'] >= 0]
    zv_df_one = generate_one_line_df(zvd_df, key='v')
    # print(zv_df_one)

    # skin surface distance
    zsd_df = zn_df[zn_df['skin_distance'] >= 0]
    zs_df_one = generate_one_line_df(zsd_df, key='s')
    # print(zs_df_one)

    traces_n = []
    for cell_type in set(nuclei_type_list):
        traces_n.append(generate_nuclei_scatter(zn_df, cell_type, show_legend=False, visible=False,
                                                legend_group="Damage" if cell_type in damage_type_list else "Cell"))
    trace_v = generate_other_scatter(zv_df, key='v', name=cell_dict['CD31']['legend'], symbol_name='CD31',
                                     visible=False, show_legend=False, legend_group="Vessel & Skin")
    trace_s = generate_other_scatter(zs_df, key='s', name=cell_dict['Skin']['legend'], symbol_name='Skin',
                                     visible=False, show_legend=False, legend_group="Vessel & Skin")
    traces_vessel_line = generate_line(zv_df_one, name=f"Distance-{cell_dict['CD31']['legend']}",
                                       color='grey', visible=False, show_legend=False, legend_group="Link")
    traces_skin_line = generate_line(zs_df_one, name=f"Distance-{cell_dict['Skin']['legend']}",
                                     color='grey', visible=False, show_legend=False, legend_group="Link")
    traces_n.extend([trace_v, trace_s, traces_vessel_line, traces_skin_line])
    for trace_n in traces_n:
        fig.add_trace(trace_n, 1, 1)

# bin_width = 10
# nbins = math.ceil((n_df["distance"].max() - n_df["distance"].min()) / bin_width)

bin_size = 3
bin_dict = dict(start=0, end=200, size=bin_size)

sbin_size = 10
sbin_dict = dict(start=0, end=5000, size=sbin_size)

# curve fitting
# from scipy import stats
#
# data_all = n_df["vessel_distance"].to_numpy()
# # data_all.sort()
# threshold = len(data_all) - np.count_nonzero(data_all)
# data_all = data_all[threshold:]
# curve_fit_all = stats.exponweib.fit(data_all, floc=0)
# pdf = stats.exponweib.pdf(data_all, *curve_fit_all)
# trace_curve_all = go.Scatter(x=data_all, y=pdf * len(data_all) * bin_size,
#                              marker=dict(color='grey'),
#                              showlegend=False,
#                              name='weibull fitting')


# add displot
# for cell_list, distance_type, col in zip([['T-Helper', 'T-Reg', 'T-Killer', 'CD68'], ["P53", "KI67", "DDB2", ]],  # ]],
#                                          ['vessel', 'skin'], [1, 2]):
for cell_list, distance_type, col in zip([['T-Helper', 'T-Reg', 'T-Killer', 'CD68'], ],
                                         ['vessel', ], [1, ]):
    print(cell_list, distance_type, col)
    hist_data = []
    hist_names = []
    for cell_type in cell_list:
        data = n_df[n_df['type'] == cell_type][f"{distance_type}_distance"]
        print(cell_type, data.size)
        if data.size > 5:
            hist_data.append(data)
            hist_names.append(cell_type)

    fig2 = ff.create_distplot(hist_data, hist_names, bin_size=bin_size if distance_type == 'vessel' else sbin_size,
                              histnorm='probability')  # , curve_type='normal')

    max_range = 1
    n_df = n_df[n_df['skin_distance'] != 0]
    for i in range(len(hist_data)):
        hist = fig2['data'][i]
        # fig.add_trace(go.Histogram(x=fig2['data'][i]['x'],xbins=bin_dict,opacity=0.5,
        #                            marker_color=color_dict[hist_names[i]], showlegend=False,
        #                            ), row=2, col=col)
        fig.add_trace(go.Histogram(
            x=n_df[n_df['type'] == hist_names[i]][f"{distance_type}_distance"],
            xbins=bin_dict if distance_type == 'vessel' else sbin_dict,
            opacity=0.6,
            marker=dict(color=cell_dict[hist_names[i]]['color']),
            showlegend=False,
            name=cell_dict[hist_names[i]]['legend']
        ), row=2, col=col)
        line = fig2['data'][len(hist_data) + i]
        line['y'] = line['y'] * len(hist_data[i])  # * bin_size *
        if not any(y > 1e5 for y in line['y']):
            fig.add_trace(go.Scatter(line,
                                     line=dict(color=cell_dict[hist_names[i]]['color'], width=2), showlegend=False,
                                     ), row=2, col=col)
        n_df[f'{hist_names[i]}_pos'] = 0.1 * (i + 1)
        fig.add_trace(go.Scatter(x=n_df[n_df['type'] == hist_names[i]][f"{distance_type}_distance"],
                                 y=n_df[f'{hist_names[i]}_pos'],
                                 mode='markers',
                                 opacity=0.6,
                                 marker=dict(color=cell_dict[hist_names[i]]['color'], symbol='line-ns-open'),
                                 showlegend=False,
                                 ), row=3, col=col)

    # some manual adjustments on the rugplot
    fig.update_yaxes(range=[0, 0.1 * (len(hist_names) + 1)],
                     tickvals=[0.1 * (i + 1) for i in range(len(hist_names))], ticktext=hist_names,
                     row=3, col=col)
    fig.update_xaxes(tickfont=dict(color='rgba(0,0,0,0)', size=1), row=2, col=col)

sub_title_text = "[Glomerulus-level (~2000 matching gloms) \n/ Crypt-level (~160 matching crypts)]"
title_text = f"Kidney/Colon - dice/recall/precision <br><sup>{sub_title_text}</sup>"

# Invisble scale for keep space instant
invisible_scale = go.Scatter3d(
    name="",
    visible=True,
    showlegend=False,
    opacity=0,
    hoverinfo='none',
    x=[x_min - x_margin, x_max + x_margin],
    y=[y_min - y_margin, y_max + y_margin],
    z=[z_min - z_margin, z_max + z_margin],
)
fig.add_trace(invisible_scale)

# Add dropdown
histogram_layout_buttons = list([
    dict(
        args=["barmode", "overlay"],
        label="Overlaid",
        method="relayout"
    ),
    dict(
        args=["barmode", "relative"],
        label="Stacked",
        method="relayout"
    ),
    dict(
        args=["barmode", "group"],
        label="Grouped",
        method="relayout"
    )
])
layer_select_buttons = []
# Create and add slider
steps = []
for i in range(z_count + 1):
    title = f"{str(i)}" if i != 0 else "All"
    step = dict(
        label=title,
        method="update",
        args=[{"visible": [False] * len(fig.data),
               "showlegend": [False] * len(fig.data)},
              {"title": ""}],  # layout attribute
    )
    for f in range(main_fig_count):
        step["args"][0]["visible"][i * main_fig_count + f] = True  # Toggle i'th trace to "visible"
        step["args"][0]["showlegend"][i * main_fig_count + f] = True
    rest = len(fig.data) - (z_count + 1) * main_fig_count
    for h in range(1, rest + 1):
        step["args"][0]["visible"][-h] = True
    steps.append(step)
layer_select_buttons = steps

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Slide: "},
    pad={"t": 0, "b": 0},
    steps=steps,
    yanchor='top', y=1,
    xanchor='right', x=1,
    lenmode='fraction', len=0.25
)]

# layout update
for annotation in fig['layout']['annotations'][:1]:
    annotation['x'] = 0
    annotation['xanchor'] = "left"
    annotation['y'] = 1
    annotation['yanchor'] = "top"
    annotation['font'] = dict(
        family="Arial, Bahnschrift",
        size=24, )
for annotation in fig['layout']['annotations'][1:]:
    annotation['x'] += 0.35 - horizontal_spacing
    annotation['xanchor'] = "right"
    annotation['y'] -= 0.05
    annotation['font'] = dict(
        family="Arial, Bahnschrift",
        size=18, )

background_color = 'rgb(240,246,255)'

# fig.add_annotation(dict(text="Slide:", showarrow=False,
#                         x=1, y=0.88, xref="paper", yref="paper", xanchor='right', yanchor='top', ))
fig.update_yaxes(rangemode='tozero', tickfont=dict(size=12), row=2)
fig.update_yaxes(rangemode='tozero', tickfont=dict(size=10), row=3)
fig.update_xaxes(rangemode='tozero', tickfont=dict(size=12), row=2)
fig.update_xaxes(rangemode='tozero', tickfont=dict(size=12), row=3)
fig.update_xaxes(ticklabelposition="outside", side="bottom",
                 title=dict(text="Distance (μm)", standoff=5, font_size=14), row=3, )
# fig.update_xaxes(range=[0, np.percentile(nuclei_vessel_distance_list, 99)], row=3, col=1)
fig.update_xaxes(range=[0, 210], row=3, col=1)
# fig.update_xaxes(range=[0, np.percentile(nuclei_skin_distance_list, 98)], row=3, col=2)
# fig.update_yaxes(ticklabelposition="inside", side="right", row=3, )
fig.update_yaxes(ticklabelposition="outside", side="left",
                 title=dict(text="Count #", standoff=5, font_size=14), row=2, col=1)
fig.update_traces(connectgaps=False, selector=dict(type="Scatter3d"))
fig.update_layout(
    updatemenus=[
        dict(
            buttons=histogram_layout_buttons,
            direction="right",
            pad={"r": 0, "t": 5},
            showactive=True,
            x=0,
            xanchor="left",
            y=-0.06,
            yanchor="bottom"
        ),

        # dict(
        #     buttons=layer_select_buttons,
        #     direction="down",
        #     pad={"r": 0, "t": 5},
        #     showactive=True,
        #     x=1,
        #     xanchor="right",
        #     y=0.85,
        #     yanchor="top"
        # ),
    ],
    font=dict(
        family="Arial, Bahnschrift",
        size=14,
        # color="RebeccaPurple"
    ),
    margin=dict(
        l=5,
        r=5,
        b=5,
        t=5,
        pad=0
    ),
    legend=dict(
        groupclick="toggleitem",
        yanchor="top",
        y=0.95,
        xanchor="left",
        x=0
    ),
    barmode='overlay',
    sliders=sliders,
    scene=dict(
        aspectmode='data',
        xaxis=dict(nticks=10, backgroundcolor=background_color, ),
        yaxis=dict(nticks=10, backgroundcolor=background_color, ),
        zaxis=dict(nticks=5, backgroundcolor=background_color, ),
    ),
    plot_bgcolor=background_color,
)

fig.write_html(os.path.join(nuclei_root_path, f"region_{region_index}.html"))
if show_html:
    fig.show()
