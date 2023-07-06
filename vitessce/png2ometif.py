from vitessce.data_utils import rgb_img_to_ome_tiff
from skimage import io
from os.path import join
from tqdm import tqdm

for i in tqdm(range(1, 65)):  # Loop from 1 to 64
    img_file = f'Region_{i}.png'
    output_file = f'Region_{i}.ome.tif'

    img_arr = io.imread(join(r'\\wsl.localhost\Ubuntu\home\bunny\vitessce\static_images', img_file))
    img_arr = img_arr.transpose((2, 0, 1))
    img_arr = img_arr[0:3, :, :]

    rgb_img_to_ome_tiff(
        img_arr,
        output_path=join(r'\\wsl.localhost\Ubuntu\home\bunny\vitessce\static_images', output_file),
        img_name='EUI',
        axes="CYX",
    )
