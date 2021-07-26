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
nuclei_distance_list = list()
nuclei_nearest_vessel_x_list = list()
nuclei_nearest_vessel_y_list = list()
nuclei_nearest_vessel_z_list = list()
vessel_x_list = list()
vessel_y_list = list()
vessel_z_list = list()
z_list = [77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101]
micro_per_pixel = 0.325
scale = 16 * micro_per_pixel

top_left = [0, 0]
bottom_right = [1000000, 1000000]
# top_left = [5350 * micro_per_pixel, 3900 * micro_per_pixel]
# bottom_right = [7150 * micro_per_pixel, 4700 * micro_per_pixel]


region_index = 10

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
        temp_z_int = int(math.floor(temp_z))
        z = z_list[temp_z_int] - z_list[0] + temp_z - temp_z_int
        if n_columns['cell_type'][i] == 'CD31':
            vessel_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            vessel_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
            vessel_z_list.append(z * scale)
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
    nuclei_distance_list.append(_min_dist)
    nuclei_nearest_vessel_x_list.append(_min_vessel_x)
    nuclei_nearest_vessel_y_list.append(_min_vessel_y)
    nuclei_nearest_vessel_z_list.append(_min_vessel_z)
    if nid % 100 == 0:
        print('\r' + str(nid), end='')

print(len(nuclei_id_list), len(nuclei_x_list), len(nuclei_y_list), len(nuclei_distance_list),
      len(nuclei_nearest_vessel_x_list), len(nuclei_nearest_vessel_y_list))

my_csv.write_csv(nuclei_output_path,
                 [nuclei_id_list,
                  nuclei_x_list,
                  nuclei_y_list,
                  nuclei_z_list,
                  nuclei_type_list,
                  nuclei_distance_list,
                  nuclei_nearest_vessel_x_list,
                  nuclei_nearest_vessel_y_list,
                  nuclei_nearest_vessel_z_list],
                 ['id', 'x', 'y', 'z',
                  'type',
                  'distance', 'vx', 'vy', 'vz'])

my_csv.write_csv(vessel_output_path,
                 [vessel_x_list, vessel_y_list, vessel_z_list],
                 ['x', 'y', 'z'])

# import matplotlib.pyplot as plt
#
# # plt.scatter(vessel_x_list, vessel_y_list, c='r')
# # plt.scatter(nuclei_x_list, nuclei_y_list, c='b')
# plt.hist(nuclei_distance_list, bins=100)
# plt.show()

color_dict = {
    'CD68': "gold",
    'Machrophage': "gold",
    'CD31': "red",
    'Blood Vessel': "red",
    'T-Helper': "blue",
    'T-Reg': "green",
    'T-Regulatory': "green",
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
n_data["nz"] = nuclei_z_list
n_data["size"] = n_size
n_data["type"] = nuclei_type_list
n_data["distance"] = nuclei_distance_list
n_data["color"] = n_color

n_df = pd.DataFrame(n_data)

print(n_df)
# https://stackoverflow.com/questions/56723792/plotly-how-to-efficiently-plot-a-large-number-of-line-shapes-where-the-points-a

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
                           opacity=0.75,
                           line=dict(
                               color=v_color,
                               width=0
                           )
                       ))
traces_line = go.Scatter3d(x=v_df_one.vx,
                           y=v_df_one.vy,
                           z=v_df_one.vz,
                           mode="lines",
                           name="Distance",
                           opacity=0.5,
                           line=dict(
                               color='grey',
                               width=1, ))

# bin_width = 10
# nbins = math.ceil((n_df["distance"].max() - n_df["distance"].min()) / bin_width)

bin_dict = dict(start=0, end=150, size=5)

traces_histogram_all = go.Histogram(
    x=n_df["distance"],
    xbins=bin_dict,
    opacity=0.1,
    marker=dict(color="gray"),
    showlegend=False,
    name='All'
)

traces_histogram_CD68 = go.Histogram(
    x=n_df[n_df['type'] == "CD68"]["distance"],
    xbins=bin_dict,
    opacity=0.5,
    marker=dict(color=color_dict['CD68']),
    showlegend=False,
    name='CD68/Machrophage'
)

traces_histogram_TH = go.Histogram(
    x=n_df[n_df['type'] == "T-Helper"]["distance"],
    xbins=bin_dict,
    opacity=0.5,
    marker=dict(color=color_dict['T-Helper']),
    showlegend=False,
    name='T-Helper'
)

traces_histogram_TR = go.Histogram(
    x=n_df[n_df['type'] == "T-Reg"]["distance"],
    xbins=bin_dict,
    opacity=0.5,
    marker=dict(color=color_dict['T-Reg']),
    showlegend=False,
    name='T-Regulatory'
)

# contents = [trace_n, trace_v, traces_line]
fig = make_subplots(
    rows=2, cols=4,
    column_widths=[0.25, 0.25, 0.25, 0.25],
    row_heights=[0.8, 0.2],
    specs=[[{"type": "Scatter3d", "colspan": 4}, None, None, None],
           [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}]],
    horizontal_spacing=0.015, vertical_spacing=0.02,
    subplot_titles=[f'VCCF 3D - Region {region_index}', 'Histogram - ALL', 'Histogram - CD68/Machrophage',
                    'Histogram - T-Helper', 'Histogram - T-Regulatory'],
)
for trace_n in traces_n:
    fig.add_trace(trace_n, 1, 1)
fig.add_trace(trace_v, 1, 1)
fig.add_trace(traces_line, 1, 1)

# fig.add_trace(traces_histogram_all, 2, 1)
fig.add_trace(traces_histogram_CD68, 2, 1)
fig.add_trace(traces_histogram_TH, 2, 1)
fig.add_trace(traces_histogram_TR, 2, 1)
fig.add_trace(traces_histogram_CD68, 2, 2)
fig.add_trace(traces_histogram_TH, 2, 3)
fig.add_trace(traces_histogram_TR, 2, 4)

fig['layout'].update(
    # title='GE VCCF 3D',
    scene=dict(
        aspectmode='data'
    ))
# fig = go.Figure(contents, layout=layout)
# fig.update_layout(showlegend=False, )
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.95,
    xanchor="left",
    x=0.05
),
    barmode='relative', )
fig.update_xaxes(title_text="Distance (um)", row=2, col=2)
fig.update_yaxes(title_text="Count #", row=2, col=1)
fig.update_xaxes(range=[0, 150], row=2)
fig.update_traces(connectgaps=False, selector=dict(type="Scatter3d"))

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
    ]
)

fig.write_html(os.path.join(nuclei_root_path, "result.html"))
fig.show()
