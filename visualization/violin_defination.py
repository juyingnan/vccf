regions = [1, 2, 3, 4, 5,
           # 6,
           7, 8, 9, 10, 11, ]  # 12]
# ages = ['72', '53', '38', '48', '33', '42', '69', '57', '60', '53_', '22', '32']
ages = [72, 53, 38, 48, 33,
        # 42,
        69, 57, 60, 53.5, 22, ]  # 32]  # the second 53 -> 54
genders = ['Male', 'Male', 'Male', 'Male', 'Female',
           # 'Female',
           'Male', 'Male', 'Male', 'Female', 'Female', ]  # 'Female', ]
# suns = ['Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Non-Sun-Exposed',
#         # 'Sun-Exposed',
#         'Non-Sun-Exposed', 'Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed']
sun_type = {
    'S': 'Moderate/Marked Sun Exposure',
    'N': 'Mild Sun Exposure'
}
suns = [sun_type['S'], sun_type['N'], sun_type['N'], sun_type['N'], sun_type['N'],
        # 'Sun-Exposed',
        sun_type['S'], sun_type['S'], sun_type['S'], sun_type['S'], sun_type['N'], ]
olds = ['old', 'old', 'Young', 'Young', 'Young',
        # 'Young',
        'old', 'old', 'old', 'old', 'Young', ]  # 'Young']

# color_dict = {'Sun-Exposed': 'orange',
#               'Non-Sun-Exposed': 'blue'}

color_dict = {sun_type["S"]: 'black',
              sun_type["N"]: 'grey',
              f'-{sun_type["S"]}': 'black',
              f'-{sun_type["N"]}': 'grey',
              f'CD68-{sun_type["S"]}': 'orangered',
              f'CD68-{sun_type["N"]}': 'orange',
              f'T-Helper-{sun_type["S"]}': 'midnightblue',
              f'T-Helper-{sun_type["N"]}': 'royalblue',
              f'T-Reg-{sun_type["S"]}': 'darkolivegreen',
              f'T-Reg-{sun_type["N"]}': 'mediumseagreen',
              f'T-Killer-{sun_type["S"]}': 'purple',
              f'T-Killer-{sun_type["N"]}': 'violet',

              f'P53-{sun_type["S"]}': 'brown',
              f'P53-{sun_type["N"]}': 'sandybrown',
              f'KI67-{sun_type["S"]}': 'dodgerblue',
              f'KI67-{sun_type["N"]}': 'lightblue',
              f'DDB2-{sun_type["S"]}': 'darkgreen',
              f'DDB2-{sun_type["N"]}': 'lightgreen',
              }

opacity_dict = {sun_type["S"]: 0.7,
                sun_type["N"]: 0.7}
