import numpy as np
import plotly.graph_objects as go
import skimage.io as sio

x = np.linspace(-2,2, 128)
y = np.linspace(-2,2, 128)
z = np.linspace(0,0, 128)
x, y = np.meshgrid(x, y)
# y = np.sin(x**2*z)

fig = go.Figure(go.Surface(#x=x, y=y, z=z,
                           colorscale='RdBu',
                           showscale=False))
image = sio.imread ("https://raw.githubusercontent.com/empet/Discrete-Arnold-map/master/Images/cat-128.jpg")
print(image.shape)
img = image[:,:, 1]
# Y = 0.5 * np.ones(y.shape)
fig.add_surface(x=x, y=y, z=z,
                surfacecolor=np.flipud(img),
                colorscale='matter_r',
                showscale=False)

fig.show()