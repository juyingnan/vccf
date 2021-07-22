def tryParseInt(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val


target_root_path = "G:\GE\skin_12_data"
cell_file_path = r"C:\Users\bunny\Desktop\new\Centroids_New.txt"

# bv_file = open(bv_file_path, 'r')
# bv_lines = bv_file.readlines()

cell_file = open(cell_file_path, 'r')
cell_lines = cell_file.readlines()

cells = {}
type_abr = {
    "TRegulatory": "T-Reg",
    "THelper": "T-Helper",
    "Machrophage": "CD68",
    "Blood Vessels": "CD31",
}
headline = "ID,X,Y,Z,cell_type\n"

current_region = ""
current_type = ""
for line in cell_lines:
    l = line.strip()
    if l.startswith("Region"):
        cells[l] = {}
        current_region = l
        current_type = ""
        continue
    elif l.startswith("Mach") or \
            l.startswith("Blood") or \
            l.startswith("T"):
        assert current_region != ""
        current_type = l
        cells[current_region][current_type] = []
    elif l.startswith("Label"):
        continue
    else:
        assert current_region != ""
        assert current_type != ""
        if current_type in type_abr:
            cells[current_region][current_type].append(l + "," + type_abr[current_type])
        else:
            print(f"{current_region}, {current_type} not in the type dict")

# write csv
for region in cells:
    print(region, ":")
    for type in cells[region]:
        print(f"\t{type}: {len(cells[region][type])}")
    region_id = tryParseInt(region[6:])
    if region_id is None:
        print(f"Region name {region} fails to parse")
        break
    target_file_path = target_root_path + rf"\region_{region_id}\centroids.csv"
    csv_file = open(target_file_path, "w")
    csv_file.write(headline)
    for type in cells[region]:
        for line in cells[region][type]:
            csv_file.write(line + "\n")
    csv_file.close()
