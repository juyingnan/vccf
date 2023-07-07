import json
import os
import sys
import pandas as pd

folder = r'C:\Users\bunny\Desktop\test'

image_index = '00a67c839'
rescale_index = 1.0

# Check if at least one command-line argument is given
if len(sys.argv) >= 2:
    # Use the given argument as region_index
    image_index = sys.argv[1]
if len(sys.argv) >= 3:
    # Use the given argument as scale
    rescale_index = float(sys.argv[2])

path_list = []

# student json reading
name_list = ["Ground Truth", "Tom", "Gleb", "Whats goin on", "Deeplive.exe", "Deepflash2"]
for i in [0, 1, 2, 3, 4, 5]:
    path_list.append(os.path.join(rf"{folder}\{i}", f"{image_index}.json"))
json_count = len(path_list)

print(path_list)

df_list = []

for i in range(len(path_list)):
    path = path_list[i]
    with open(path) as data_file:
        data = json.load(data_file)

    coor_list = []

    for item in data:
        coor_list.extend(item["geometry"]["coordinates"])
    x_list = [[xy[0] // 2 // rescale_index for xy in coor] for coor in coor_list]
    y_list = [[xy[1] // 2 // rescale_index for xy in coor] for coor in coor_list]
    vertices_list = [list(zip(x, y)) for x, y in zip(x_list, y_list)]

    df_temp = pd.DataFrame({'id': range(1, len(vertices_list) + 1),
                            'type': name_list[i],
                            'vertices': vertices_list})
    df_list.append(df_temp)

color_dict = {"Ground Truth": 'yellow',
              'Tom': 'black',
              'Gleb': 'orangered',
              'Whats goin on': 'midnightblue',
              'Deeplive.exe': 'darkolivegreen',
              'Deepflash2': 'purple',
              }

for i in range(json_count):
    print(name_list[i], color_dict[name_list[i]], '\t', path_list[i])

# Concatenate all dataframes and save to a single CSV
df_final = pd.concat(df_list, ignore_index=True)
df_final.to_csv(os.path.join(folder, rf"{image_index}_all_coordinates.csv"), index=False)
