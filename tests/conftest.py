"""
    ---Task 1---
Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt строку вида:
время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из файла /proc/loadavg
(можно писать просто всё содержимое этого файла).
"""
from datetime import datetime
import random
import string

import pytest
import yaml

from bin.checkout import checkout
from bin.lib_for_hw import get_cpu_load

with open('config/config.yaml', 'rb') as f:
    data = yaml.safe_load(f)


# ---Task 1---
@pytest.fixture(autouse=True)
def write_to_stat_file():
    current_time = datetime.now().strftime('%H:%M:%S.%f')
    config_file_count = data['count']
    config_file_size = data['file_size']
    cpu_load_data = get_cpu_load(data['os_system'])

    # Создаем строку для записи в файл stat.txt
    stat_line = f"{current_time}, {config_file_count}, {config_file_size}, {cpu_load_data}\n"

    # Открываем файл stat.txt для дописывания
    with open('logs/stat.txt', 'a') as stat_file:
        stat_file.write(stat_line)


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
        if checkout('cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock'.format(data['folder_in'], filename,
                                                                                           data['file_size']),
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
