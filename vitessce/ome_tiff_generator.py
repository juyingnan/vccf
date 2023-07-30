import os
import sys
import pandas as pd
import numpy as np
import ast
from tqdm import tqdm
from skimage.draw import polygon, line
from vitessce.data_utils import multiplex_img_to_ome_tiff
from skimage.morphology import disk, dilation


def generate_cell_mask(mask, value, vertices, is_line=False):
    if is_line:
        # Loop over pairs of vertices
        for i in range(len(vertices) - 1):
            rr, cc = line(int(vertices[i][1]), int(vertices[i][0]),
                          int(vertices[i + 1][1]), int(vertices[i + 1][0]))
            mask[rr, cc] = value
    else:
        rr, cc = polygon([v[1] for v in vertices], [v[0] for v in vertices])
        mask[rr, cc] = value


def convert_str_to_list(row):
    return [list(i) for i in ast.literal_eval(row)]


def generate_mask_arr(type_list, table, mask_shape, is_line=False):
    # initialize an empty mask for each cell type
    masks = {cell_type: np.zeros(mask_shape, dtype=np.uint8) for cell_type in type_list}
    for index, row in tqdm(table.iterrows(), total=len(table), desc='Processing rows'):
        generate_cell_mask(masks[row['type']], color_dict[row['type']], row['vertices'], is_line=is_line)

    # Create an ordered list of masks
    mask_list = [masks[cell_type] for cell_type in type_list]

    # make the line thicker by dilation
    if is_line:
        for i in range(len(mask_list)):
            selem = disk(2)
            mask_list[i] = dilation(mask_list[i], selem)

    # Stack masks into a 3D array. The new array has shape (n, m, len(cell_types)),
    # where n and m are the dimensions of the original masks.
    bitmask_stack = np.dstack(mask_list)
    return bitmask_stack


def vertices_str2list(table, zoom_scale):
    table['vertices'] = table['vertices'].apply(convert_str_to_list)
    table['vertices'] = table['vertices'].apply(lambda x: [[int(i[0] * zoom_scale), int(i[1] * zoom_scale)] for i in x])


# Default region_index
region_index = 3

scale = 16 * 0.325

# Check if at least one command-line argument is given
if len(sys.argv) >= 2:
    # Use the given argument as region_index
    region_index = int(sys.argv[1])
if len(sys.argv) >= 3:
    # Use the given argument as scale
    scale = float(sys.argv[2])

# Construct the path to the nuclei file
nuclei_root_path = rf'G:\GE\skin_12_data\region_{region_index}'
nuclei_file_name = 'cell_table.csv'
vessel_file_name = 'link_table.csv'
skin_file_name = 'skin_table.csv'
damage_file_name = 'damage_table.csv'
nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)
vessel_file_path = os.path.join(nuclei_root_path, vessel_file_name)
skin_file_path = os.path.join(nuclei_root_path, skin_file_name)
damage_file_path = os.path.join(nuclei_root_path, damage_file_name)

cell_table = pd.read_csv(nuclei_file_path)
link_table = pd.read_csv(vessel_file_path)
skin_table = pd.read_csv(skin_file_path)
damage_table = pd.read_csv(damage_file_path)

# convert the vertices column from string to list
vertices_str2list(cell_table, scale)
vertices_str2list(link_table, scale)
vertices_str2list(skin_table, scale)
vertices_str2list(damage_table, scale)

cell_types = ['T-Killer', 'T-Helper', 'T-Reg', 'CD68', 'vessel']
link_types = ["T-Killer_link", 'T-Helper_link', 'T-Reg_link', 'CD68_link']
damage_types = ['DDB2', 'P53', 'KI67']
skin_types = ['skin']
color_dict = {'T-Killer': 1, 'T-Helper': 2, 'T-Reg': 3, 'CD68': 4, 'vessel': 5,
              "T-Killer_link": 1, 'T-Helper_link': 2, 'T-Reg_link': 3, 'CD68_link': 4,
              'DDB2': 10, 'P53': 11, 'KI67': 12, 'skin': 13}

# determine the shape of your canvas
height = (cell_table['y'].max() + 30) * scale
width = (cell_table['x'].max() + 30) * scale
shape = (height, width)
shape = tuple(map(int, shape))
print(shape)

print("Generating cell masks...")
cell_mask_stack = generate_mask_arr(cell_types, cell_table, shape)
print("Generating link masks...")
link_mask_stack = generate_mask_arr(link_types, link_table, shape, is_line=True)
print("Generating damage masks...")
damage_mask_stack = generate_mask_arr(damage_types, damage_table, shape, is_line=True)
print("Generating skin masks...")
skin_mask_stack = generate_mask_arr(skin_types, skin_table, shape)

layer_combine = True

if layer_combine:
    for i in range(len(link_types)):  # As there are 4 link mask layers
        cell_mask_stack[:, :, i] = np.maximum(cell_mask_stack[:, :, i], link_mask_stack[:, :, i])
    # combine damage mask and skin mask
    combined_damage_mask_stack = np.amax(damage_mask_stack, axis=2)[:, :, np.newaxis]
    combined_skin_mask_stack = np.maximum(combined_damage_mask_stack, skin_mask_stack)
    mask_stack = np.dstack((cell_mask_stack, combined_skin_mask_stack))
    final_types = cell_types + skin_types
    assert len(final_types) == mask_stack.shape[2]
else:
    # stack cell_mask_stack and link_mask_stack
    mask_stack = np.dstack((cell_mask_stack, link_mask_stack, damage_mask_stack, skin_mask_stack))
    final_types = cell_types + link_types

# Ensure the axes are in the CYX order by transposing the array
bitmask_arr = np.transpose(mask_stack, (2, 0, 1))

# Save the masks
print("Saving masks...")

multiplex_img_to_ome_tiff(bitmask_arr, final_types,
                          nuclei_file_path.replace('.csv', f'_region_{region_index}.ome.tif'),
                          axes="CYX")
