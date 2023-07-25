import pandas as pd

cell_data = {
    'cell_id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'cell_type': ['T-Killer', 'T-Helper', 'T-Reg', 'CD68', 'vessel',
                  "T-Killer_link", 'T-Helper_link', 'T-Reg_link', 'CD68_link']
}
cell_sets_data = pd.DataFrame(cell_data)

cell_sets_data.to_csv('vccf_cell_sets.csv', index=False)
