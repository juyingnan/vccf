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
        rr, cc = line(int(vertices[0][1]), int(vertices[0][0]),
                      int(vertices[1][1]), int(vertices[1][0]))
        mask[rr, cc] = value
        # selem = disk(1)
        # mask = dilation(mask, selem)
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
    # Stack masks into a 3D array. The new array has shape (n, m, len(cell_types)),
    # where n and m are the dimensions of the original masks.
    bitmask_stack = np.dstack(mask_list)
    return bitmask_stack


# Default region_index
region_index = 3

scale = 0.5

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
nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)
vessel_file_path = os.path.join(nuclei_root_path, vessel_file_name)

cell_table = pd.read_csv(nuclei_file_path)
link_table = pd.read_csv(vessel_file_path)

# convert the vertices column from string to list
cell_table['vertices'] = cell_table['vertices'].apply(convert_str_to_list)
link_table['vertices'] = link_table['vertices'].apply(convert_str_to_list)
cell_table['vertices'] = cell_table['vertices'].apply(lambda x: [[int(i[0] * scale), int(i[1] * scale)] for i in x])
link_table['vertices'] = link_table['vertices'].apply(lambda x: [[int(i[0] * scale), int(i[1] * scale)] for i in x])

cell_types = ['T-Killer', 'T-Helper', 'T-Reg', 'CD68', 'vessel']
links_types = ["T-Killer_link", 'T-Helper_link', 'T-Reg_link', 'CD68_link']
color_dict = {'T-Killer': 1, 'T-Helper': 2, 'T-Reg': 3, 'CD68': 4, 'vessel': 5,
              "T-Killer_link": 1, 'T-Helper_link': 2, 'T-Reg_link': 3, 'CD68_link': 4}

# determine the shape of your canvas
height = (cell_table['y'].max() + 30) * scale
width =(cell_table['x'].max() + 30) * scale
shape = (height, width)
shape = tuple(map(int, shape))
print(shape)

print("Generating cell masks...")
cell_mask_stack = generate_mask_arr(cell_types, cell_table, shape)
print("Generating link masks...")
link_mask_stack = generate_mask_arr(links_types, link_table, shape, is_line=True)

layer_combine = True

if layer_combine:
    for i in range(len(links_types)):  # As there are 4 link mask layers
        cell_mask_stack[:, :, i] = np.maximum(cell_mask_stack[:, :, i], link_mask_stack[:, :, i])
    mask_stack = cell_mask_stack
    final_types = cell_types
else:
    # stack cell_mask_stack and link_mask_stack
    mask_stack = np.dstack((cell_mask_stack, link_mask_stack))
    final_types = cell_types + links_types

# Ensure the axes are in the CYX order by transposing the array
bitmask_arr = np.transpose(mask_stack, (2, 0, 1))

# Save the masks
print("Saving masks...")

multiplex_img_to_ome_tiff(bitmask_arr, final_types,
                          nuclei_file_path.replace('.csv', f'_region_{region_index}.ome.tif'),
                          axes="CYX")
