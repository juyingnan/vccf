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
root_path = r"C:\Users\bunny\Desktop\ForYingnan\Region7\Slide78"
image_list = ['CD3_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              "CD4_S78_AFRemoved_pyr16_region_007_Prob_2_thre.tif",
              'CD8_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              'CD68_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              'DDB2_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              'FOXP3_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              'KI67_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              'P53_S78_AFRemoved_pyr16_region_007_Prob_thre.tif',
              ]
blood_vessel_image_path = 'CD31_S78_AFRemoved_pyr16_region_007_Prob.nii'

# root_path = r"C:\Users\bunny\Desktop\ForYingnan\Region11\Slide78"
# image_list = ['CD3_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               "CD4_S78_AFRemoved_pyr16_region_011_Prob_2.tif",
#               'CD8_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               'CD68_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               'DDB2_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               'FOXP3_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               'KI67_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               'P53_S78_AFRemoved_pyr16_region_011_Prob.tif',
#               ]
# blood_vessel_image_path = 'CD31_S78_AFRemoved_pyr16_region_011_Prob.nii'

threshold_list = [
    0.5, #CD3 ?
    #0.9, #CD4 1195
    0.6, #CD8 28
    0.6, #CD68 142
    0.5, #DDB2 154
    0.5, #FOXP3 106
    0.95, #KI67 765
    0.3, #P53 82
]

resize_index = 1
if len(sys.argv) >= 2:
    image_path = sys.argv[1]
if len(sys.argv) >= 3:
    resize_index = int(sys.argv[2])
preview = False

vessels = []

blood_vessel_img = imageio.imread(os.path.join(root_path, blood_vessel_image_path))
cell_type = blood_vessel_image_path.split('_')[0]
if len(blood_vessel_img.shape) == 2:
    mask = blood_vessel_img
else:
    mask = np.array(blood_vessel_img[:, :, 0])
vessel_location = np.where(mask > 0.9)
vessel_index = 5
count = 0
for x, y in zip(vessel_location[0], vessel_location[1]):
    count += 1
    if count % vessel_index == 0:
        vessels.append([x, y])
print(f"{len(vessels)} vessels")

cells = {}
for i in range(len(image_list)):
    img_item = image_list[i]
    threshold = 0.5# threshold_list[i]
    img_path = os.path.join(root_path, img_item)
    img = imageio.imread(img_path)
    cell_type = img_item.split('_')[0]
    cells[cell_type] = []
    print(cell_type)

    if len(img.shape) == 2:
        mask = img
    else:
        mask = np.array(img[0, :, :])
    mask = np.where(mask > threshold, 1, 0)
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

# print(cells)
for key in cells:
    print(key, len(cells[key]))

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
