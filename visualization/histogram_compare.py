import os
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from cell_defination import *
from violin_defination import *

postfix_list = ['', '_3d', '_s2d', '_2d']
for compare_postfix in [postfix_list[2], postfix_list[3]]:
    applied_postfix_list = [postfix_list[1], compare_postfix]
    data_list = []
    for postfix in applied_postfix_list:
        target_root_path = rf"G:\GE\skin_12_data{postfix}"

        file_paths = []

        for region_id in regions:
            target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
            file_paths.append(target_file_path)

        for index in range(len(regions)):
            file_path = file_paths[index]
            df = pd.read_csv(file_path, index_col=None, header=0)
            df['new_type'] = df['type'].astype(str) + postfix
            for _list, name in zip([regions, ages, genders],
                                   ["Region", "Age", "Gender"]):
                df[name] = [_list[index]] * len(df)
            data_list.append(df)

    n_data = pd.concat(data_list, axis=0, ignore_index=True)
    print(n_data)

    region_list = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 0]
    horizontal_spacing = 0.03
    title_list = []

    bin_size = 20
    bin_dict = dict(start=0, end=700, size=bin_size)

    sbin_size = 10
    sbin_dict = dict(start=0, end=5000, size=sbin_size)

    damage_type_list = ['P53', 'KI67', 'DDB2']
    all_cell_list = ['T-Helper', 'T-Reg', 'T-Killer', 'CD68', 'DDB2', 'KI67', 'P53', ]

    # for cell_list, distance_type, col in zip([['T-Helper', 'T-Reg', 'T-Killer', 'CD68'], ],
    #                                          ['vessel', ], [1, ]):

    for cell in all_cell_list:

        fig = make_subplots(
            rows=6, cols=4,
            column_widths=[1.0, 1.0, 1.0, 1.0],
            row_heights=[0.6, 0.2, 0.6, 0.2, 0.6, 0.2, ],
            specs=[
                [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, ],
                [{"type": "Scatter"}, {"type": "Scatter"}, {"type": "Scatter"}, {"type": "Scatter"}, ],
                [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, ],
                [{"type": "Scatter"}, {"type": "Scatter"}, {"type": "Scatter"}, {"type": "Scatter"}, ],
                [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, ],
                [{"type": "Scatter"}, {"type": "Scatter"}, {"type": "Scatter"}, {"type": "Scatter"}, ],
            ],
            horizontal_spacing=horizontal_spacing,
            vertical_spacing=0.02,
            shared_xaxes=True,
            subplot_titles=['Region 1', 'Region 2', 'Region 3', 'Region 4',
                            '', '', '', '',
                            'Region 5', 'Region 7', 'Region 8', 'Region 9',
                            '', '', '', '',
                            'Region 10', 'Region 11', 'Region 12', 'All Regions',
                            '', '', '', ''
                            ],
        )

        new_cell_list = []
        for postfix in applied_postfix_list:
            new_cell_list.append(cell + postfix)
        for i in range(len(region_list)):
            region = region_list[i]
            r_data = n_data[n_data['Region'] == region] if region > 0 else n_data
            distance_type = 'vessel' if cell not in damage_type_list else 'skin'
            col = i % 4 + 1
            row = i // 4 * 2 + 1
            print(cell, distance_type, row, col)
            hist_data = []
            hist_names = []
            threshold = 0
            for cell_type in new_cell_list:
                data = r_data[r_data['new_type'] == cell_type][f"{distance_type}_distance"]
                threshold_distance = data.quantile(.98)
                if threshold_distance > threshold:
                    threshold = threshold_distance
                print(cell_type, data.size)
                if data.size > 3:
                    hist_data.append(data)
                    hist_names.append(cell_type)
            if len(hist_names) == 0:
                continue

            # import plotly.express as px
            #
            # fig2 = px.histogram(x=hist_data, y=hist_names,
            #                     bin_size=bin_size if distance_type == 'vessel' else sbin_size,
            #                     histnorm='probability')
            fig2 = ff.create_distplot(hist_data, hist_names,
                                      bin_size=bin_size if distance_type == 'vessel' else sbin_size,
                                      curve_type='kde')

            max_range = 1
            r_data = r_data[r_data['skin_distance'] != 0]
            for i in range(len(hist_data)):
                hist = fig2['data'][i]
                # fig.add_trace(go.Histogram(x=fig2['data'][i]['x'],xbins=bin_dict,opacity=0.5,
                #                            marker_color=color_dict[hist_names[i]], showlegend=False,
                #                            ), row=2, col=col)
                fig.add_trace(go.Histogram(
                    x=r_data[(r_data['new_type'] == hist_names[i]) &
                             (r_data[f"{distance_type}_distance"] < threshold)][f"{distance_type}_distance"],
                    xbins=bin_dict if distance_type == 'vessel' else sbin_dict,
                    opacity=0.6,
                    marker=dict(color=cell_dict[hist_names[i].split('_')[1]]['color']),
                    showlegend=False,
                    name=cell_dict[hist_names[i].split('_')[1]]['legend']
                ), row=row, col=col)
                line = fig2['data'][len(hist_data) + i]
                line['y'] = line['y'] * len(hist_data[i])  * bin_size
                fig.add_trace(go.Scatter(line,
                                         line=dict(color=cell_dict[hist_names[i].split('_')[1]]['color'], width=2),
                                         showlegend=False,
                                         ), row=row, col=col)
                r_data[f'{hist_names[i]}_pos'] = 0.1 * (i + 1)
                fig.add_trace(go.Scatter(x=r_data[(r_data['new_type'] == hist_names[i]) &
                                                  (r_data[f"{distance_type}_distance"] < threshold)][
                    f"{distance_type}_distance"],
                                         y=r_data[f'{hist_names[i]}_pos'],
                                         mode='markers',
                                         opacity=0.6,
                                         marker=dict(color=cell_dict[hist_names[i].split('_')[1]]['color'],
                                                     symbol='line-ns-open'),
                                         showlegend=False,
                                         ), row=row + 1, col=col)

            # some manual adjustments on the rugplot
            fig.update_yaxes(range=[0, 0.1 * (len(hist_names) + 1)],
                             tickvals=[0.1 * (i + 1) for i in range(len(hist_names))], ticktext=hist_names,
                             row=row + 1, col=col)
            fig.update_xaxes(tickfont=dict(color='rgba(0,0,0,0)', size=1), row=row, col=col)
            fig.update_yaxes(rangemode='tozero', tickfont=dict(size=10), row=row + 1, col=col)
            fig.update_xaxes(rangemode='tozero', tickfont=dict(size=12), row=row + 1, col=col)
            fig.update_xaxes(ticklabelposition="inside", side="bottom", row=row + 1, col=col)
            fig.update_xaxes(range=[0, 1000], col=col)

            # for annotation in fig['layout']['annotations']:
            #     annotation['yanchor'] = 'bottom'
            #     annotation['y'] = 0.25
            #     annotation['yref'] = 'paper'
        fig.update_layout(
            title=f"Histogram Comparison ({cell}: {applied_postfix_list[0][1:]} vs {applied_postfix_list[1][1:]})", )
        fig.write_html(os.path.join(r'G:\GE', f"compare_{cell}{applied_postfix_list[0]}{applied_postfix_list[1]}.html"))

        fig.show()
