import os
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
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

    threshold_distance = {
        'cell': n_data['vessel_distance'].quantile(.98),
        'damage': n_data['skin_distance'].quantile(.98)
    }

    cell_types = ['', 'CD68', 'T-Helper', 'T-Killer', 'T-Reg']
    damage_types = ['', 'P53', 'KI67', 'DDB2']

    for item in ['cell']:  # , 'damage']:
        cell_type_list = cell_types if item == 'cell' else damage_types
        cell_dict[''] = {}
        cell_dict['']['legend'] = 'All Cells' if item == 'cell' else 'All Damages'

        # display box and scatter plot along with violin plot
        # fig = pt.violin(n_data, y="distance", x="Age", color="Skin Type",
        #                 box=True, hover_data=n_data.columns,
        #                 points='all',
        #                 )
        subplot_titles = []
        for cell_type in cell_type_list:
            subplot_titles.append(cell_dict[cell_type]['legend'])

        row_heights_list = [1.0 / len(cell_type_list)] * len(cell_type_list)
        specs_list = [[{"secondary_y": False}], ]
        for i in range(len(cell_type_list) - 1):
            specs_list.append([{"secondary_y": True}])
        fig = make_subplots(
            rows=len(cell_type_list), cols=1,
            row_heights=row_heights_list,
            # specs=[[{"type": "Scatter3d", "colspan": 4}, None, None, None],
            #        [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}]],
            shared_xaxes=True,
            vertical_spacing=0.02,
            # subplot_titles=[f'All', 'CD68 / Macrophage', 'T-Helper', 'T-Regulatory'],
            subplot_titles=subplot_titles,
            specs=specs_list
        )

        # fig.add_trace(go.Violin(x=n_data['Region'][n_data['Skin Type'] == 'Sun-Exposed'],
        #                         y=n_data['distance'][n_data['Skin Type'] == 'Sun-Exposed'],
        #                         name='Sun-Exposed', legendgroup='Sun-Exposed',
        #                         line_color='orange', points="outliers",
        #                         box_visible=True, width=2,
        #                         meanline_visible=True))
        # fig.add_trace(go.Violin(x=n_data['Region'][n_data['Skin Type'] == 'Non-Sun-Exposed'],
        #                         y=n_data['distance'][n_data['Skin Type'] == 'Non-Sun-Exposed'],
        #                         name='Non-Sun-Exposed', legendgroup='Non-Sun-Exposed',
        #                         line_color='blue', points="outliers",
        #                         box_visible=True, width=2,
        #                         meanline_visible=True))

        # region_seq = [12, 5, 4, 2, 10, 7, 11, 3, 6, 8, 9, 1, ]
        # for index in range(len(regions)):
        #     next = region_seq[index] - 1
        #     fig.add_trace(go.Violin(x=n_data['Age'][n_data['Region'] == str(regions[next])],
        #                             y=n_data['distance'][n_data['Region'] == str(regions[next])],
        #                             name=suns[next], legendgroup=suns[next],
        #                             line_color=color_dict[suns[next]], points="outliers",
        #                             box_visible=True, width=1,
        #                             meanline_visible=True))
        # for skin_type in ['Sun-Exposed', 'Non-Sun-Exposed']:
        #     fig.add_trace(go.Violin(x=n_data['Age'][n_data['Skin Type'] == skin_type],
        #                             y=n_data['distance'][n_data['Skin Type'] == skin_type],
        #                             name=skin_type, legendgroup='All', legendgrouptitle_text="All",
        #                             points="outliers", opacity=opacity_dict[skin_type], width=4,
        #                             box_visible=True, line_color=color_dict[skin_type], meanline_visible=False),
        #                   secondary_y=False, row=1, col=1, )

        # fig.update_xaxes(range=[0, np.percentile(nuclei_vessel_distance_list, 99)], row=3, col=1)

        distance_type = 'vessel_distance' if item == 'cell' else 'skin_distance'
        for cell_type in cell_type_list:
            for postfix in applied_postfix_list:
                fig.add_trace(
                    go.Violin(
                        x=n_data['Age'][(n_data['new_type'].str.contains(cell_type + postfix)) &
                                        (n_data[distance_type] >= 0) &
                                        (n_data[distance_type] < threshold_distance[item])],
                        y=n_data[distance_type][
                            (n_data['new_type'].str.contains(cell_type + postfix)) &
                            (n_data[distance_type] >= 0) &
                            (n_data[distance_type] < threshold_distance[item])],
                        name=cell_type + postfix if cell_type != '' else 'All' + postfix,
                        points=False,  # jitter=0.05,
                        opacity=compare_opacity_dict[postfix], width=4,
                        legendgroup=cell_dict[cell_type]['legend'], scalegroup=cell_type, scalemode='width',
                        legendgrouptitle_text=cell_dict[cell_type]['legend'],
                        box_visible=True, box_fillcolor='white', line_width=1,
                        side='negative' if postfix == postfix_list[1] else 'positive',
                        line_color=color_dict[f'{cell_type}-{sun_type["S"]}'], meanline_visible=False),
                    secondary_y=False, row=cell_type_list.index(cell_type) + 1, col=1)

            # if cell_type != '':
            #     line_ages = [age for age in ages if suns[ages.index(age)] == skin_type]
            #     line_ages.sort()
            #     fig.add_trace(
            #         go.Scatter(x=line_ages,
            #                    # y=[percentage_dict[cell_type][ages.index(age)] * 100 for age in line_ages],
            #                    y=[len(n_data[(n_data['type'].str.contains(cell_type)) & (n_data['Age'] == age)])
            #                       / len(n_data[n_data['Age'] == age])
            #                       * 100 for age in line_ages],
            #                    mode='lines+markers', marker_symbol='cross',
            #                    name=skin_type + " percentage", legendgroup=cell_type_dict[cell_type],
            #                    line=dict(color=color_dict[f'{cell_type}-{skin_type}'], width=1), ),
            #         secondary_y=True, row=cell_type_list.index(cell_type) + 1, col=1)

        # fig.update_traces(meanline_visible=True,
        #                   scalemode='width')  # scale violin plot area with total count

        annotations = go.Scatter(
            x=ages,
            y=[700, 700, 700, 700, 700, 700, 700, 700, 700, 700, 700]
            if item == 'cell' else [4000, 4000, 4000, 3700, 4000, 4000, 4000, 4000, 3700, 4000],
            marker={
                "color": "LightBlue",
                "line": {
                    "width": 0,
                },
                "size": 22
            },
            mode="markers+text",
            opacity=0.7,
            name='Region #',
            text=[f"{x}" for x in regions], showlegend=True,
            textfont={
                "color": ["black" if sun == sun_type['S'] else "white" for sun in suns], }
        )
        fig.add_trace(annotations, row=1, col=1)

        title_dict = {
            'cell': {
                'main_subtitle': "from Cells to Endothelial Cells",
                'yaxis': "to Endothelial Cells",
            },
            'damage': {
                'main_subtitle': "from Damages to Skin Surface",
                'yaxis': "to Skin Surface",
            },
        }
        main_subtitle = f'<br><sup>Nearest Distance {title_dict[item]["main_subtitle"]}</sup>'
        fig.update_layout(
            title=f'Vascular Common Coordinate Framework Violin Chart '
                  f'[{applied_postfix_list[0][1:]} vs {applied_postfix_list[1][1:]}] {main_subtitle}',
            font=dict(
                family="Arial, Bahnschrift",
                size=14,
                # color="RebeccaPurple"
            ),
            # x1axis_title="Age",
            # y4axis_title="Nearest Distance",
            violingap=0.3, violingroupgap=0,
            violinmode='overlay',
            yaxis_zeroline=False)
        fig.update_xaxes(title_text="Age", row=5, col=1)
        fig.update_yaxes(title_text=f"Nearest Distance {title_dict[item]['yaxis']}", row=3, col=1)
        fig.update_yaxes(title_text="Percentage", row=2, col=1, secondary_y=True)
        fig.update_yaxes(range=[-49, 800] if item == 'cell' else [-999, 4300])

        # subtitle location
        vertical_offset = 0.02
        for annotation in fig['layout']['annotations']:
            annotation['xanchor'] = "center"
            annotation['y'] -= vertical_offset
            annotation['font'] = dict(
                family="Arial, Bahnschrift",
                size=16, )

        fig.write_html(os.path.join(r'G:\GE', f"compare_violin{applied_postfix_list[0]}{applied_postfix_list[1]}.html"))
        fig.show()
