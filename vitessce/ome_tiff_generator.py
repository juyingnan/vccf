import os
import sys
import pandas as pd
import numpy as np
import ast
from skimage.draw import polygon
from vitessce.data_utils import multiplex_img_to_ome_tiff


def generate_cell_mask(shape, vertices):
    rr, cc = polygon([v[1] for v in vertices], [v[0] for v in vertices])
    mask = np.zeros(shape)
    mask[rr, cc] = 1
    return mask


def convert_str_to_list(row):
    return [list(i) for i in ast.literal_eval(row)]


# Default region_index
region_index = 3

# Check if at least one command-line argument is given
if len(sys.argv) >= 2:
    # Use the given argument as region_index
    region_index = int(sys.argv[1])

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

cell_types = ['T-Killer', 'T-Helper', 'T-Reg', 'CD68', 'vessel']

# determine the shape of your canvas
height = cell_table['y'].max() + 30
width = cell_table['x'].max() + 30
shape = (height, width)
shape = tuple(map(int, shape))

# initialize an empty mask for each cell type
masks = {cell_type: np.zeros(shape, dtype=np.uint16) for cell_type in cell_types}

for index, row in cell_table.iterrows():
    mask = generate_cell_mask(shape, row['vertices'])
    masks[row['type']] += (mask * (index + 1)).astype(np.uint16)

# Create an ordered list of masks
mask_list = [masks[cell_type] for cell_type in cell_types]

# Stack masks into a 3D array. The new array has shape (n, m, len(cell_types)),
# where n and m are the dimensions of the original masks.
bitmask_arr = np.dstack(mask_list)

# Ensure the axes are in the CYX order by transposing the array
bitmask_arr = np.transpose(bitmask_arr, (2, 0, 1))

# Save the masks
multiplex_img_to_ome_tiff(bitmask_arr, cell_types, nuclei_file_path.replace('csv', 'ome.tif'), axes="CYX")
