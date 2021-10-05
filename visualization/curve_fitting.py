import os
import plotly.graph_objects as go
import pandas as pd
import warnings
import numpy as np
import scipy.stats as st
import statsmodels.api as sm
import matplotlib
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots


# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [
        st.alpha, st.anglit, st.arcsine,
        st.beta, st.betaprime, st.bradford, st.burr, st.cauchy, st.chi, st.chi2, st.cosine,
        st.dgamma, st.dweibull, st.erlang, st.expon, st.exponnorm, st.exponweib, st.exponpow, st.f, st.fatiguelife,
        st.fisk, st.foldcauchy, st.foldnorm, st.genlogistic, st.genpareto, st.gennorm, st.genexpon,
        st.genextreme, st.gausshyper, st.gamma, st.gengamma, st.genhalflogistic, st.gilbrat, st.gompertz, st.gumbel_r,
        st.gumbel_l, st.halfcauchy, st.halflogistic, st.halfnorm, st.halfgennorm, st.hypsecant, st.invgamma,
        st.invgauss, st.invweibull, st.johnsonsb, st.johnsonsu, st.ksone, st.kstwobign, st.laplace, st.levy, st.levy_l,
        st.loggamma, st.loglaplace,
        st.lognorm, st.lomax, st.maxwell, st.mielke,
        st.nakagami, st.ncx2, st.ncf,
        st.nct, st.norm, st.pareto, st.pearson3, st.powerlaw, st.powerlognorm, st.rdist, st.reciprocal,
        st.rayleigh, st.rice, st.recipinvgauss, st.semicircular, st.t, st.triang, st.truncexpon, st.truncnorm,
        st.tukeylambda, st.uniform,
        st.vonmises_line, st.wald, st.weibull_min, st.weibull_max,
        st.wrapcauchy,

        # st.logistic,st.levy_stable, # too slow
        # st.vonmises, # no result
        # st.powernorm, # nan result
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    diffs = {}
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                diffs[distribution.name] = sse

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params, diffs)


def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf


target_root_path = r"G:\GE\skin_12_data"

file_paths = []

regions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# ages = ['72', '53', '38', '48', '33', '42', '69', '57', '60', '53_', '22', '32']
ages = [72, 53, 38, 48, 33, 42, 69, 57, 60, 53.5, 22, 32]  # the second 53 -> 54
genders = ['Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', ]
suns = ['Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed',
        'Non-Sun-Exposed', 'Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed', 'Sun-Exposed', 'Non-Sun-Exposed']
olds = ['old', 'old', 'Young', 'Young', 'Young', 'Young', 'old', 'old', 'old', 'old', 'Young', 'Young']

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

opacity_dict = {'Sun-Exposed': 0.7,
                'Non-Sun-Exposed': 0.7}

for region_id in range(1, 13):
    target_file_path = target_root_path + rf"\region_{region_id}\nuclei.csv"
    file_paths.append(target_file_path)

data_list = []
for index in range(12):
    file_path = file_paths[index]
    df = pd.read_csv(file_path, index_col=None, header=0)
    for l, name in zip([regions, ages, genders, suns, olds], ["Region", "Age", "Gender", "Skin Type", "Age Group"]):
        df[name] = [l[index]] * len(df)
    data_list.append(df)

n_data = pd.concat(data_list, axis=0, ignore_index=True)
print(n_data)

cell_type_list = ['', 'CD68', 'T-Helper', 'T-Reg']
cell_type_dict = {'': 'All',
                  'CD68': 'CD68 / Macrophage',
                  'T-Helper': 'T-Helper',
                  'T-Reg': 'T-Regulatory',
                  'T-Killer': 'T-Killer'}

# plt.figure(figsize=(12, 8))
region_count = 12
fig, axs = plt.subplots(region_count + 3, 2)
for i in range(region_count + 3):
    if i < region_count:
        region_data = n_data['distance'][n_data["Region"] == i + 1].squeeze()
        title = f'Region {i + 1}'
    elif i == region_count:
        region_data = n_data['distance'].squeeze()
        title = f'ALL'
    elif i == region_count + 1:
        region_data = n_data['distance'][n_data["Skin Type"] == 'Sun-Exposed'].squeeze()
        title = f'SUN-EXPOSED'
    elif i == region_count + 2:
        region_data = n_data['distance'][n_data["Skin Type"] == 'Non-Sun-Exposed'].squeeze()
        title = f'NON-SUN-EXPOSED'
    else:
        continue

    # print(region_data)

    for col in [0,1]:
        region_data.plot(kind='hist',
                         # bins=50,
                         # bins=np.arange(0, max(region_data) + 5, 5),
                         bins=np.arange(0, 205, 5),
                         density=True, alpha=0.5,
                         color=plt.rcParams['axes.prop_cycle'].by_key()['color'][1], ax=axs[i, col])

        dataYLim = axs[i, 0].get_ylim()
        axs[i, col].set_ylim(dataYLim)
        axs[i, col].set_xlim(0)

    # Save plot limits

    # Find best fit distribution
    best_fit_name, best_fit_params, differences = best_fit_distribution(region_data, 200, axs[i, 0])
    # print(differences)
    if i == 0:
        for key in sorted(differences.keys()):
            print(key, end="\t")
        print()
    for key in sorted(differences.keys()):
        print(differences[key], end="\t")
    print()
    best_dist = getattr(st, best_fit_name)

    # Update plots
    # axs[i, 0].set_title(u'El Niño sea temp.\n All Fitted Distributions')
    # axs[i, 0].set_xlabel(u'Temp (°C)')
    # axs[i, 0].set_ylabel('Frequency')

    # Make PDF with best params
    pdf = make_pdf(best_dist, best_fit_params)

    # Display
    pdf.plot(lw=2, label='PDF', legend=True, ax=axs[i, 1])
    # region_data.plot(kind='hist',
    #                  # bins=50,
    #                  # bins=np.arange(0, max(region_data) + 5, 5),
    #                  bins=np.arange(0, 205, 5),
    #                  density=True, alpha=0.5, label='Data', legend=False, ax=axs[i, 1])

    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k, v) for k, v in zip(param_names, best_fit_params)])
    dist_str = '{}({})'.format(best_fit_name, param_str)

    # axs[i, 1].set_ylim(dataYLim)
    axs[i, 1].set_title(f'{dist_str}\n{title}', y=1.0, pad=-60)
    # axs[i, 1].set_xlabel(u'Temp. (°C)')
    # axs[i, 1].set_ylabel('Frequency')
plt.show()
