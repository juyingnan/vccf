def try_parse_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val


target_root_path = r"G:\GE\skin_12_data"
cell_file_path = r"C:\Users\bunny\Desktop\Centroids_New_0916.txt"

# bv_file = open(bv_file_path, 'r')
# bv_lines = bv_file.readlines()

cell_file = open(cell_file_path, 'r')
cell_lines = cell_file.readlines()

cells = {}
type_abr = {
    "_TRegulatory": "T-Reg",
    "TRegulator": "T-Reg",
    "THelper": "T-Helper",
    "TKiller": "T-Killer",
    "Macrophage": "CD68",
    "Blood Vessels": "CD31",
}
headline = "ID,X,Y,Z,cell_type\n"

current_region = ""
current_type = ""
for line_content in cell_lines:
    line = line_content.strip().rstrip(",")
    if len(line) == 0:
        continue
    if line.startswith("Region"):
        if line not in cells:
            cells[line] = {}
        current_region = line
        current_type = ""
        continue
    elif line.startswith("Mac") or \
            line.startswith("Blood") or \
            line.startswith("T"):
        assert current_region != ""
        current_type = line
        cells[current_region][current_type] = []
    elif line.startswith("Label"):
        continue
    else:
        assert current_region != ""
        assert current_type != ""
        if current_type in type_abr:
            cells[current_region][current_type].append(line + "," + type_abr[current_type])
        else:
            print(f"{current_region}, {current_type} not in the type dict")

# write csv
for region in cells:
    print(region, ":")
    for cell_type in cells[region]:
        print(f"\t{cell_type}: {len(cells[region][cell_type])}")
    region_id = try_parse_int(region[6:])
    if region_id is None:
        print(f"Region name {region} fails to parse")
        break
    target_file_path = target_root_path + rf"\region_{region_id}\centroids.csv"
    csv_file = open(target_file_path, "w")
    csv_file.write(headline)
    for cell_type in cells[region]:
        for line in cells[region][cell_type]:
            csv_file.write(line + "\n")
    csv_file.close()
