import csv
import os
import sys
import pandas as pd
from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool, CDSView, IndexFilter, ColumnDataSource
from bokeh.transform import factor_cmap


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


if __name__ == '__main__':
    tools_list = "pan," \
                 "box_select," \
                 "lasso_select," \
                 "box_zoom, " \
                 "wheel_zoom," \
                 "reset," \
                 "save," \
                 "help"
    # "hover," \

    input_id = '6b87d4f577d78de84819962e8bafeea8'
    if len(sys.argv) >= 2:
        input_id = sys.argv[1]
    output_root_path = rf'G:\kidney\slideseq-cell-type-annotated\slideseq-cell-type-annotated\{input_id}'
    nuclei_output_name = 'nuclei.csv'
    nuclei_file_path = os.path.join(output_root_path, nuclei_output_name)
    vessel_output_name = 'vessel.csv'
    vessel_file_path = os.path.join(output_root_path, vessel_output_name)

    output_file(os.path.join(output_root_path, f'{input_id}.html'))

    p = figure(match_aspect=True,
               plot_width=int(2000 * 1.075), plot_height=int(2000 * 1.075),
               tools=tools_list,
               # title='nuclei/vessel distance',
               )

    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.visible = False
    p.background_fill_alpha = 0.0
    p.outline_line_color = None

    v_headers, v_columns = read_csv(vessel_file_path)
    for i in range(0, len(v_headers)):
        v_columns[v_headers[i]] = [float(value) for value in v_columns[v_headers[i]]]

    data = dict()
    for header in v_headers:
        data[header] = v_columns[header]
    v_df = pd.DataFrame(data)

    # p.circle(x='x', y='y', source=v_df, color='#91672c', size=6, alpha=1)

    n_headers, n_columns = read_csv(nuclei_file_path)
    # for i in range(1, len(n_headers)):
    #    n_columns[n_headers[i]] = [float(value) for value in n_columns[n_headers[i]]]
    n_columns['y'] = [float(value) for value in n_columns['y']]
    n_columns['vy'] = [float(value) for value in n_columns['vy']]
    n_columns['x'] = [float(value) for value in n_columns['x']]
    n_columns['vx'] = [float(value) for value in n_columns['vx']]
    n_columns['alpha'] = [(float(value) + 500) / 1500 for value in n_columns['distance']]
    n_columns['color'] = ['#%02x%02x%02x' % (0, int(255 * float(value) / 1000), int(255 * (1000 - float(value)) / 1000))
                          for value in n_columns['distance']]

    cell_type_pool = [
        'Ascending Thin Limb to Thick Ascending Limb Cell',
        'Ascending Thin Limb Cell',
        'Proximal Tubule Cell',
        'Fibroblast',
        'Thick Ascending Limb Cell',
        'Macrophage',
        'Distal Convoluted Tubule Cell',
        'Myofibroblast',
        'Connecting Tubule',
        'Principal Cell',
        'Descending Thin Limb Cell',
        'placeholder_0',
        'Podocyte',
        'placeholder_1',
        'Endothelial Cell',
        'placeholder_2',
        'Vascular Smooth Muscle Cell and Pericyte'
        'placeholder_3',
        'Intercalated Alpha Cell',
        'Intercalated Beta Cell',
    ]

    data = dict()
    for header in n_headers:
        data[header] = n_columns[header]
    data['alpha'] = n_columns['alpha']
    data['color'] = n_columns['color']
    n_df = pd.DataFrame(data)

    cell_types = list(set(n_columns['type']))
    cell_types.sort()
    n_df = ColumnDataSource(data=n_df)
    for label in cell_types:
        index_list = []
        legend_label = ''
        for i in range(len(n_df.data['type'])):
            if n_df.data['type'][i] == label:
                index_list.append(i)
                legend_label = n_df.data['type'][i]
        view = CDSView(source=n_df, filters=[IndexFilter(index_list)])
        p.scatter(x='x', y='y', source=n_df, fill_alpha=0.8, size=6,
                  # marker=factor_mark('style_label', markers, roman_label),
                  marker='circle',
                  color=factor_cmap('type', 'Category20_20', cell_type_pool),
                  # muted_color=factor_cmap(label['real_label_list'], 'Category10_8',
                  #                         label['standard_label_list']),
                  muted_alpha=0.1, view=view,
                  legend_label=legend_label)
        p.segment(x0='x', y0='y', x1='vx', source=n_df, y1='vy',
                  # color="red",
                  color=factor_cmap('type', 'Category20_20', cell_type_pool),
                  alpha=0.2, line_width=1,
                  view=view,
                  legend_label=legend_label
                  )
    # p.circle(x='x', y='y', source=n_df, color='color', alpha=0.7, size=6)
    # g1_hover = HoverTool(renderers=[circle], tooltips=[('X', "@x"), ('Y', "@y"), ('distance', "@distance")])
    # p.add_tools(g1_hover)

    p.legend.location = "bottom_right"
    p.legend.click_policy = "mute"
    show(p)
