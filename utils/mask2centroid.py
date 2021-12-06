import math
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

non_nuclei_types = ['P53', 'KI67', 'DDB2']

# read mask image
root_path = r"C:\Users\bunny\Desktop\Region3_Slide88_Visualization"
image_list = ['CD4_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked_CD3_Masked.tif',
              'CD68_S88_AFRemoved_pyr16_region_003_Prob_WSI_Masked.tif',
              'CD8_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked_CD3_Masked.tif',
              'DDB2_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked.tif',
              'FOXP3_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked_CD3_Masked.tif',
              'KI67_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked.tif',
              'P53_S88_AFRemoved_pyr16_region_003_Prob_DAPI_Seg_BinThresh_WSI_Masked.tif',
              ]
resize_index = 1
if len(sys.argv) >= 2:
    image_path = sys.argv[1]
if len(sys.argv) >= 3:
    resize_index = int(sys.argv[2])
preview = False

vessels = []
blood_vessel_image_path = 'CD31_S88_AFRemoved_pyr16_region_003_Prob_WSI_Masked_BinThresh0.tif'
blood_vessel_img = imageio.imread(os.path.join(root_path, blood_vessel_image_path))
cell_type = blood_vessel_image_path.split('_')[0]
if len(blood_vessel_img.shape) == 2:
    mask = blood_vessel_img
else:
    mask = np.array(blood_vessel_img[:, :, 0])
vessel_location = np.where(mask > 0.5)
vessel_index = 10
count = 0
for x, y in zip(vessel_location[0], vessel_location[1]):
    count += 1
    if count % vessel_index == 0:
        vessels.append([x, y])
print(f"{len(vessels)} vessels")

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
        vx, vy = x, y
        distance = 0
        if cell_type not in non_nuclei_types:
            distance = 500
            for vessel_coor in vessels:
                _vx, _vy = vessel_coor[0], vessel_coor[1]
                if abs(_vx - x) <= distance and abs(_vy - y) <= distance:
                    _dis = math.sqrt((_vx - x) ** 2 + (_vy - y) ** 2)
                    if _dis < distance:
                        distance = _dis
                        vx, vy = _vx, _vy
            if distance == 300:
                print("NO NEAR")
        cells[cell_type].append([x, y, vx, vy, distance])

print(cells)

id = 0

id_list = []
x_list = []
y_list = []
vx_list = []
vy_list = []
dis_list = []
type_list = []

for key in cells:
    for coor in cells[key]:
        id_list.append(id)
        id += 1
        x_list.append(coor[0])
        y_list.append(coor[1])
        vx_list.append(coor[2])
        vy_list.append(coor[3])
        dis_list.append(coor[4])
        type_list.append(key)

my_csv.write_csv(os.path.join(root_path, "nuclei.csv"),
                 [id_list,
                  x_list,
                  y_list,
                  type_list,
                  vx_list,
                  vy_list,
                  dis_list],
                 ['id', 'x', 'y', 'type', 'vx', 'vy', 'distance'])

print(f"{len(id_list)} cells/damages saved")

id = 0
vid_list = []
vx_list = []
vy_list = []
for vessel in vessels:
    vid_list.append(id)
    id += 1
    vx_list.append(vessel[0])
    vy_list.append(vessel[1])

my_csv.write_csv(os.path.join(root_path, "vessel.csv"),
                 [vid_list,
                  vx_list,
                  vy_list, ],
                 ['vid', 'vx', 'vy'])
print(f"{len(vid_list)} vessels saved")
