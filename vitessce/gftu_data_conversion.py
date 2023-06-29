import json
import os
import pandas as pd

folder = r'F:\Projects\VCCF\hackathon_temp\crypts'

image_index = 'a'
rescale_index = 1.2

# VU "gold" standard reading
gt_file_name = os.path.join(folder, f'{image_index}.json')

path_list = [gt_file_name]

# student json reading
name_list = ["Ground Truth", "Tom", "Gleb", "Whats goin on", "Deeplive.exe", "Deepflash2"]
for i in [1, 2, 3, 4, 5]:
    path_list.append(os.path.join(rf"{folder}\{i}", f"{i}{image_index}.json"))
json_count = len(path_list)

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
    if i == 0:
        vertices_list = [list(zip(x, y)) for x, y in zip(x_list, y_list)]
    else:
        vertices_list = [list(zip(y, x)) for x, y in zip(x_list, y_list)]

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
