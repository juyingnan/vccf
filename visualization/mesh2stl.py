import math
import os
import sys
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import alphashape
from stl import mesh
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

region_index = 2
show_html = True

cell_type_list = ['CD68', 'T-Helper', 'T-Killer', 'T-Reg']
damage_type_list = ['P53', 'KI67', 'DDB2']
filter = 'all'

if len(sys.argv) >= 2:
    region_index = int(sys.argv[1])
if len(sys.argv) >= 3:
    filter = sys.argv[2]

nuclei_root_path = rf'G:\GE\skin_12_data\region_{region_index}'
nuclei_file_name = rf'centroids.csv'

nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)

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

# import matplotlib.pyplot as plt

index = 5000
for alpha in range(1, 11):
    for i in range(len(nuclei_types)):
        cell_type = nuclei_types[i]
        color = cell_dict[cell_type]['color']
        mesh_test = traces_n[i]
        points_3d = [(mesh_test.x[i] / index, mesh_test.y[i] / index, mesh_test.z[i] / index) for i in
                     range(len(mesh_test.x))]
        # alpha = alphashape.optimizealpha(points_3d)
        # print(alpha)

        if len(points_3d) > 10:
            alpha_shape = alphashape.alphashape(points_3d, alpha=alpha)
            stl_shape = mesh.Mesh(np.zeros(alpha_shape.faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, f in enumerate(alpha_shape.faces):
                for j in range(3):
                    stl_shape.vectors[i][j] = alpha_shape.vertices[f[j], :]
            stl_path = nuclei_root_path + fr'\stl\region_{region_index}_{cell_type}_alpha_{alpha}.stl'
            stl_shape.save(stl_path)
            print(f"STL file saved to {stl_path}")
            # print()
            # fig = plt.figure()
            # ax = plt.axes(projection='3d')
            # ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces)
            # plt.show()
