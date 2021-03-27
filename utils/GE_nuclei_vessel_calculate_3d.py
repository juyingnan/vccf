from skimage import io
import math
import csv
import os
import sys
import random
import matplotlib.pyplot as plt


# from mpl_toolkits.mplot3d import Axes3D


def write_csv(path, list_of_columns, list_of_names=None):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        if list_of_names is not None:
            writer.writerow(list_of_names)
        lines = []
        for _i in range(len(list_of_columns[0])):
            lines.append([column[_i] for column in list_of_columns])
        writer.writerows(lines)


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        _headers = next(reader, None)

        # get column
        _columns = {}
        for h in _headers:
            _columns[h] = []
        for _row in reader:
            for _h, _v in zip(_headers, _row):
                _columns[_h].append(_v)

        for item in _headers:
            print(item)

        return _headers, _columns


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

input_id = 86
fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(111, projection='3d')
ax._axis3don = False

top_left = [5350, 3900]
bottom_right = [7150, 4700]

max_z = 308

vessel_x_list = list()
vessel_y_list = list()

vessel_root_path = \
    r'G:\GE\HubmapDemoDay_Dec14th_2020_Vessel_Nuclei_Segmentation_NucleiQuantification\VesselSegmentation'
vessel_image_file_name = rf'CD31_S{input_id}_AFRemoved_pyr16_region_006_Vessel_Prob_p.tif'
vessel_image_path = os.path.join(vessel_root_path, vessel_image_file_name)
if len(sys.argv) >= 4:
    vessel_image_path = sys.argv[3]

vessel_image = io.imread(vessel_image_path)[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]  # [::-1, :]

for i in range(len(vessel_image)):
    row = vessel_image[i]
    for j in range(len(row)):
        pixel = row[j]
        if pixel[0] < 100:  # if pixel[0] > 200:
            vessel_y_list.append(i)
            vessel_x_list.append(j)
print(len(vessel_x_list))

vessel_z_list = [random.randint(0, max_z) for i in range(len(vessel_x_list))]

for k, color in zip([3, 68], ['gold', 'red']):
    nuclei_id_list = list()
    nuclei_x_list = list()
    nuclei_y_list = list()
    nuclei_distance_list = list()
    nuclei_nearest_vessel_x_list = list()
    nuclei_nearest_vessel_y_list = list()
    nuclei_nearest_vessel_z_list = list()

    CD_index = k
    CD_str = f'CD{CD_index}_'
    if CD_index == 0:
        CD_str = ""
    index = 1
    if len(sys.argv) >= 2:
        input_id = sys.argv[1]

    nuclei_root_path = \
        r'G:\GE\HubmapDemoDay_Dec14th_2020_Vessel_Nuclei_Segmentation_NucleiQuantification\NucleiQuantification'
    nuclei_file_name = rf'{CD_str}quant_slide{input_id}_region6.csv'
    # nuclei_file_name = rf'quant_slide{input_id}_region6.csv'

    nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)

    if len(sys.argv) >= 3:
        nuclei_file_path = sys.argv[2]

    n_headers, n_columns = read_csv(nuclei_file_path)
    for i in range(0, 7):  # len(n_headers)):
        n_columns[n_headers[i]] = [float(value) for value in n_columns[n_headers[i]]]
    n_columns['Y'] = [float(value) for value in n_columns['Y']]

    full_nuclei_x_list = [float(value / index) for value in n_columns['X']]
    full_nuclei_y_list = [float(value / index) for value in n_columns['Y']]
    full_nuclei_id_list = [int(value) for value in n_columns['Cell ID']]

    if CD_index == 0:
        nuclei_x_list = []
        nuclei_y_list = []
        nuclei_id_list = []
        for i in range(len(full_nuclei_x_list)):
            if top_left[0] < full_nuclei_x_list[i] < bottom_right[0] and \
                    top_left[1] < full_nuclei_y_list[i] < bottom_right[1]:
                nuclei_x_list.append(full_nuclei_x_list[i] - top_left[0])
                nuclei_y_list.append(full_nuclei_y_list[i] - top_left[1])
                nuclei_id_list.append(full_nuclei_id_list[i])
    else:
        nuclei_x_list = full_nuclei_x_list
        nuclei_y_list = full_nuclei_y_list
        nuclei_id_list = full_nuclei_id_list

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

    output_root_path = r'G:\GE\HubmapDemoDay_Dec14th_2020_Vessel_Nuclei_Segmentation_NucleiQuantification\output'
    nuclei_output_name = nuclei_file_name.replace('region6', 'region6_nuclei')
    nuclei_output_path = os.path.join(output_root_path, nuclei_output_name)
    vessel_output_name = nuclei_file_name.replace('region6', 'region6_vessel')
    vessel_output_path = os.path.join(output_root_path, vessel_output_name)

    write_csv(nuclei_output_path,
              [nuclei_id_list,
               nuclei_x_list,
               nuclei_y_list],
              ['id', 'x', 'y'])

    write_csv(vessel_output_path,
              [vessel_x_list, vessel_y_list],
              ['x', 'y'])

    nuclei_z_list = [random.randint(0, max_z) for i in range(len(nuclei_x_list))]

    for nid in range(len(nuclei_id_list)):
        _min_dist = 1600 / index
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

    write_csv(nuclei_output_path,
              [nuclei_id_list,
               nuclei_x_list,
               nuclei_y_list,
               # nuclei_class_list,
               nuclei_distance_list,
               nuclei_nearest_vessel_x_list,
               nuclei_nearest_vessel_y_list],
              ['id', 'x', 'y',
               # 'class',
               'distance', 'vx', 'vy'])

    write_csv(vessel_output_path,
              [vessel_x_list, vessel_y_list],
              ['x', 'y'])

    color_max = max(nuclei_distance_list)
    colors = ['#%02x%02x%02x' % (0, int(255 * value / color_max), int(255 * (color_max - value) / color_max))
              for value in nuclei_distance_list]

    ax.scatter(nuclei_x_list, nuclei_y_list, nuclei_z_list, color=color, marker="o", s=15)
    ax.scatter(vessel_x_list, vessel_y_list, vessel_z_list, color='b', marker=".", s=0.1)

    for i in range(len(nuclei_id_list)):
        ax.plot([nuclei_x_list[i], nuclei_nearest_vessel_x_list[i]],
                [nuclei_y_list[i], nuclei_nearest_vessel_y_list[i]],
                [nuclei_z_list[i], nuclei_nearest_vessel_z_list[i]],
                color='k', linewidth=0.1)

ax.set_xlim3d(0, 1500)
ax.set_ylim3d(0, 1500)
ax.set_zlim3d(0, 1500)

plt.show()

# plt.scatter(vessel_x_list, vessel_y_list, c='r')
# plt.scatter(nuclei_x_list, nuclei_y_list, c='b')
plt.hist(nuclei_distance_list, bins=100)
plt.show()
