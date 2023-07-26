import pandas as pd

cell_data = {
    'cell_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'cell_type': ['T-Killer', 'T-Helper', 'T-Reg', 'CD68', 'vessel',
                  "T-Killer_link", 'T-Helper_link', 'T-Reg_link', 'CD68_link',
                  'DDB2', 'P53', 'KI67', 'skin'],
}
cell_sets_data = pd.DataFrame(cell_data)

cell_sets_data.to_csv('cell_sets.csv', index=False)
