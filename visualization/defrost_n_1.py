# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output, no_update, State
from dash.dependencies import Input, Output
import math
import os
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from cell_defination import *
from violin_defination import *
import csv


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        _headers = next(reader, None)

        # get column
        _columns = {}
        for _h in _headers:
            _columns[_h] = []
        for row in reader:
            for _h, _v in zip(_headers, row):
                _columns[_h].append(_v)

        return _headers, _columns


def generate_one_line_df(df, key):
    line_x = [None] * (len(df) * 2)
    line_y = [None] * (len(df) * 2)
    line_z = [None] * (len(df) * 2)
    line_x[::2] = df[f"n{key}x"]
    line_y[::2] = df[f"n{key}y"]
    line_z[::2] = df[f"n{key}z"]
    line_x[1::2] = df["nx"]
    line_y[1::2] = df["ny"]
    line_z[1::2] = df["nz"]

    l_data = dict()
    l_data["x"] = line_x
    l_data["y"] = line_y
    l_data["z"] = line_z
    # v_color = ['red'] * len(vessel_x_list)
    # v_data["color"] = v_color
    l_df = pd.DataFrame(l_data)
    l_gap = (l_df.iloc[1::2]
             .assign(x=np.nan, y=np.nan)
             .rename(lambda x: x + .5))
    l_df_one = pd.concat([l_df, l_gap], sort=False).sort_index().reset_index(drop=True)
    l_df_one.loc[l_df_one.isnull().any(axis=1), :] = np.nan
    return l_df_one


def generate_nuclei_scatter(df, ct, visible=True, show_legend=True, legend_group=""):
    return go.Scatter3d(x=df[df['type'] == ct]["nx"],
                        y=df[df['type'] == ct]["ny"],
                        z=df[df['type'] == ct]["nz"],
                        mode="markers",
                        name=cell_dict[cell_type]['legend'],
                        showlegend=show_legend,
                        legendgroup=legend_group,
                        legendgrouptitle_text=legend_group,
                        marker=dict(
                            size=df[df['type'] == ct]["size"],
                            color=df[df['type'] == ct]["color"],
                            symbol=cell_dict[ct]['marker'],
                            opacity=0.75,
                            line=dict(
                                color=df[df['type'] == ct]["color"],
                                width=0
                            )),
                        hovertemplate=
                        '<i>X</i>: %{x:.2f}<br>' +
                        '<i>Y</i>: %{y:.2f}<br>' +
                        '<i>Z</i>: %{z:.2f}<br>' +
                        '<b><i>Distance</i>: %{text}</b>',
                        text=df[df['type'] == ct]["vessel_distance"],
                        visible=visible)


def generate_other_scatter(df, key, name, symbol_name, visible=True, show_legend=True, legend_group=""):
    return go.Scatter3d(x=df[f"{key}x"], y=df[f"{key}y"], z=df[f"{key}z"],
                        mode="markers",
                        name=name,
                        showlegend=show_legend,
                        legendgroup=legend_group,
                        legendgrouptitle_text=legend_group,
                        marker=dict(
                            size=df["size"],
                            color=df["color"],
                            symbol=cell_dict[symbol_name]['marker'],
                            opacity=0.5,
                            line=dict(
                                color=df["color"],
                                width=0)),
                        visible=visible)


def generate_line(df, name, color, visible=True, opacity=0.5, width=1, show_legend=True, legend_group=""):
    return go.Scatter3d(x=df["x"],
                        y=df["y"],
                        z=df["z"],
                        mode="lines",
                        name=name,
                        opacity=opacity,
                        showlegend=False,  # show_legend
                        legendgroup=legend_group,
                        legendgrouptitle_text=legend_group,
                        line=dict(
                            color=color,
                            width=width, ),
                        visible=visible)


app = Dash(__name__)

# vis
z_list = [77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101]
micro_per_pixel = 0.325
scale = 16 * micro_per_pixel

top_left = [0, 0]
bottom_right = [1000000, 1000000]

root_path = r'G:\GE\skin_12_data\temp/'

n_headers, n_columns = read_csv(root_path + 'nuclei.csv')
for i in range(len(n_columns)):  # len(n_headers)):
    n_columns[n_headers[i]] = [value for value in n_columns[n_headers[i]]]
nuclei_id_list = [int(value) for value in n_columns['id']]
nuclei_x_list = [float(value) for value in n_columns['x']]
nuclei_y_list = [float(value) for value in n_columns['y']]
nuclei_z_list = [float(value) for value in n_columns['z']]
nuclei_type_list = n_columns['type']
nuclei_vessel_distance_list = [float(value) for value in n_columns['vessel_distance']]
nuclei_nearest_vessel_x_list = [float(value) for value in n_columns['vx']]
nuclei_nearest_vessel_y_list = [float(value) for value in n_columns['vy']]
nuclei_nearest_vessel_z_list = [float(value) for value in n_columns['vz']]
nuclei_skin_distance_list = [float(value) for value in n_columns['skin_distance']]
nuclei_nearest_skin_x_list = [float(value) for value in n_columns['sx']]
nuclei_nearest_skin_y_list = [float(value) for value in n_columns['sx']]
nuclei_nearest_skin_z_list = [float(value) for value in n_columns['sx']]

n_headers, n_columns = read_csv(root_path + 'vessel.csv')
for i in range(len(n_columns)):  # len(n_headers)):
    n_columns[n_headers[i]] = [value for value in n_columns[n_headers[i]]]
vessel_x_list = [float(value) for value in n_columns['x']]
vessel_y_list = [float(value) for value in n_columns['y']]
vessel_z_list = [float(value) for value in n_columns['z']]

n_headers, n_columns = read_csv(root_path + 'skin.csv')
for i in range(len(n_columns)):  # len(n_headers)):
    n_columns[n_headers[i]] = [value for value in n_columns[n_headers[i]]]
skin_x_list = [float(value) for value in n_columns['x']]
skin_y_list = [float(value) for value in n_columns['y']]
skin_z_list = [float(value) for value in n_columns['z']]

n_color = [cell_dict[cell_type]['color'] for cell_type in nuclei_type_list]
v_color = [cell_dict['CD31']['color']] * len(vessel_x_list)
s_color = [cell_dict['Skin']['color']] * len(skin_x_list)

n_size = [cell_dict[cell_type]['size'] / 2 for cell_type in nuclei_type_list]
v_size = [cell_dict['CD31']['size'] / 2] * len(vessel_x_list)
s_size = [cell_dict['Skin']['size'] / 2] * len(skin_x_list)

n_data = dict()
n_data["nx"] = nuclei_x_list
n_data["ny"] = nuclei_y_list
n_data["nz"] = nuclei_z_list
n_data["nvx"] = nuclei_nearest_vessel_x_list
n_data["nvy"] = nuclei_nearest_vessel_y_list
n_data["nvz"] = nuclei_nearest_vessel_z_list
n_data["nsx"] = nuclei_nearest_skin_x_list
n_data["nsy"] = nuclei_nearest_skin_y_list
n_data["nsz"] = nuclei_nearest_skin_z_list
n_data["size"] = n_size
n_data["type"] = nuclei_type_list
n_data["vessel_distance"] = nuclei_vessel_distance_list
n_data["skin_distance"] = nuclei_skin_distance_list
n_data["color"] = n_color

n_df = pd.DataFrame(n_data)
# print(n_df)

v_data = dict()
v_data["vx"] = vessel_x_list
v_data["vy"] = vessel_y_list
v_data["vz"] = vessel_z_list
v_data["color"] = v_color
v_data["size"] = v_size
v_df = pd.DataFrame(v_data)
# print(v_df)

s_data = dict()
s_data["sx"] = skin_x_list
s_data["sy"] = skin_y_list
s_data["sz"] = skin_z_list
s_data["color"] = s_color
s_data["size"] = s_size
s_df = pd.DataFrame(s_data)
skin_display_rate = 1
s_df = s_df[s_df.index % skin_display_rate == 0]
# print(s_df)
# print(f"Displayed skin size: {len(s_df)}")

# blood vessel distance
vd_df = n_df[n_df['vessel_distance'] >= 0]
v_df_one = generate_one_line_df(vd_df, key='v')
# print(v_df_one)

# skin surface distance
sd_df = n_df[n_df['skin_distance'] >= 0]
s_df_one = generate_one_line_df(sd_df, key='s')
# print(s_df_one)

traces_n = []
for cell_type in set(nuclei_type_list):
    traces_n.append(generate_nuclei_scatter(n_df, cell_type,
                                            legend_group=cell_dict[cell_type]['group']))
trace_v = generate_other_scatter(v_df, key='v', name=cell_dict['CD31']['legend'], symbol_name='CD31', visible=True,
                                 legend_group="Endothelial & Skin")
trace_s = generate_other_scatter(s_df, key='s', name=cell_dict['Skin']['legend'], symbol_name='Skin', visible=True,
                                 legend_group="Endothelial & Skin")
traces_vessel_line = generate_line(v_df_one, name=f"Distance-{cell_dict['CD31']['legend']}",
                                   color=cell_dict['CD31']['color'], visible=True, legend_group="Link")
traces_skin_line = generate_line(s_df_one, name=f"Distance-{cell_dict['Skin']['legend']}",
                                 color=cell_dict['Skin']['color'], visible='legendonly', legend_group="Link")
traces_n.extend([trace_v, trace_s, traces_vessel_line, traces_skin_line])
main_fig_count = len(traces_n)

# violin
cell_types = ['', 'CD68', 'T-Helper', 'T-Killer', 'T-Reg']
damage_types = ['', 'P53', 'KI67', 'DDB2']
cell_type_list = cell_types
cell_dict[''] = {}
cell_dict['']['legend'] = 'All Cells'

subplot_titles = []
for cell_type in cell_type_list:
    subplot_titles.append(cell_dict[cell_type]['legend'])

image_hyperlink = f'https://raw.githubusercontent.com/hubmapconsortium/vccf-visualization-release/main/vheimages/S002_VHE_region_03.jpg'
main_subtitle = f'<br><sup>Region 3 <a href="{image_hyperlink}">Virtual H&E Image Preview</a></sup>'
hist_subtitle = '<br><sup>Histogram</sup>'
horizontal_spacing = 0.03
subfigs = make_subplots(
    rows=5, cols=2,
    column_widths=[0.6, 0.4],
    row_heights=[0.2, 0.2, 0.2, 0.2, 0.2],
    specs=[
        [{"type": "Scatter3d", "colspan": 1, 'rowspan': 3}, {"secondary_y": False}, ],
        [None, {"secondary_y": True}],
        [None, {"secondary_y": True}],
        [{"type": "Histogram"}, {"secondary_y": True}],  # {"type": "Histogram"}
        [{"type": "Scatter"}, {"secondary_y": True}],  # {"type": "Scatter"}
    ],
    horizontal_spacing=horizontal_spacing, vertical_spacing=0.02, shared_xaxes=True,
    subplot_titles=[f'Vascular Common Coordinate Framework 3D Visualization {main_subtitle}',
                    subplot_titles[0],
                    subplot_titles[1],
                    subplot_titles[2],
                    f'Distance to Endothelial Cells{hist_subtitle}',
                    subplot_titles[3],
                    None,
                    subplot_titles[4],
                    ],
)
fig = subfigs
for trace_n in traces_n:
    fig.add_trace(trace_n, 1, 1)

bin_size = 3
bin_dict = dict(start=0, end=200, size=bin_size)

sbin_size = 10
sbin_dict = dict(start=0, end=5000, size=sbin_size)

for cell_list, distance_type, col in zip([['T-Helper', 'T-Reg', 'T-Killer', 'CD68'], ],
                                         ['vessel', ], [1, ]):
    # print(cell_list, distance_type, col)
    hist_data = []
    hist_names = []
    for cell_type in cell_list:
        data = n_df[n_df['type'] == cell_type][f"{distance_type}_distance"]
        # print(cell_type, data.size)
        if data.size > 5:
            hist_data.append(data)
            hist_names.append(cell_type)

    fig2 = ff.create_distplot(hist_data, hist_names, bin_size=bin_size if distance_type == 'vessel' else sbin_size,
                              histnorm='probability')  # , curve_type='normal')

    max_range = 1
    n_df = n_df[n_df['skin_distance'] != 0]
    for i in range(len(hist_data)):
        hist = fig2['data'][i]
        # fig.add_trace(go.Histogram(x=fig2['data'][i]['x'],xbins=bin_dict,opacity=0.5,
        #                            marker_color=color_dict[hist_names[i]], showlegend=False,
        #                            ), row=4, col=col)
        fig.add_trace(go.Histogram(
            x=n_df[n_df['type'] == hist_names[i]][f"{distance_type}_distance"],
            xbins=bin_dict if distance_type == 'vessel' else sbin_dict,
            opacity=0.6,
            marker=dict(color=cell_dict[hist_names[i]]['color']),
            showlegend=False,
            # name=cell_dict[hist_names[i]]['legend']
        ), row=4, col=col)
        line = fig2['data'][len(hist_data) + i]
        line['y'] = line['y'] * len(hist_data[i])  # * bin_size *
        if not any(y > 1e5 for y in line['y']):
            fig.add_trace(go.Scatter(line,
                                     line=dict(color=cell_dict[hist_names[i]]['color'], width=2), showlegend=False,
                                     ), row=4, col=col)
        n_df[f'{hist_names[i]}_pos'] = 0.1 * (i + 1)
        fig.add_trace(go.Scatter(x=n_df[n_df['type'] == hist_names[i]][f"{distance_type}_distance"],
                                 y=n_df[f'{hist_names[i]}_pos'],
                                 mode='markers',
                                 name=cell_dict[hist_names[i]]['legend'],
                                 opacity=0.6,
                                 marker=dict(color=cell_dict[hist_names[i]]['color'], symbol='line-ns-open',
                                             size=[8] * len(
                                                 n_df[n_df['type'] == hist_names[i]][f"{distance_type}_distance"])),
                                 showlegend=False,
                                 ), row=5, col=col)

    # some manual adjustments on the rugplot
    fig.update_yaxes(range=[0, 0.1 * (len(hist_names) + 1)],
                     tickvals=[0.1 * (i + 1) for i in range(len(hist_names))], ticktext=hist_names,
                     row=5, col=col)
    fig.update_xaxes(tickfont=dict(color='rgba(0,0,0,0)', size=1), row=4, col=col)

sub_title_text = "[Glomerulus-level (~2000 matching gloms) \n/ Crypt-level (~160 matching crypts)]"
title_text = f"Kidney/Colon - dice/recall/precision <br><sup>{sub_title_text}</sup>"

# Invisble scale for keep space instant

x_min, x_max = min(nuclei_x_list), max(nuclei_x_list)
y_min, y_max = min(nuclei_y_list), max(nuclei_y_list)
z_min, z_max = min(nuclei_z_list), max(nuclei_z_list)
margin_index = 0.05
x_margin = (x_max - x_min) * margin_index
y_margin = (y_max - y_min) * margin_index
z_margin = (z_max - z_min) * margin_index * 2

invisible_scale = go.Scatter3d(
    name="",
    visible=True,
    showlegend=False,
    opacity=0,
    hoverinfo='none',
    x=[x_min - x_margin, x_max + x_margin],
    y=[y_min - y_margin, y_max + y_margin],
    z=[z_min - z_margin, z_max + z_margin],
)
fig.add_trace(invisible_scale)

# Add dropdown
histogram_layout_buttons = list([
    dict(
        args=["barmode", "overlay"],
        label="Overlaid",
        method="relayout"
    ),
    dict(
        args=["barmode", "relative"],
        label="Stacked",
        method="relayout"
    ),
    dict(
        args=["barmode", "group"],
        label="Grouped",
        method="relayout"
    )
])

# layout update
for annotation in fig['layout']['annotations'][:1]:
    annotation['x'] = 0
    annotation['xanchor'] = "left"
    annotation['y'] = 1
    annotation['yanchor'] = "top"
    annotation['font'] = dict(
        family="Arial, Bahnschrift",
        size=24, )
for annotation in fig['layout']['annotations'][4:5]:
    annotation['x'] = 0.4
    annotation['xanchor'] = "left"
    annotation['y'] = 0.3
    annotation['font'] = dict(
        family="Arial, Bahnschrift",
        size=16, )

background_color = 'rgb(240,246,255)'

# fig.add_annotation(dict(text="Slide:", showarrow=False,
#                         x=1, y=0.88, xref="paper", yref="paper", xanchor='right', yanchor='top', ))
fig.update_yaxes(rangemode='tozero', tickfont=dict(size=12), row=4, col=1)
fig.update_yaxes(rangemode='tozero', tickfont=dict(size=10), row=5, col=1)
fig.update_xaxes(rangemode='tozero', tickfont=dict(size=12), row=4, col=1)
fig.update_xaxes(rangemode='tozero', tickfont=dict(size=12), row=5, col=1)
fig.update_xaxes(ticklabelposition="outside", side="bottom",
                 title=dict(text="Distance (μm)", standoff=5, font_size=14), row=5, col=1)
# fig.update_xaxes(range=[0, np.percentile(nuclei_vessel_distance_list, 99)], row=5, col=1)
fig.update_xaxes(range=[0, 210], row=5, col=1)
# fig.update_xaxes(range=[0, np.percentile(nuclei_skin_distance_list, 98)], row=5, col=2)
# fig.update_yaxes(ticklabelposition="inside", side="right", row=5, )
fig.update_yaxes(ticklabelposition="outside", side="left",
                 title=dict(text="Count #", standoff=5, font_size=14), row=4, col=1)
fig.update_traces(connectgaps=False, selector=dict(type="Scatter3d"))

# violin

n_data = pd.read_csv(root_path + 'violin.csv')

threshold_distance = {
    'cell': n_data['vessel_distance'].quantile(.98),
    'damage': n_data['skin_distance'].quantile(.98)
}

fig.update_layout(
    updatemenus=[
        dict(
            buttons=histogram_layout_buttons,
            direction="right",
            pad={"r": 0, "t": 5},
            showactive=True,
            x=0,
            xanchor="left",
            y=-0.06,
            yanchor="bottom"
        ),

        # dict(
        #     buttons=layer_select_buttons,
        #     direction="down",
        #     pad={"r": 0, "t": 5},
        #     showactive=True,
        #     x=1,
        #     xanchor="right",
        #     y=0.85,
        #     yanchor="top"
        # ),
    ],
    font=dict(
        family="Arial, Bahnschrift",
        size=14,
        # color="RebeccaPurple"
    ),
    margin=dict(
        l=5,
        r=5,
        b=5,
        t=5,
        pad=0
    ),
    legend=dict(
        groupclick="toggleitem",
        yanchor="top",
        y=0.95,
        xanchor="left",
        x=0.45
    ),
    barmode='overlay',
    scene=dict(
        aspectmode='data',
        xaxis=dict(nticks=10, backgroundcolor=background_color, ),
        yaxis=dict(nticks=10, backgroundcolor=background_color, ),
        zaxis=dict(nticks=5, backgroundcolor=background_color, ),
    ),
    plot_bgcolor=background_color,
)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

item = 'cell'
distance_type = 'vessel_distance' if item == 'cell' else 'skin_distance'
for cell_type in cell_type_list:
    fig.add_trace(
        go.Violin(
            x=n_data['Age'][(n_data['Age'] != 38) &
                            (n_data['type'].str.contains(cell_type)) &
                            (n_data[distance_type] >= 0) &
                            (n_data[distance_type] < threshold_distance[item])],
            y=n_data[distance_type][(n_data['Age'] != 38) &
                                    (n_data['type'].str.contains(cell_type)) &
                                    (n_data[distance_type] >= 0) &
                                    (n_data[distance_type] < threshold_distance[item])],
            # name=cell_dict[cell_type]['legend'],
            points=False,  # jitter=0.05,
            showlegend=False,
            opacity=0.5, width=4,
            legendgroup=cell_dict[cell_type]['legend'], scalegroup='cell_type', scalemode='width',
            legendgrouptitle_text=cell_dict[cell_type]['legend'],
            box_visible=True, box_fillcolor='white', line_width=1,
            line_color=color_dict[f'{cell_type}-{sun_type["N"]}'], meanline_visible=False),
        secondary_y=False, row=cell_type_list.index(cell_type) + 1, col=2)
    fig.add_trace(
        go.Violin(
            x=n_data['Age'][(n_data['Age'] == 38) &
                            (n_data['type'].str.contains(cell_type)) &
                            (n_data[distance_type] >= 0) &
                            (n_data[distance_type] < threshold_distance[item])],
            y=n_data[distance_type][(n_data['Age'] == 38) &
                                    (n_data['type'].str.contains(cell_type)) &
                                    (n_data[distance_type] >= 0) &
                                    (n_data[distance_type] < threshold_distance[item])],
            name=cell_dict[cell_type]['legend'],
            points=False,  # jitter=0.05,
            showlegend=False,
            opacity=0.5, width=4,
            legendgroup=cell_dict[cell_type]['legend'], scalegroup='cell_type', scalemode='width',
            legendgrouptitle_text=cell_dict[cell_type]['legend'],
            box_visible=True, box_fillcolor='white', line_width=1,
            line_color=color_dict[f'{cell_type}-{sun_type["N"]}'], meanline_visible=False),
        secondary_y=False, row=cell_type_list.index(cell_type) + 1, col=2)

annotations = go.Scatter(
    x=ages,
    y=[220, 220, 200, 220, 220, 220, 220, 220, 220, 200, 220],
    marker={
        "color": "LightBlue",
        "line": {
            "width": 0,
        },
        "size": 22
    },
    mode="markers+text",
    opacity=0.9,
    name='Region #',
    text=[f"{x}" for x in regions], showlegend=False,
    textfont={
        "color": ["black" if sun == sun_type['S'] else "black" for sun in suns], }
)
fig.add_trace(annotations, row=1, col=2)
fig.update_layout(
    violingap=0.3, violingroupgap=0,
    violinmode='overlay',
    yaxis_zeroline=False)

fig.update_xaxes(title_text="Age", row=5, col=2)
fig.update_yaxes(title_text=f"Nearest Distance to Endothelial Cells (Percentage)", row=3, col=2, secondary_y=False)
fig.update_yaxes(range=[-49, 249] if item == 'cell' else [-999, 4300], col=2)
vertical_offset = 0.03
horizontal_offset = 0.18
sub_title_index_list = [1, 2, 3, 5, 6]
for i in sub_title_index_list:
    annotation = fig['layout']['annotations'][i]
    annotation['xanchor'] = "left"
    annotation['y'] -= vertical_offset
    annotation['x'] -= horizontal_offset
    annotation['font'] = dict(
        family="Arial, Bahnschrift",
        size=14, )

# viz end

app.layout = html.Div(children=[
    # html.H1(children='Hello Dash22'),
    #
    # html.Div(children='''
    #     Dash: A web application framework for your data.
    # '''),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        style={'width': '180vh', 'height': '90vh'}
    ),
    dcc.Tooltip(id="graph-tooltip"),
])

size_list = {
    'CD68': fig.data[4]['marker']['size'],
    't-helper': fig.data[5]['marker']['size'],
    't-killer': fig.data[3]['marker']['size'],
    't-reg': fig.data[6]['marker']['size'],
}

for i in range(len(fig.data)):
    print(i, fig.data[i]['name'])

curve_filter = [cell_dict[cell_type]['legend'] for cell_type in cell_type_list]


@app.callback(
    Output("example-graph", "figure"),
    Input('example-graph', 'clickData'),
)
def display_hover(clickData):
    if clickData is not None:
        pt = clickData["points"][0]
        bbox = pt["bbox"]
        num = pt["pointNumber"]
        curve = pt["curveNumber"]
        current_size = pt["marker.size"]
        if fig.data[curve]['name'] in curve_filter and curve < 23:
            clicked_type = fig.data[curve]['name']
            for plot in fig.data[:23]:
                if plot['name'] == clicked_type:
                    if current_size < 30:
                        default_size = list(plot['marker']['size'][:])
                        default_size[num] = 30
                        plot['marker']['size'] = default_size
                        print(f"click curve {curve}, changed curve {plot['name']}")
                    else:
                        default_size = list(plot['marker']['size'][:])
                        default_size[num] = 8
                        plot['marker']['size'] = default_size
                        print(f"click curve {curve}, restored curve {plot['name']}")
            for plot in fig.data[23:]:
                if plot['name'] == clicked_type:
                    plot['opacity'] = 1
                    print(f"click curve {curve}, changed violin opacity")
            fig.update_layout()
    # if curve in curve_dict:

    print(clickData)
    return fig

    # children = [
    #     html.Div([
    #         html.H2(f"test", style={"color": "darkblue", "overflow-wrap": "break-word"}),
    #     ], style={'width': '200px', 'white-space': 'normal'})
    # ]
    # return True, bbox, children


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
