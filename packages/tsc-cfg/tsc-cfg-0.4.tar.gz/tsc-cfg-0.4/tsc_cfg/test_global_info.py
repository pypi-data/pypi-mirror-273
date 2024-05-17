import unittest
import redis
try:
    from .global_info import GlobalInfo, GlobalInfoMem
except:
    from global_info import GlobalInfo, GlobalInfoMem


class TestGlobalInfo(unittest.TestCase):
    def setUp(self):
        self.key_name = 'univglm/test/global_info'
        self.global_info = GlobalInfo(key_name=self.key_name, database=redis.Redis(
            host='127.0.0.1',
            port='',
            password='',
        ))
        self.database = self.global_info.database

    def tearDown(self):
        self.global_info['t'] = {'a': 123}
        self.global_info['t.a'].delete()
        self.assertEqual(self.global_info['t'].v, {})
        n = self.global_info.delete()
        self.assertEqual(n, 1)

    def test_init(self):
        self.assertEqual(self.global_info.key_name, self.key_name)
        self.assertEqual(self.global_info.database, self.database)

    def test_set_get(self):
        self.global_info['key'] = 100
        value = self.global_info['key'].v
        self.assertEqual(value, 100)
        self.global_info['bool.a'] = {'b': False}
        value = self.global_info['bool.a.b'].v
        self.assertEqual(value, False)
        self.assertEqual(self.global_info['bool.a.b'].parent.v, {'b': value})
        string = self.global_info['string']
        string[None] = 'False'
        value = self.global_info['string'].v
        self.assertEqual(value, 'False')

    def test_iadd(self):
        self.global_info['key'] = 10
        self.global_info['key'] += 5
        self.assertEqual(self.global_info['key'].v, 15)
        self.global_info['array'] = []
        self.global_info['array'] += [1, 5]
        self.assertEqual(self.global_info['array'][-1].v, 5)
        self.assertEqual(self.global_info['array[-2]'].v, 1)

    def test_isub(self):
        self.global_info['key'] = 20
        self.global_info['key'] -= 5
        self.assertEqual(self.global_info['key'].v, 15)

    def test_insert(self):
        self.global_info['array'] = [2, 3]
        self.global_info['array'].insert(1)
        self.global_info['array'].append(4)
        self.assertEqual(self.global_info['array'].v, [1, 2, 3, 4])

    def test_pop(self):
        self.global_info['array'] = [1, 2, 3]
        value = self.global_info['array'].pop()
        self.assertEqual(value, 3)
        self.assertEqual(self.global_info['array'].v, [1, 2])
        
        self.global_info['dict'] = {'12': 123, 'a': ''}
        value = self.global_info['dict'].pop('12')
        self.assertEqual(value, 123)
        self.assertEqual(self.global_info['dict'].v, {'a': ''})

    def test_len(self):
        self.global_info['string'] = "abc"
        self.assertEqual(len(self.global_info['string']), 3)
        self.assertEqual(len(self.global_info), 1)

    def test_type(self):
        self.global_info['key'] = 20
        self.assertEqual(self.global_info['key'].type, int)

    def test_bool(self):
        self.global_info['key'] = 123
        self.assertEqual(bool(self.global_info['key']), True)

    def test_cover_dict(self):
        fail_dict = {'1': 2, '3': 4}
        success_dict = {'test': 123}
        d = {}
        d.update(success_dict)
        d.update(fail_dict)
        self.global_info['cover_dict'] = {'test': []}
        fail_dict_ = self.global_info['cover_dict'].cover_dict(d)
        self.assertEqual(fail_dict, fail_dict_)
        self.assertEqual(self.global_info['cover_dict'].v, success_dict)
        
        self.global_info['cover_dict'] = {'test': []}
        fail_dict_ = self.global_info['cover_dict'].cover_dict(d, allow_new=True)
        self.assertEqual({}, fail_dict_)
        self.assertEqual(self.global_info['cover_dict'].v, d)
        
        self.global_info['cover_dict'] = {'test': []}
        fail_dict_ = self.global_info['cover_dict'].cover_dict(d, only_new=True)
        self.assertEqual(success_dict, fail_dict_)
        self.assertEqual(self.global_info['cover_dict'].v, {'test': [], **fail_dict})


class TestGlobalInfoMem(TestGlobalInfo):
    def setUp(self):
        self.key_name = 'univglm/test/global_info_mem'
        self.global_info = GlobalInfoMem(key_name=self.key_name)
        self.database = self.global_info.database


if __name__ == '__main__':
    unittest.main()
