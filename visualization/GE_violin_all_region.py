import os
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

target_root_path = r"G:\GE\skin_12_data"

file_paths = []

regions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# ages = ['72', '53', '38', '48', '33', '42', '69', '57', '60', '53_', '22', '32']
ages = [72, 53, 38, 48, 33, 42, 69, 57, 60, 53.5, 22, 32]  # the second 53 -> 54
genders = ['Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', ]
suns = ['Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed',
        'Non-Sun-Exposed', 'Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed']
olds = ['old', 'old', 'Young', 'Young', 'Young', 'Young', 'old', 'old', 'old', 'old', 'Young', 'Young']
place_holders = ['All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', 'All', ]

# color_dict = {'Sun-Exposed': 'orange',
#               'Non-Sun-Exposed': 'blue'}

percentage_dict = {
    'CD68': [0.184952978,
             0.188191882,
             0.126099707,
             0.317140238,
             0.078381795,
             0.073265962,
             0.588394062,
             0.124542125,
             0.131067961,
             0.159292035,
             0.072016461,
             0.335238095,
             ],
    'T-Helper': [0.031347962,
                 0.136531365,
                 0.092375367,
                 0.117323556,
                 0.10619469,
                 0.816628388,
                 0.102564103,
                 0.036630037,
                 0.065533981,
                 0.09439528,
                 0.072016461,
                 0.08,
                 ],
    'T-Reg': [0.78369906,
              0.675276753,
              0.781524927,
              0.565536205,
              0.815423515,
              0.11010565,
              0.309041835,
              0.838827839,
              0.803398058,
              0.746312684,
              0.855967078,
              0.584761905,
              ]

}

median_dict = {
    'All': [29.87172576,
            28.48157299,
            26.51490147,
            26.12967661,
            24.8531857,
            21.59722204,
            28.48157299,
            36.29053324,
            28.12329995,
            28.06307847,
            25.07349198,
            23.97081559, ],
    'CD68': [25.18261275,
             21.93882403,
             24.11140809,
             24.97169753,
             35.26811591,
             25.47469332,
             35.1951737,
             60.47445742,
             22.59458342,
             25.89953839,
             78.27513044,
             21.78417619, ],
    'T-Helper': [26.12967661,
                 33.11537765,
                 25.59026882,
                 24.61089343,
                 46.8,
                 21.44014925,
                 33.29624603,
                 40.94484094,
                 24.39016195,
                 24.59705835,
                 31.7370446,
                 29.59924473, ],
    'T-Reg': [20.47242047,
              24.52835094,
              24.77112263,
              26.10379283,
              28.002857,
              22.21440974,
              38.21203999,
              25.93418173,
              26.12967661,
              21.59722204,
              26.01798108,
              23.67215573, ]

}

color_dict = {'Sun-Exposed': 'black',
              'Non-Sun-Exposed': 'grey',
              '-Sun-Exposed': 'black',
              '-Non-Sun-Exposed': 'grey',
              'CD68-Sun-Exposed': 'orangered',
              'CD68-Non-Sun-Exposed': 'orange',
              'T-Helper-Sun-Exposed': 'midnightblue',
              'T-Helper-Non-Sun-Exposed': 'royalblue',
              'T-Reg-Sun-Exposed': 'darkolivegreen',
              'T-Reg-Non-Sun-Exposed': 'mediumseagreen',
              'T-Killer-Sun-Exposed': 'purple',
              'T-Killer-Non-Sun-Exposed': 'violet',
              }

point_position_dict = {'Sun-Exposed': 1.1,
                       'Non-Sun-Exposed': -0.8,
                       '-Sun-Exposed': 1.1,
                       '-Non-Sun-Exposed': -0.8,
                       'CD68-Sun-Exposed': 1.1,
                       'CD68-Non-Sun-Exposed': -0.9,
                       'T-Helper-Sun-Exposed': 1.1,
                       'T-Helper-Non-Sun-Exposed': -0.85,
                       'T-Reg-Sun-Exposed': 1.1,
                       'T-Reg-Non-Sun-Exposed': -0.7,
                       'T-Killer-Sun-Exposed': 1.1,
                       'T-Killer-Non-Sun-Exposed': -0.7,
                       }

opacity_dict = {'Sun-Exposed': 0.7,
                'Non-Sun-Exposed': 0.7}

for region_id in range(1, 13):
    target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
    file_paths.append(target_file_path)

data_list = []
for index in range(12):
    file_path = file_paths[index]
    df = pd.read_csv(file_path, index_col=None, header=0)
    for l, name in zip([regions, ages, genders, suns, olds, place_holders],
                       ["Region", "Age", "Gender", "Skin Type", "Age Group", "Place Holder"]):
        df[name] = [l[index]] * len(df)
    data_list.append(df)

n_data = pd.concat(data_list, axis=0, ignore_index=True)

print(n_data)

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

cell_type_list = ['', 'CD68', 'T-Helper', 'T-Killer']  # , 'T-Reg']
cell_type_dict = {'': 'All',
                  'CD68': 'CD68 / Macrophage',
                  'T-Helper': 'T-Helper',
                  'T-Reg': 'T-Regulator',
                  'T-Killer': 'T-Killer'}
for cell_type in cell_type_list:
    for skin_type in ['Sun-Exposed', 'Non-Sun-Exposed']:
        fig.add_trace(
            go.Violin(x=(n_data['type'][(n_data['Skin Type'] == skin_type) &
                                        (n_data['type'].str.contains(cell_type))]
                         if cell_type != '' else
                         n_data["Place Holder"][(n_data['Skin Type'] == skin_type)]),
                      y=(n_data['distance'][(n_data['Skin Type'] == skin_type) &
                                            (n_data['type'].str.contains(cell_type))]
                         if cell_type != '' else
                         n_data['distance'][(n_data['Skin Type'] == skin_type)]),
                      name=skin_type,
                      points="all", opacity=opacity_dict[skin_type],
                      pointpos=point_position_dict[f'{cell_type}-{skin_type}'],
                      side=('positive' if skin_type == 'Sun-Exposed' else 'negative'),
                      legendgroup='All-region', showlegend=True, scalegroup='', scalemode='width',
                      jitter=0.05, marker_opacity=0.5, marker_size=1, line_width=1,
                      legendgrouptitle_text='All-region',
                      box_visible=True, box_fillcolor='white',
                      line_color=color_dict[f'{cell_type}-{skin_type}'], meanline_visible=True)
        )

# fig.update_traces(# meanline_visible=False,
#                   scalemode='count')  # scale violin plot area with total count
fig.update_layout(
    title="Nearest distance distribution",
    # x1axis_title="Age",
    # y4axis_title="Nearest Distance",
    violingap=0.3, violingroupgap=0,
    violinmode='overlay',
    yaxis_zeroline=False)
fig.update_yaxes(title_text="Nearest Distance",)

fig.write_html(os.path.join(target_root_path, f"violin_all_region.html"))
fig.show()
