import statistics

target_root_path = r"G:\GE\skin_12_data"

print("Region", end='')
for i in range(5):
    print("\t\tAverage\tMedian\t%", end='')
print()

cell_types = ['all', 'CD68', 'T-Helper', 'T-Killer', 'T-Reg']
region_list = [11, 3, 8, 9, 1, 12, 5, 4, 2, 10, 7]
for region_id in region_list:
    target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"

    cell_file = open(target_file_path, 'r')
    cell_file.readline()
    cell_lines = cell_file.readlines()

    distances = {'all': []}

    for line in cell_lines:
        content = line.split(',')
        type = content[4]
        distance = content[5]
        if type in cell_types:
            if type not in distances:
                distances[type] = []
            else:
                distances[type].append(float(distance))
                distances['all'].append(float(distance))

    # print("Region ", region_id)
    # for key in distances:
    #     print("\t", key)
    #     print("\t\tAverage Distance: ", statistics.mean(distances[key]))
    #     print("\t\tMedian Distance: ", statistics.median(distances[key]))

    print(region_id, end='')
    for key in cell_types:
        print("\t", key, end='')
        if key in distances:
            dis_mean = statistics.mean(distances[key])
            dis_median = statistics.median(distances[key])
            percentage = len(distances[key]) / len(distances['all'])
        else:
            dis_mean = 0
            dis_median = 0
            percentage = 0
        print(f"\t{dis_mean}", end='')
        print(f"\t{dis_median}", end='')
        print(f"\t{percentage}", end='')
    print()
#
# distances = {'all': []}
# for region_id in [1, 3, 6, 8, 9, 11]:
#     target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
#
#     cell_file = open(target_file_path, 'r')
#     cell_file.readline()
#     cell_lines = cell_file.readlines()
#
#     for line in cell_lines:
#         content = line.split(',')
#         type = content[4]
#         distance = content[5]
#         if type not in distances:
#             distances[type] = []
#         else:
#             distances[type].append(float(distance))
#             distances['all'].append(float(distance))
#
# print("Sun", end='')
# for key in ['all', 'CD68', 'T-Reg', 'T-Helper']:
#     print("\t", key, end='')
#     print(f"\t{statistics.mean(distances[key])}", end='')
#     print(f"\t{statistics.median(distances[key])}", end='')
#     print(f"\t{len(distances[key]) / len(distances['all'])}", end='')
# print()
#
# distances = {'all': []}
# for region_id in [2, 4, 5, 7, 10, 12]:
#     target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
#
#     cell_file = open(target_file_path, 'r')
#     cell_file.readline()
#     cell_lines = cell_file.readlines()
#
#     for line in cell_lines:
#         content = line.split(',')
#         type = content[4]
#         distance = content[5]
#         if type not in distances:
#             distances[type] = []
#         else:
#             distances[type].append(float(distance))
#             distances['all'].append(float(distance))
#
# print("Non-sun", end='')
# for key in ['all', 'CD68', 'T-Reg', 'T-Helper']:
#     print("\t", key, end='')
#     print(f"\t{statistics.mean(distances[key])}", end='')
#     print(f"\t{statistics.median(distances[key])}", end='')
#     print(f"\t{len(distances[key]) / len(distances['all'])}", end='')
# print()
#
# distances = {'all': []}
# for region_id in region_list:
#     target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
#
#     cell_file = open(target_file_path, 'r')
#     cell_file.readline()
#     cell_lines = cell_file.readlines()
#
#     for line in cell_lines:
#         content = line.split(',')
#         type = content[4]
#         distance = content[5]
#         if type in cell_types:
#             if type not in distances:
#                 distances[type] = []
#             else:
#                 distances[type].append(float(distance))
#                 distances['all'].append(float(distance))
#
# print("All ", end='')
# for key in cell_types:
#     print("\t", key, end='')
#     print(f"\t{statistics.mean(distances[key])}", end='')
#     print(f"\t{statistics.median(distances[key])}", end='')
#     print(f"\t{len(distances[key]) / len(distances['all'])}", end='')
# print()
