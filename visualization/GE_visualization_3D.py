import math
import os
import sys
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.graph_objs import Layout
from plotly.subplots import make_subplots

sys.path.insert(1, r'C:\Users\bunny\PycharmProjects\vccf_visualization')
import utils.kidney_nuclei_vessel_calculate as my_csv

# prs = Presentation(r'C:\Users\bunny\Desktop\KidneyAnnotated-GW.pptx')
# print(prs.slide_height, prs.slide_width)
# slide = prs.slides[0]
#
# shapes = slide.shapes
#
# print(len(shapes))
#
# unit_per_um = 1024646 / 50
# unit_per_pixel = 28346400 / 2232
# pixel_per_um = unit_per_um / unit_per_pixel
#
nuclei_id_list = list()
nuclei_type_list = list()
nuclei_x_list = list()
nuclei_y_list = list()
nuclei_z_list = list()
nuclei_vessel_distance_list = list()
nuclei_skin_distance_list = list()
nuclei_nearest_vessel_x_list = list()
nuclei_nearest_vessel_y_list = list()
nuclei_nearest_vessel_z_list = list()
nuclei_nearest_skin_x_list = list()
nuclei_nearest_skin_y_list = list()
nuclei_nearest_skin_z_list = list()
vessel_x_list = list()
vessel_y_list = list()
vessel_z_list = list()
skin_x_list = list()
skin_y_list = list()
skin_z_list = list()
z_list = [77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101]
micro_per_pixel = 0.325
scale = 16 * micro_per_pixel

top_left = [0, 0]
bottom_right = [1000000, 1000000]
# top_left = [5350 * micro_per_pixel, 3900 * micro_per_pixel]
# bottom_right = [7150 * micro_per_pixel, 4700 * micro_per_pixel]


region_index = 1
show_html = True

if len(sys.argv) >= 2:
    region_index = sys.argv[1]
    show_html = False

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
        # temp_z = float(n_columns['Z'][i])
        # temp_z_int = int(math.floor(temp_z))
        # z = z_list[temp_z_int] - z_list[0] + temp_z - temp_z_int
        z = float(n_columns['Z'][i])
        if n_columns['cell_type'][i] == 'CD31':
            vessel_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            vessel_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
            vessel_z_list.append(z * scale)
        elif n_columns['cell_type'][i] == 'Skin':
            skin_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            skin_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
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
print(len(nuclei_x_list))

output_root_path = nuclei_root_path
nuclei_output_name = 'nuclei.csv'
nuclei_output_path = os.path.join(output_root_path, nuclei_output_name)
vessel_output_name = 'vessel.csv'
vessel_output_path = os.path.join(output_root_path, vessel_output_name)
skin_output_name = 'skin.csv'
skin_output_path = os.path.join(output_root_path, skin_output_name)

# calculate blood vessel distance
for nid in range(len(nuclei_id_list)):
    _min_dist = 100 * scale
    _min_vessel_x = 0
    _min_vessel_y = 0
    _min_vessel_z = 0
    _nx = nuclei_x_list[nid]
    _ny = nuclei_y_list[nid]
    _nz = nuclei_z_list[nid]
    _has_near = False
    for v in range(len(vessel_x_list)):
        _vx = vessel_x_list[v]
        _vy = vessel_y_list[v]
        _vz = vessel_z_list[v]
        if abs(_nx - _vx) < _min_dist and abs(_ny - _vy) < _min_dist:
            _dist = math.sqrt((_nx - _vx) ** 2 + (_ny - _vy) ** 2 + (_nz - _vz) ** 2)
            if _dist < _min_dist:
                _has_near = True
                _min_dist = _dist
                _min_vessel_x = _vx
                _min_vessel_y = _vy
                _min_vessel_z = _vz
    if not _has_near:
        print("NO NEAR")
    nuclei_vessel_distance_list.append(_min_dist)
    nuclei_nearest_vessel_x_list.append(_min_vessel_x)
    nuclei_nearest_vessel_y_list.append(_min_vessel_y)
    nuclei_nearest_vessel_z_list.append(_min_vessel_z)
    if nid % 100 == 0:
        print('\r' + str(nid), end='')

# calculate skin surface distance
for nid in range(len(nuclei_id_list)):
    _min_dist = 3000 * scale
    _min_skin_x = 0
    _min_skin_y = 0
    _min_skin_z = 0
    _nx = nuclei_x_list[nid]
    _ny = nuclei_y_list[nid]
    _nz = nuclei_z_list[nid]
    _has_near = False
    for v in range(len(skin_x_list)):
        _sx = skin_x_list[v]
        _sy = skin_y_list[v]
        _sz = skin_z_list[v]
        if abs(_nx - _sx) < _min_dist and abs(_ny - _sy) < _min_dist:
            _dist = math.sqrt((_nx - _sx) ** 2 + (_ny - _sy) ** 2 + (_nz - _sz) ** 2)
            if _dist < _min_dist:
                _has_near = True
                _min_dist = _dist
                _min_skin_x = _sx
                _min_skin_y = _sy
                _min_skin_z = _sz
    if not _has_near:
        print("NO NEAR")
    nuclei_skin_distance_list.append(_min_dist)
    nuclei_nearest_skin_x_list.append(_min_skin_x)
    nuclei_nearest_skin_y_list.append(_min_skin_y)
    nuclei_nearest_skin_z_list.append(_min_skin_z)
    if nid % 100 == 0:
        print('\r' + str(nid), end='')
print()
print(len(nuclei_id_list))
# assert len(nuclei_id_list) == len(nuclei_x_list) == len(nuclei_y_list) == len(nuclei_z_list) == \
#        len(nuclei_vessel_distance_list) == len(nuclei_skin_distance_list) == \
#        len(nuclei_nearest_vessel_x_list) == (nuclei_nearest_vessel_y_list) == (nuclei_nearest_vessel_z_list) == \
#        len(nuclei_nearest_skin_x_list) == (nuclei_nearest_skin_y_list) == (nuclei_nearest_skin_z_list)

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

color_dict = {
    'CD68': "gold",
    'Macrophage': "gold",
    'CD31': "red",
    'Blood Vessel': "red",
    'T-Helper': "blue",
    'T-Reg': "mediumspringgreen",
    'T-Regulatory': "mediumspringgreen",
    'T-Regulator': "mediumspringgreen",
    'T-Killer': "purple",

    'P53': "chocolate",
    'KI67': "cyan",
    'DDB2': "olivedrab",
    'Skin': "darkgrey"
}
n_color = [color_dict[cell_type] for cell_type in nuclei_type_list]
v_color = [color_dict['CD31']] * len(vessel_x_list)
s_color = [color_dict['Skin']] * len(skin_x_list)

size_dict = {
    'CD68': 15.89,
    'Macrophage': 15.89,
    'CD31': 16.83,
    'Blood Vessel': 16.83,
    'T-Helper': 16.96,
    'T-Reg': 17.75,
    'T-Regulatory': 17.75,
    'T-Regulator': 17.75,

    # placeholder, not accurate
    'T-Killer': 16,
    'P53': 16,
    'KI67': 16,
    'DDB2': 16,
    'Skin': 16,
}

cell_type_dict = {
    'CD68': "Macrophage / CD68",
    'Macrophage': "Macrophage / CD68",
    'CD31': "Blood Vessel",
    'Blood Vessel': "Blood Vessel",
    'T-Helper': "T-Helper",
    'T-Reg': "T-Regulator",
    'T-Regulatory': "T-Regulator",
    'T-Regulator': "T-Regulator",
    'T-Killer': "T-Killer",
    "P53": "P53",
    "KI67": "KI67",
    "DDB2": "DDB2",
    'Skin': "Skin Surface",
}

histogram_location_dict = {
    'T-Helper': [2, 2],
    'T-Reg': [2, 3],
    'T-Regulator': [2, 3],
    'T-Killer': [2, 4],
    'CD68': [3, 1],
    "Macrophage / CD68": [3, 1],
    "P53": [3, 2],
    "KI67": [3, 3],
    "DDB2": [3, 4],
}

marker_dict = {
    'T-Helper': 'circle',
    'T-Reg': 'circle',
    'T-Regulator': 'circle',
    'T-Killer': 'circle',
    'CD68': 'circle',
    "Macrophage / CD68": 'circle',
    'CD31': 'circle',
    "P53": 'x',
    "KI67": 'x',
    "DDB2": 'x',
    "Skin": 'diamond',
}

n_size = [size_dict[cell_type] / 2 for cell_type in nuclei_type_list]
v_size = [size_dict['CD31'] / 2] * len(vessel_x_list)
s_size = [size_dict['Skin'] / 2] * len(skin_x_list)
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
n_data["size"] = n_size
n_data["type"] = nuclei_type_list
n_data["vessel_distance"] = nuclei_vessel_distance_list
n_data["skin_distance"] = nuclei_skin_distance_list
n_data["color"] = n_color

n_df = pd.DataFrame(n_data)

print(n_df)
# https://stackoverflow.com/questions/56723792/plotly-how-to-efficiently-plot-a-large-number-of-line-shapes-where-the-points-a

# blood vessel distance
line_x = [None] * (len(nuclei_x_list) + len(nuclei_nearest_vessel_x_list))
line_y = [None] * (len(nuclei_y_list) + len(nuclei_nearest_vessel_y_list))
line_z = [None] * (len(nuclei_z_list) + len(nuclei_nearest_vessel_z_list))
line_x[::2] = nuclei_nearest_vessel_x_list
line_x[1::2] = nuclei_x_list
line_y[::2] = nuclei_nearest_vessel_y_list
line_y[1::2] = nuclei_y_list
line_z[::2] = nuclei_nearest_vessel_z_list
line_z[1::2] = nuclei_z_list

v_data = dict()
v_data["vx"] = line_x
v_data["vy"] = line_y
v_data["vz"] = line_z
# v_color = ['red'] * len(vessel_x_list)
# v_data["color"] = v_color
v_df = pd.DataFrame(v_data)
v_gap = (v_df.iloc[1::2]
         .assign(vx=np.nan, vy=np.nan)
         .rename(lambda x: x + .5))
v_df_one = pd.concat([v_df, v_gap], sort=False).sort_index().reset_index(drop=True)
v_df_one.loc[v_df_one.isnull().any(axis=1), :] = np.nan
print(v_df_one)

# skin surface distance
line_x = [None] * (len(nuclei_x_list) + len(nuclei_nearest_skin_x_list))
line_y = [None] * (len(nuclei_y_list) + len(nuclei_nearest_skin_y_list))
line_z = [None] * (len(nuclei_z_list) + len(nuclei_nearest_skin_z_list))
line_x[::2] = nuclei_nearest_skin_x_list
line_x[1::2] = nuclei_x_list
line_y[::2] = nuclei_nearest_skin_y_list
line_y[1::2] = nuclei_y_list
line_z[::2] = nuclei_nearest_skin_z_list
line_z[1::2] = nuclei_z_list

s_data = dict()
s_data["sx"] = line_x
s_data["sy"] = line_y
s_data["sz"] = line_z
# v_color = ['red'] * len(vessel_x_list)
# v_data["color"] = v_color
s_df = pd.DataFrame(s_data)
s_gap = (s_df.iloc[1::2]
         .assign(sx=np.nan, sy=np.nan)
         .rename(lambda x: x + .5))
s_df_one = pd.concat([s_df, s_gap], sort=False).sort_index().reset_index(drop=True)
s_df_one.loc[s_df_one.isnull().any(axis=1), :] = np.nan
print(s_df_one)

# import plotly.express as px
#
# range_max = max(bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]) * 1.2
#
# fig = px.scatter_3d(n_df, x='nx', y='ny', z='nz',
#                     color='color', opacity=0.7,  # size=1,
#                     range_x=[0, range_max], range_y=[0, range_max], range_z=[0, range_max])
# # fig.add_scatter3d(px.scatter_3d(v_df, x='vx', y='vy', z='vz', color='color'))
# import plotly.graph_objects as go
#
# fig.add_trace(go.Scatter3d(v_df, x='vx', y='vy', z='vz'))
#
# fig.show()

traces_n = []
for cell_type in set(nuclei_type_list):
    traces_n.append(go.Scatter3d(x=n_df[n_df['type'] == cell_type]["nx"],
                                 y=n_df[n_df['type'] == cell_type]["ny"],
                                 z=n_df[n_df['type'] == cell_type]["nz"],
                                 mode="markers",
                                 name=cell_type_dict[cell_type],
                                 marker=dict(
                                     size=n_df[n_df['type'] == cell_type]["size"],
                                     color=n_df[n_df['type'] == cell_type]["color"],
                                     symbol=marker_dict[cell_type],
                                     opacity=0.75,
                                     line=dict(
                                         color=n_df[n_df['type'] == cell_type]["color"],
                                         width=0
                                     )
                                 )))
trace_v = go.Scatter3d(x=vessel_x_list, y=vessel_y_list, z=vessel_z_list,
                       mode="markers",
                       name="Blood Vessel",
                       marker=dict(
                           size=v_size,
                           color=v_color,
                           symbol=marker_dict['CD31'],
                           opacity=0.5,
                           line=dict(
                               color=v_color,
                               width=0
                           )
                       ))
trace_s = go.Scatter3d(x=skin_x_list, y=skin_y_list, z=skin_z_list,
                       mode="markers",
                       name="Skin Surface",
                       marker=dict(
                           size=s_size,
                           color=s_color,
                           symbol=marker_dict['Skin'],
                           opacity=0.5,
                           line=dict(
                               color=s_color,
                               width=0)),
                       visible='legendonly')
traces_vessel_line = go.Scatter3d(x=v_df_one.vx,
                                  y=v_df_one.vy,
                                  z=v_df_one.vz,
                                  mode="lines",
                                  name="Distance-Blood Vessel",
                                  opacity=0.5,
                                  line=dict(
                                      color='grey',
                                      width=1, ))
traces_skin_line = go.Scatter3d(x=s_df_one.sx,
                                y=s_df_one.sy,
                                z=s_df_one.sz,
                                mode="lines",
                                name="Distance-Skin",
                                opacity=0.5,
                                line=dict(
                                    color='grey',
                                    width=1, ),
                                visible='legendonly')

# bin_width = 10
# nbins = math.ceil((n_df["distance"].max() - n_df["distance"].min()) / bin_width)

bin_size = 5
bin_dict = dict(start=0, end=200, size=bin_size)

traces_histogram_all = go.Histogram(
    x=n_df["vessel_distance"],
    xbins=bin_dict,
    opacity=0.1,
    marker=dict(color="gray"),
    showlegend=False,
    name='All'
)

vessel_histograms = []
skin_histograms = []
for distance_type, histograms in zip(['vessel', 'skin'], [vessel_histograms, skin_histograms]):
    for cell_type in ['T-Helper', 'T-Reg', 'T-Killer', 'CD68', "P53", "KI67", "DDB2"]:
        traces_histogram = go.Histogram(
            x=n_df[n_df['type'] == cell_type][f"{distance_type}_distance"],
            xbins=bin_dict,
            opacity=0.5,
            marker=dict(color=color_dict[cell_type]),
            showlegend=False,
            name=cell_type_dict[cell_type]
        )
        histograms.append(traces_histogram)

hist_subtitle = '<br><sup>Histogram</sup>'
fig = make_subplots(
    rows=3, cols=4,
    column_widths=[0.25, 0.25, 0.25, 0.25],
    row_heights=[0.6, 0.2, 0.2],
    specs=[
        [{"type": "Scatter3d", "colspan": 4}, None, None, None, ],
        [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, ],
        [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, ],
    ],
    horizontal_spacing=0.015, vertical_spacing=0.02,
    subplot_titles=[f'VCCF 3D - Region {region_index}',
                    f'ALL{hist_subtitle}',
                    f'T-Helper{hist_subtitle}', f'T-Regulator{hist_subtitle}', f'T-Killer{hist_subtitle}',
                    f'CD68{hist_subtitle}', f'P53{hist_subtitle}', f'KI67{hist_subtitle}', f'DDB2{hist_subtitle}'],
)
for trace_n in traces_n:
    fig.add_trace(trace_n, 1, 1)
fig.add_trace(trace_v, 1, 1)
fig.add_trace(trace_s, 1, 1)
fig.add_trace(traces_vessel_line, 1, 1)
fig.add_trace(traces_skin_line, 1, 1)

# curve fitting
from scipy import stats

data_all = n_df["vessel_distance"].to_numpy()
data_all.sort()
threshold = len(data_all) - np.count_nonzero(data_all)
data_all = data_all[threshold:]
curve_fit_all = stats.exponweib.fit(data_all, floc=0)
pdf = stats.exponweib.pdf(data_all, *curve_fit_all)
trace_curve_all = go.Scatter(x=data_all, y=pdf * len(data_all) * bin_size,
                             marker=dict(color='grey'),
                             showlegend=False,
                             name='weibull fitting')

# fig.add_trace(traces_histogram_all, 2, 1)
# ['T-Helper', 'T-Reg', 'T-Killer', 'CD68', "P53", "KI67", "DDB2"]
# fig.add_trace(trace_curve_all, 2, 1)
for hist in vessel_histograms:
    fig.add_trace(hist, 2, 1)
for vessel_histogram in vessel_histograms:
    name = vessel_histogram['name']
    fig.add_trace(vessel_histogram, histogram_location_dict[name][0], histogram_location_dict[name][1])

fig['layout'].update(
    # title='GE VCCF 3D',
    scene=dict(
        aspectmode='data'
    ))

annotations = [a.to_plotly_json() for a in fig["layout"]["annotations"]]
for annotation in annotations:
    annotation['x'] += 0.0875
    annotation['y'] -= 0.035
# annotations.append(dict(
#     x=100, y=50,  # annotation point
#     xref='x1',
#     yref='y1',
#     text=f'a={curve_fit_all[0]:.2f},c={curve_fit_all[1]:.2f}',
#     showarrow=False,
# ))
fig["layout"]["annotations"] = annotations

# fig = go.Figure(contents, layout=layout)
# fig.update_layout(showlegend=False, )
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.95,
    xanchor="left",
    x=0.05
),
    barmode='relative', )
fig.update_xaxes(title_text="Distance (um)", row=3, col=2)
fig.update_yaxes(title_text="Count #", row=2, col=1)
fig.update_xaxes(range=[0, 200], row=2)
fig.update_xaxes(range=[0, 200], row=3)
fig.update_yaxes(rangemode='tozero', row=2)
fig.update_yaxes(rangemode='tozero', row=3)
fig.update_traces(connectgaps=False, selector=dict(type="Scatter3d"))

sub_title_text = "[Glomerulus-level (~2000 matching gloms) \n/ Crypt-level (~160 matching crypts)]"
title_text = f"Kidney/Colon - dice/recall/precision <br><sup>{sub_title_text}</sup>"

# Add dropdown
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["barmode", "relative"],
                    label="Stacked",
                    method="relayout"
                ),
                dict(
                    args=["barmode", "overlay"],
                    label="Overlaid",
                    method="relayout"
                ),
                dict(
                    args=["barmode", "group"],
                    label="Grouped",
                    method="relayout"
                )
            ]),
            direction="up",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="right",
            y=-0.05,
            yanchor="bottom"
        ),
    ],
    font=dict(
        family="Bahnschrift, Arial",
        size=15,
        # color="RebeccaPurple"
    )
)

fig.write_html(os.path.join(nuclei_root_path, f"region_{region_index}.html"))
if show_html:
    fig.show()
