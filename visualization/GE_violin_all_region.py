import os
import plotly.graph_objects as go
import pandas as pd
from cell_defination import *
from violin_defination import *
from plotly.subplots import make_subplots

target_root_path = r"G:\GE\skin_12_data"

file_paths = []

place_holders = ["All"] * len(regions)

point_position_dict = {sun_type["S"]: 1.0,
                       sun_type["N"]: -1.0,
                       f'-{sun_type["S"]}': 1.0,
                       f'-{sun_type["N"]}': -1.0,
                       f'CD68-{sun_type["S"]}': 0.9,
                       f'CD68-{sun_type["N"]}': -0.9,
                       f'T-Helper-{sun_type["S"]}': 1.0,
                       f'T-Helper-{sun_type["N"]}': -1.0,
                       f'T-Reg-{sun_type["S"]}': 1.0,
                       f'T-Reg-{sun_type["N"]}': -1.0,
                       f'T-Killer-{sun_type["S"]}': 1.0,
                       f'T-Killer-{sun_type["N"]}': -1.1,

                       f'P53-{sun_type["S"]}': 0.6,
                       f'P53-{sun_type["N"]}': -0.6,
                       f'KI67-{sun_type["S"]}': 1.1,
                       f'KI67-{sun_type["N"]}': -1.0,
                       f'DDB2-{sun_type["S"]}': 0.7,
                       f'DDB2-{sun_type["N"]}': -0.7,
                       }

for region_id in regions:
    target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
    file_paths.append(target_file_path)

data_list = []
for index in range(len(regions)):
    file_path = file_paths[index]
    df = pd.read_csv(file_path, index_col=None, header=0)
    for l, name in zip([regions, ages, genders, suns, olds, place_holders],
                       ["Region", "Age", "Gender", "Skin Type", "Age Group", "Place Holder"]):
        df[name] = [l[index]] * len(df)
    data_list.append(df)

n_data = pd.concat(data_list, axis=0, ignore_index=True)

print(n_data)

threshold_distance = {
    'cell': n_data['vessel_distance'].quantile(.98),
    'damage': n_data['skin_distance'].quantile(.98)
}

# display box and scatter plot along with violin plot
# fig = pt.violin(n_data, y="distance", x="Age", color="Skin Type",
#                 box=True, hover_data=n_data.columns,
#                 points='all',
#                 )
fig = go.Figure()

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

cell_types = ['', 'CD68', 'T-Helper', 'T-Killer', 'T-Reg']
damage_types = ['', 'P53', 'KI67', 'DDB2']

for item in ['cell', 'damage']:
    cell_type_list = cell_types if item == 'cell' else damage_types
    distance_type = 'vessel_distance' if item == 'cell' else 'skin_distance'

    fig = go.Figure()
    for cell_type in cell_type_list:
        for skin_type in [sun_type["S"], sun_type["N"]]:
            fig.add_trace(
                go.Violin(
                    x=(
                        n_data['type'][(n_data['Skin Type'] == skin_type) &
                                       (n_data['type'].str.contains(cell_type)) &
                                       (n_data[distance_type] >= 0) &
                                       (n_data[distance_type] < threshold_distance[item])]
                        if cell_type != '' else
                        n_data["Place Holder"][(n_data['Skin Type'] == skin_type) &
                                               (n_data[distance_type] >= 0) &
                                               (n_data[distance_type] < threshold_distance[item])]
                    ),
                    y=(
                        n_data[distance_type][(n_data['Skin Type'] == skin_type) &
                                              (n_data['type'].str.contains(cell_type)) &
                                              (n_data[distance_type] >= 0) &
                                              (n_data[distance_type] < threshold_distance[item])]
                        if cell_type != '' else
                        n_data[distance_type][(n_data['Skin Type'] == skin_type) &
                                              (n_data[distance_type] >= 0) &
                                              (n_data[distance_type] < threshold_distance[item])]
                    ),
                    name=skin_type,
                    points="all", opacity=opacity_dict[skin_type],
                    pointpos=point_position_dict[f'{cell_type}-{skin_type}'],
                    side=('positive' if skin_type == sun_type["S"] else 'negative'),
                    legendgroup='All-region', showlegend=True, scalegroup='', scalemode='width',
                    jitter=0.05, marker_opacity=0.5, marker_size=1, line_width=1,
                    legendgrouptitle_text='All-region',
                    box_visible=True, box_fillcolor='white',
                    line_color=color_dict[f'{cell_type}-{skin_type}'], meanline_visible=True)
            )

    # fig.update_traces(# meanline_visible=False,
    #                   scalemode='count')  # scale violin plot area with total count
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
        title=f'Vascular Common Coordinate Framework Violin Chart {main_subtitle}',
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
    fig.update_yaxes(title_text=f"Nearest Distance {title_dict[item]['yaxis']}")
    fig.update_yaxes(range=[-29, 220] if item == 'cell' else [-599, 3600])

    fig.write_html(os.path.join(target_root_path, f"violin_{item}_all_region.html"))
    fig.show()
