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
z_scale = 5

top_left = [0, 0]
bottom_right = [1000000, 1000000]

region_index = 3
show_html = True

cell_type_list = ['CD68', 'T-Helper', 'T-Killer', 'T-Reg']
damage_type_list = ['P53', 'KI67', 'DDB2']
filter = 'all'

if len(sys.argv) >= 2:
    region_index = int(sys.argv[1])
    show_html = False
if len(sys.argv) >= 3:
    filter = sys.argv[2]

nuclei_root_path = rf'G:\GE\skin_12_data\region_{region_index}'
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
            vessel_z_list.append(z * scale * z_scale)
        elif n_columns['cell_type'][i] == 'Skin':
            offset_x, offset_y, offset_z = skin_offset_dict[region_index]
            x_temp = (float(n_columns['X'][i]) + offset_x) * scale - top_left[0]
            if x_temp < skin_threshold_dict[region_index]:
                skin_x_list.append(x_temp)
                skin_y_list.append((float(n_columns['Y'][i]) + offset_y) * scale - top_left[1])
                skin_z_list.append(z * scale * z_scale)
        else:
            nuclei_id_list.append(i)
            nuclei_type_list.append(n_columns['cell_type'][i])
            nuclei_x_list.append(float(n_columns['X'][i]) * scale - top_left[0])
            nuclei_y_list.append(float(n_columns['Y'][i]) * scale - top_left[1])
            nuclei_z_list.append(z * scale * z_scale)
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
n_data["size"] = n_size
n_data["type"] = nuclei_type_list
n_data["color"] = n_color

n_df = pd.DataFrame(n_data)
print(n_df)

nuclei_types = list(set(nuclei_type_list))
result_path = f"cluster_region_{region_index}.html"
if filter == 'damage':
    nuclei_types = list(set(nuclei_types).intersection(damage_type_list))
    result_path = f"cluster_region_{region_index}_damage.html"
elif filter == 'cell':
    nuclei_types = list(set(nuclei_types).intersection(cell_type_list))
    result_path = f"cluster_region_{region_index}_cell.html"
nuclei_types.sort()
print(nuclei_types)

traces_n = []
for cell_type in nuclei_types:
    traces_n.append(generate_nuclei_scatter(n_df, cell_type,
                                            legend_group=cell_dict[cell_type]['group']))
main_fig_count = len(traces_n)

image_hyperlink = f'https://raw.githubusercontent.com/hubmapconsortium/vccf-visualization-release/main/vheimages/S002_VHE_region_0{region_index:02d}.jpg'
main_subtitle = f'<br><sup>Region {region_index} / Donor {donor_dict[region_index]}  <a href="{image_hyperlink}">Virtual H&E Image Preview</a></sup>'
hist_subtitle = '<br><sup>Histogram</sup>'
horizontal_spacing = 0.03
fig = go.Figure()
fig.update_layout(
    title=main_subtitle,
)
for trace_n in traces_n:
    fig.add_trace(trace_n)

for alpha in range(-1, 11):
    for i in range(len(nuclei_types)):
        cell_type = nuclei_types[i]
        color = cell_dict[cell_type]['color']
        mesh_test = traces_n[i]
        _3d_test = go.Mesh3d(x=mesh_test.x, y=mesh_test.y, z=mesh_test.z,
                             alphahull=alpha, name=nuclei_types[i] + ' Mesh',
                             color=color, opacity=0.150, legendgroup='Cluster Mesh', showlegend=True,
                             visible=True if alpha == -1 else False)
        fig.add_trace(_3d_test)

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

steps = []
for i in range(-1, 11):
    title = str(i)
    step = dict(
        label=title,
        method="update",
        args=[{"visible": [False] * len(fig.data),
               "showlegend": [False] * len(fig.data)
               },
              # {"title": ""},
              ],  # layout attribute
    )
    for f in range(main_fig_count):
        step["args"][0]["visible"][f] = True
        step["args"][0]["showlegend"][f] = True
        step["args"][0]["visible"][(i + 2) * main_fig_count + f] = True
        step["args"][0]["showlegend"][(i + 2) * main_fig_count + f] = True
    steps.append(step)

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
fig.update_traces(connectgaps=False, selector=dict(type="Scatter3d"))
fig.update_layout(
    # updatemenus=[
    #     dict(
    #         buttons=histogram_layout_buttons,
    #         direction="down",
    #         pad={"r": 0, "t": 5},
    #         showactive=True,
    #         x=0.9,
    #         xanchor="right",
    #         y=0.9,
    #         yanchor="top"
    #     ),
    # ],
    sliders=sliders,
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
    scene=dict(
        aspectmode='data',
        xaxis=dict(nticks=10, backgroundcolor=background_color, ),
        yaxis=dict(nticks=10, backgroundcolor=background_color, ),
        zaxis=dict(nticks=5, backgroundcolor=background_color, ),
    ),
    plot_bgcolor=background_color,
)

fig.write_html(os.path.join(nuclei_root_path, result_path))
if show_html:
    fig.show()
