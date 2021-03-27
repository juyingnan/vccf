import anndata
import csv

input_id = '38e2af3a115f13e7d90d33c4e5ca4e9e'

h5ad_file_path = rf"G:\kidney\slideseq-cell-type-annotated\slideseq-cell-type-annotated\{input_id}\expr_labeled.h5ad"

d = anndata.read_h5ad(h5ad_file_path)

# print(d.obs)

# print(d.obsm)

# print(d.obsm['X_spatial'])


celltypes = d.obs["cell_type_predicted"]

print(set(celltypes))

x_list, y_list = [], []
for row in d.obsm['X_spatial']:
    x_list.append(row[0])
    y_list.append(row[1])

csv_file_path = h5ad_file_path.replace(".h5ad", ".csv")

assert len(celltypes) == len(x_list)

with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['ID', 'X', 'Y', 'cell_type']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(len(celltypes)):
        writer.writerow({'ID': i, 'X': x_list[i], 'Y': y_list[i], 'cell_type': celltypes[i]})
