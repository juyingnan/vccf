from skimage import io, transform, color
import numpy as np
import os
import random
from scipy import io as sio


def read_img_random(path, total_count, resize=None, as_gray=False, size_filter=10000):
    cate = [path + folder for folder in os.listdir(path) if os.path.isdir(path + folder)]
    for idx, folder in enumerate(cate):
        imgs = list()
        labels = list()
        file_names = list()
        print('reading the images: {}'.format(folder))
        count = 0
        file_path_list = [os.path.join(folder, file_name) for file_name in os.listdir(folder)
                          if os.path.isfile(os.path.join(folder, file_name))]

        while len(labels) < total_count and count < len(file_path_list):
            im = file_path_list[count]
            count += 1
            file_info = os.stat(im)
            file_size = file_info.st_size
            if file_size < size_filter:
                continue
            if file_size > 100 * size_filter:
                continue
            img = io.imread(im, as_gray=as_gray)
            if resize is not None:
                img = transform.resize(img, resize)
            if img.shape[-1] == 4:
                img = img[..., :3]
            imgs.append(img.astype(np.uint8))
            labels.append(idx)
            file_names.append(os.path.basename(im))
            if len(labels) % 100 == 0:
                print("\rreading {0}/{1}".format(len(labels), min(total_count, len(file_path_list))), end='')
        print('\r', end='')
        print('{} images read in {}'.format(len(labels), folder))
        output_folder = os.path.join(r'd:\Projects', '{}.mat'.format(os.path.basename(folder)))
        sio.savemat(output_folder,
                    mdict={'feature_matrix': imgs,
                           'label': labels,
                           'file_names': file_names})
        print('mat file saved at: {}'.format(output_folder))
    # return np.asarray(imgs, np.uint8), np.asarray(labels, int), file_names


if __name__ == '__main__':
    train_image_count = 50000
    train_path = r'C:\Users\bunny\Desktop\pathology_8class_50000each\data_50000/'
    # np.seterr(all='ignore')
    read_img_random(train_path, train_image_count, resize=None, as_gray=False)
