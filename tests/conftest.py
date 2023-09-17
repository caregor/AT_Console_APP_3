from datetime import datetime
import random
import string

import pytest
import yaml

from bin.checkout import checkout

with open('tests/config.yaml', 'rb') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    return checkout(
        'mkdir {} {} {} {}'.format(data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_ext2']), "")


@pytest.fixture()
def clear_folders():
    return checkout('rm -rf {}/* {}/* {}/* {}/*'.format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                        data['folder_ext2']), "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout('cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['folder_in'], filename),
                    ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout('cd {}; mkdir {}'.format(data['folder_in'], subfoldername), ""):
        return None, None
    if not checkout(
            'cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['folder_in'], subfoldername,
                                                                                      testfilename), ''):
        return subfoldername, None

    return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_time():
    print('Start: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))
    yield print('Stop: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))
