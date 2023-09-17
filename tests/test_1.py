"""
    ---Task 2---
Дополнить все тесты ключом команды 7z -t (тип архива). Вынести этот параметр в конфиг.
"""
import yaml

from bin.checkout import checkout
from bin.hash_calc import calc_crc32

with open('config/config.yaml', 'rb') as f:
    data = yaml.safe_load(f)

class TestPositive:
    def test_step1(self, make_folder, clear_folders, make_files):
        # test1
        res1 = checkout('cd {}; 7zz a -t{} {}/arx2'.format(data['folder_in'], data['arch_type'], data['folder_out']), 'Everything is Ok')
        res2 = checkout('ls {}'.format(data['folder_out']), 'arx2.{}'.format(data['arch_type']))
        assert res1 and res2, "test1 FAIL"


    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(checkout('cd {}; 7zz a -t{} {}/arx2'.format(data['folder_in'], data['arch_type'], data['folder_out']), 'Everything is Ok'))
        res.append(
            checkout('cd {}; 7zz e arx2.{} -o{} -y'.format(data['folder_out'],data['arch_type'], data['folder_ext']), 'Everything is Ok'))
        for item in make_files:
            res.append(checkout('ls {}'.format(data['folder_ext']), item))
        assert all(res), "test2 FAIL"


    def test_step3(self):
        # test3
        assert checkout('cd {}; 7zz t arx2.{}'.format(data['folder_out'],data['arch_type']), 'Everything is Ok'), 'test3 FAIL'


    def test_step4(self):
        # step4
        assert checkout('cd {}; 7zz u arx2.{}'.format(data['folder_in'],data['arch_type']), ''), 'test4 FAIL'


    def test_step5(self, clear_folders, make_files):
        # step5
        res = []
        res.append(checkout('cd {}; 7zz a -t{} {}/arx2'.format(data['folder_in'], data['arch_type'], data['folder_out']), 'Everything is Ok'))
        for item in make_files:
            res.append(checkout('cd {}; 7zz l arx2.{}'.format(data['folder_out'], data['arch_type']), item))
        assert all(res), 'test5 FAIL'


    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(checkout('cd {}; 7zz a -t{} {}/arx'.format(data['folder_in'], data['arch_type'], data['folder_out']), 'Everything is Ok'))
        res.append(
            checkout('cd {}; 7zz x arx.{} -o{} -y'.format(data['folder_out'], data['arch_type'], data['folder_ext2']), 'Everything is Ok'))

        for item in make_files:
            res.append(checkout('ls {}'.format(data['folder_ext2']), item))

        res.append(checkout('ls {}'.format(data['folder_ext2']), make_subfolder[0]))
        res.append(checkout('ls {}/{}'.format(data['folder_ext2'], make_subfolder[0]), make_subfolder[1]))
        assert all(res), 'test6 FAIL'


    def test_step7(self):
        # test7
        assert checkout('cd {}; 7zz d arx.{}'.format(data['folder_out'], data['arch_type']), 'Everything is Ok'), 'test7 FAIL'


    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(checkout('cd {}; 7zz h {}'.format(data['folder_in'], item), 'Everything is Ok'))
            hash = calc_crc32('{}/{}'.format(data['folder_in'], item))
            res.append(checkout('cd {}; 7zz h {}'.format(data['folder_in'], item), hash))
        assert all(res), 'test8 FAIL'
