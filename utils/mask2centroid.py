import os

import imageio
import json
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure, io
import copy
import sys
from skimage.transform import rescale, resize
from PIL import Image
import utils.kidney_nuclei_vessel_calculate as my_csv

Image.MAX_IMAGE_PIXELS = None

# read mask image
root_path = r"C:\Users\bunny\Desktop\Region3_Slide88_Visualization"
image_list = ['CD4_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked_CD3_Masked.tif',
              'CD68_S88_AFRemoved_pyr16_region_003_Prob_WSI_Masked.tif',
              'CD8_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked_CD3_Masked.tif',
              'DDB2_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked.tif',
              'FOXP3_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked_CD3_Masked.tif',
              'KI67_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked.tif',
              'P53_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked.tif', ]
resize_index = 1
if len(sys.argv) >= 2:
    image_path = sys.argv[1]
if len(sys.argv) >= 3:
    resize_index = int(sys.argv[2])
preview = False
cells = {}

for img_item in image_list:
    img_path = os.path.join(root_path, img_item)
    img = imageio.imread(img_path)
    cell_type = img_item.split('_')[0]
    cells[cell_type] = []
    print(cell_type)

    if len(img.shape) == 2:
        mask = img
    else:
        mask = np.array(img[:, :, 0])
    mask = np.where(mask > 0.5, 1, 0)
    # mask = resize(mask, (500,500), anti_aliasing=False)

    # get the contour
    contours = measure.find_contours(mask, 0.8)

    # contour to polygon
    polygons = []
    for object in contours:
        coords = []
        for point in object:
            coords.append([int(point[0]), int(point[1])])
        polygons.append(coords)

    for polygon in polygons:
        x = sum([polygon[i][0] for i in range(len(polygon))]) // len(polygon)
        y = sum([polygon[i][1] for i in range(len(polygon))]) // len(polygon)
        cells[cell_type].append([x, y])

print(cells)

id = 0

id_list = []
x_list = []
y_list = []
type_list = []

for key in cells:
    for coor in cells[key]:
        id_list.append(id)
        id += 1
        x_list.append(coor[0])
        y_list.append(coor[1])
        type_list.append(key)

my_csv.write_csv(os.path.join(root_path, "seg.csv"),
                 [id_list,
                  x_list,
                  y_list,
                  type_list, ],
                 ['id', 'x', 'y', 'type', ])
