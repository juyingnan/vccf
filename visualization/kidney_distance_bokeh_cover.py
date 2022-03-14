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

    # input_id = 'Region7'
    # image_size = [14906, 9416]
    input_id = 'Region11'
    image_size = [20439, 9418]
    if len(sys.argv) >= 2:
        input_id = sys.argv[1]
    output_root_path = rf'C:\Users\bunny\Desktop\ForYingnan\{input_id}\Slide78'
    nuclei_output_name = 'nuclei.csv'
    nuclei_file_path = os.path.join(output_root_path, nuclei_output_name)
    vessel_output_name = 'vessel.csv'
    vessel_file_path = os.path.join(output_root_path, vessel_output_name)

    output_file(os.path.join(output_root_path, f'{input_id}.html'))

    index = 1
    p = figure(match_aspect=True,
               plot_width=int(4189 * index), plot_height=int(2352 * index),
               tools=tools_list, output_backend="svg",
               # title='nuclei/vessel distance',
               )

    p.background_fill_color = None
    p.border_fill_color = None

    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.visible = False
    p.background_fill_alpha = 0.0
    p.outline_line_color = None

    # v_headers, v_columns = read_csv(vessel_file_path)
    # for i in range(0, len(v_headers)):
    #     v_columns[v_headers[i]] = [float(value) for value in v_columns[v_headers[i]]]
    #
    # data = dict()
    # for header in v_headers:
    #     data[header] = v_columns[header]
    # v_df = pd.DataFrame(data)

    color_dict = {
        'CD68': "red",
        'Macrophage': "red",
        'CD31': "cyan",
        'Blood Vessel': "cyan",
        'T-Helper': "yellow",
        'T-Reg': "white",
        'T-Regulatory': "white",
        'T-Regulator': "white",
        'T-Killer': "lime",
        'P53': "chocolate",
        'KI67': "grey",
        'DDB2': "olivedrab",
        'Skin': "darkgrey",
        "CD4": "yellow",
        "CD3": "green",
        "CD8": "lime",
        "FOXP3": "white",
        "placeholder": "red",
    }

    # color_dict = {
    #     'CD68': "gold",
    #     'Macrophage': "gold",
    #     'CD31': "red",
    #     'Blood Vessel': "red",
    #     'T-Helper': "blue",
    #     'T-Reg': "mediumspringgreen",
    #     'T-Regulatory': "mediumspringgreen",
    #     'T-Regulator': "mediumspringgreen",
    #     'T-Killer': "purple",
    #     'P53': "chocolate",
    #     'KI67': "cyan",
    #     'DDB2': "olivedrab",
    #     'Skin': "darkgrey",
    #     "CD4": "blue",
    #     "CD8": "purple",
    #     "FOXP3": "mediumspringgreen",
    #     "placeholder": "red",
    # }

    n_headers, n_columns = read_csv(nuclei_file_path)
    n_columns['y'] = [float(value) for value in n_columns['y']]
    n_columns['vy'] = [float(value) for value in n_columns['vy']]
    n_columns['x'] = [float(value) for value in n_columns['x']]
    n_columns['vx'] = [float(value) for value in n_columns['vx']]
    n_columns['alpha'] = [0.5] * len(n_columns['y'])
    n_columns['color'] = [color_dict[type] for type in n_columns['type']]
    n_columns['nuclei'] = [False if type in ['P53', 'KI67', 'DDB2'] else True for type in n_columns['type']]

    n_columns['id'].append(len(n_columns['y']))
    n_columns['y'].append(0)
    n_columns['x'].append(0)
    n_columns['vy'].append(0)
    n_columns['vx'].append(0)
    n_columns['distance'].append(0)
    n_columns['type'].append("placeholder")
    n_columns['alpha'].append(0.5)
    n_columns['color'].append(color_dict["placeholder"])
    n_columns['nuclei'].append(False)

    n_columns['id'].append(len(n_columns['y']))
    n_columns['y'].append(image_size[0])
    n_columns['x'].append(image_size[1])
    n_columns['vy'].append(image_size[0])
    n_columns['vx'].append(image_size[1])
    n_columns['distance'].append(0)
    n_columns['type'].append("placeholder")
    n_columns['alpha'].append(0.5)
    n_columns['color'].append(color_dict["placeholder"])
    n_columns['nuclei'].append(False)

    data = dict()
    for header in n_headers:
        data[header] = n_columns[header]
        data['alpha'] = n_columns['alpha']
        data['color'] = n_columns['color']
        data['nuclei'] = n_columns['nuclei']
    n_df = pd.DataFrame(data)

    v_headers, v_columns = read_csv(vessel_file_path)
    for i in range(0, len(v_headers)):
        v_columns[v_headers[i]] = [float(value) for value in v_columns[v_headers[i]]]

    data = dict()
    for header in v_headers:
        data[header] = v_columns[header]
    v_df = pd.DataFrame(data)

    # p.segment(x0='x', y0='y', x1='vx', source=n_df, y1='vy', color="ivory", alpha=0.4, line_width=1)
    circle = p.circle(x='y', y='x', source=n_df[n_df['nuclei'] == True], color='color', alpha=0.5, size=5,
                      line_width=1)
    cross = p.cross(x='y', y='x', source=n_df[n_df['nuclei'] == False], color='color', alpha=0.5, size=6,
                    line_width=2)
    p.segment(x0='y', y0='x', x1='vy', y1='vx', source=n_df[n_df['nuclei'] == True],
              color="white",
              alpha=0.4, line_width=1,
              )
    p.scatter(x='vy', y='vx', source=v_df, fill_alpha=0.1, size=0.2,
              # marker=factor_mark('style_label', markers, roman_label),
              marker='circle',
              color=color_dict['CD31'], )
    g1_hover = HoverTool(renderers=[circle], tooltips=[('X', "@x"), ('Y', "@y"), ('distance', "@distance")])
    p.add_tools(g1_hover)

    show(p)
