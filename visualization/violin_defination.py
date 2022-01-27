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

              'P53-Sun-Exposed': 'brown',
              'P53-Non-Sun-Exposed': 'sandybrown',
              'KI67-Sun-Exposed': 'dodgerblue',
              'KI67-Non-Sun-Exposed': 'lightblue',
              'DDB2-Sun-Exposed': 'darkgreen',
              'DDB2-Non-Sun-Exposed': 'lightgreen',
              }

opacity_dict = {'Sun-Exposed': 0.7,
                'Non-Sun-Exposed': 0.7}