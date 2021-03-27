from skimage import io
import math
import csv
import os
import sys


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
        for row in reader:
            for h, v in zip(_headers, row):
                _columns[h].append(v)

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
nuclei_id_list = list()
nuclei_type_list = list()
nuclei_x_list = list()
nuclei_y_list = list()
nuclei_distance_list = list()
nuclei_nearest_vessel_x_list = list()
nuclei_nearest_vessel_y_list = list()
vessel_x_list = list()
vessel_y_list = list()

input_id = '38e2af3a115f13e7d90d33c4e5ca4e9e'
if len(sys.argv) >= 2:
    input_id = sys.argv[1]

nuclei_root_path = rf'G:\kidney\slideseq-cell-type-annotated\slideseq-cell-type-annotated\{input_id}'
nuclei_file_name = rf'expr_labeled.csv'

nuclei_file_path = os.path.join(nuclei_root_path, nuclei_file_name)

if len(sys.argv) >= 3:
    nuclei_file_path = sys.argv[2]

n_headers, n_columns = read_csv(nuclei_file_path)
for i in range(0, 4):  # len(n_headers)):
    n_columns[n_headers[i]] = [value for value in n_columns[n_headers[i]]]
# n_columns['Y'] = [float(value) for value in n_columns['Y']]
# n_columns['X'] = [float(value) for value in n_columns['X']]
for i in range(len(n_columns['ID'])):
    if n_columns['cell_type'][i] == 'Endothelial Cell':
        vessel_x_list.append(float(n_columns['X'][i]))
        vessel_y_list.append(float(n_columns['Y'][i]))
    nuclei_id_list.append(int(n_columns['ID'][i]))
    nuclei_type_list.append(n_columns['cell_type'][i])
    nuclei_x_list.append(float(n_columns['X'][i]))
    nuclei_y_list.append(float(n_columns['Y'][i]))
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

write_csv(nuclei_output_path,
          [nuclei_id_list,
           nuclei_x_list,
           nuclei_y_list,
           nuclei_type_list],
          ['id', 'x', 'y', 'type'])

write_csv(vessel_output_path,
          [vessel_x_list, vessel_y_list],
          ['x', 'y'])

for nid in range(len(nuclei_id_list)):
    _min_dist = 2000
    _min_vessel_x = 0
    _min_vessel_y = 0
    _nx = nuclei_x_list[nid]
    _ny = nuclei_y_list[nid]
    _has_near = False
    for v in range(len(vessel_x_list)):
        _vx = vessel_x_list[v]
        _vy = vessel_y_list[v]
        if abs(_nx - _vx) < _min_dist and abs(_ny - _vy) < _min_dist:
            _dist = math.sqrt((_nx - _vx) ** 2 + (_ny - _vy) ** 2)
            if _dist < _min_dist:
                _has_near = True
                _min_dist = _dist
                _min_vessel_x = _vx
                _min_vessel_y = _vy
    if not _has_near:
        print("NO NEAR")
    nuclei_distance_list.append(_min_dist)
    nuclei_nearest_vessel_x_list.append(_min_vessel_x)
    nuclei_nearest_vessel_y_list.append(_min_vessel_y)
    if nid % 100 == 0:
        print('\r' + str(nid), end='')

print(len(nuclei_id_list), len(nuclei_x_list), len(nuclei_y_list), len(nuclei_distance_list),
      len(nuclei_nearest_vessel_x_list), len(nuclei_nearest_vessel_y_list))

write_csv(nuclei_output_path,
          [nuclei_id_list,
           nuclei_x_list,
           nuclei_y_list,
           nuclei_type_list,
           nuclei_distance_list,
           nuclei_nearest_vessel_x_list,
           nuclei_nearest_vessel_y_list],
          ['id', 'x', 'y',
           'type',
           'distance', 'vx', 'vy'])

write_csv(vessel_output_path,
          [vessel_x_list, vessel_y_list],
          ['x', 'y'])

import matplotlib.pyplot as plt

# plt.scatter(vessel_x_list, vessel_y_list, c='r')
# plt.scatter(nuclei_x_list, nuclei_y_list, c='b')
plt.hist(nuclei_distance_list, bins=100)
plt.show()
