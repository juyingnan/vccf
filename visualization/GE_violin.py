import os
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from cell_defination import *

target_root_path = r"G:\GE\skin_12_data"

file_paths = []

regions = [1, 2, 3, 4, 5,
           # 6,
           7, 8, 9, 10, 11, 12]
# ages = ['72', '53', '38', '48', '33', '42', '69', '57', '60', '53_', '22', '32']
ages = [72, 53, 38, 48, 33,
        # 42,
        69, 57, 60, 53.5, 22, 32]  # the second 53 -> 54
genders = ['Male', 'Male', 'Male', 'Male', 'Female',
           # 'Female',
           'Male', 'Male', 'Male', 'Female', 'Female', 'Female', ]
suns = ['Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Non-Sun-Exposed',
        # 'Sun-Exposed',
        'Non-Sun-Exposed', 'Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed']
olds = ['old', 'old', 'Young', 'Young', 'Young',
        # 'Young',
        'old', 'old', 'old', 'old', 'Young', 'Young']

# color_dict = {'Sun-Exposed': 'orange',
#               'Non-Sun-Exposed': 'blue'}

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

opacity_dict = {'Sun-Exposed': 0.7,
                'Non-Sun-Exposed': 0.7}

for region_id in regions:
    target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
    file_paths.append(target_file_path)

data_list = []
for index in range(12 - 1):
    file_path = file_paths[index]
    df = pd.read_csv(file_path, index_col=None, header=0)
    for l, name in zip([regions, ages, genders, suns, olds], ["Region", "Age", "Gender", "Skin Type", "Age Group"]):
        df[name] = [l[index]] * len(df)
    data_list.append(df)

n_data = pd.concat(data_list, axis=0, ignore_index=True)

print(n_data)

cell_type_list = ['', 'CD68', 'T-Helper', 'T-Killer', 'T-Reg']
cell_dict[''] = {}
cell_dict['']['legend'] = 'All Cells'

# display box and scatter plot along with violin plot
# fig = pt.violin(n_data, y="distance", x="Age", color="Skin Type",
#                 box=True, hover_data=n_data.columns,
#                 points='all',
#                 )
subplot_titles = []
for cell_type in cell_type_list:
    subplot_titles.append(cell_dict[cell_type]['legend'])
fig = make_subplots(
    rows=5, cols=1,
    row_heights=[0.2, 0.2, 0.2, 0.2, 0.2],
    # specs=[[{"type": "Scatter3d", "colspan": 4}, None, None, None],
    #        [{"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}, {"type": "Histogram"}]],
    shared_xaxes=True,
    vertical_spacing=0.02,
    # subplot_titles=[f'All', 'CD68 / Macrophage', 'T-Helper', 'T-Regulatory'],
    subplot_titles=subplot_titles,
    specs=[[{"secondary_y": False}],
           [{"secondary_y": True}],
           [{"secondary_y": True}],
           [{"secondary_y": True}],
           [{"secondary_y": True}], ]
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


for cell_type in cell_type_list:
    for skin_type in ['Sun-Exposed', 'Non-Sun-Exposed']:
        fig.add_trace(
            go.Violin(x=n_data['Age'][(n_data['Skin Type'] == skin_type) & (n_data['type'].str.contains(cell_type))],
                      y=n_data['vessel_distance'][(n_data['Skin Type'] == skin_type) &
                                                  (n_data['type'].str.contains(cell_type))],
                      name=skin_type,
                      points=False, opacity=opacity_dict[skin_type], width=4,
                      legendgroup=cell_dict[cell_type]['legend'], scalegroup='', scalemode='width',
                      legendgrouptitle_text=cell_dict[cell_type]['legend'],
                      box_visible=True, box_fillcolor='white', line_width=1,
                      line_color=color_dict[f'{cell_type}-{skin_type}'], meanline_visible=False),
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
main_subtitle = f'<br><sup>Nearest distance from cells to Endothelial cells</sup>'
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
fig.update_xaxes(title_text="Age", row=5, col=1)
fig.update_yaxes(title_text="Nearest Distance to Endothelial Cells", row=3, col=1)
fig.update_yaxes(title_text="Percentage", row=2, col=1, secondary_y=True)
fig.update_yaxes(range=[-99, 550])

# subtitle location
vertical_offset = 0.02
for annotation in fig['layout']['annotations']:
    annotation['xanchor'] = "center"
    annotation['y'] -= vertical_offset
    annotation['font'] = dict(
        family="Arial, Bahnschrift",
        size=16, )

fig.write_html(os.path.join(target_root_path, f"violin.html"))
fig.show()
