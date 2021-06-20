import os
import os.path
import kaggle
import tarfile
import urllib.request
import numpy as np

from zlib import crc32

datasets_path=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "datasets"))

def get_dataset_path(dest):
    dataset_path = os.path.join(datasets_path, dest)

    if not os.path.exists(dataset_path):
        raise Exception("invalid dataset path: "+dataset_path)

    return dataset_path

def download_dataset(url, dest, format='tar'):
    full_dest = os.path.join(datasets_path, dest)

    if format == 'tar':
        file_stream = urllib.request.urlopen(url)
        tar_file = tarfile.open(fileobj=file_stream, mode="r|gz")
        tar_file.extractall(path=full_dest)
        tar_file.close()
    else:
        urllib.request.urlretrieve(url, dest)

def download_kaggle_dataset_file(dataset_name: str, file_name: str, dest: str, force=False) -> str:
    dest_path = os.path.join(datasets_path, dest)

    # authenticates to kaggle and downloads dataset file
    kaggle.api.authenticate()
    kaggle.api.dataset_download_file(dataset_name, file_name, dest_path, force=force)

    return dest_path

def split_train_test_random(data, test_ratio):
    shuffle_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_set_indices = shuffle_indices[test_set_size:]
    train_set_indices = shuffle_indices[:test_set_size]

    return data.iloc[train_set_indices], data.iloc[test_set_indices]

def split_train_test_by_id(data, test_ratio, id_column):
    def test_set_check(identifier, test_ratio):
        return crc32(np.int64(identifier)) & 0xffffffff < test_ratio * 2**32

    ids = data[id_column]

    in_test_set = ids.apply(lambda id: test_set_check(id, test_ratio))

    return data.loc[~in_test_set], data.loc[in_test_set]