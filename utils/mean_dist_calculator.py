import statistics

target_root_path = r"G:\GE\skin_12_data"

for i in range(4):
    print("\tAverage\tMedian", end='')
print()

for region_id in range(1, 13):
    target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"

    cell_file = open(target_file_path, 'r')
    cell_file.readline()
    cell_lines = cell_file.readlines()

    distances = {'all': []}

    for line in cell_lines:
        content = line.split(',')
        type = content[4]
        distance = content[5]
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

    print("Region ", region_id, end='')
    for key in ['all', 'CD68', 'T-Reg', 'T-Helper']:
        print("\t", key, end='')
        print(f"\t{statistics.mean(distances[key])}", end='')
        print(f"\t{statistics.median(distances[key])}", end='')
    print()
