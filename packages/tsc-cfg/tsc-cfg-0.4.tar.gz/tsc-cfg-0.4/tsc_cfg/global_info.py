import redis
import json
from typing import Any, List, Tuple, Callable, Union, Optional
from tsc_base import dict_to_pair, pair_to_dict, get, put
import re
from jsonpath_ng import parse, jsonpath
from functools import lru_cache
import redis.asyncio as async_redis


class GlobalInfo:
    split_path_re = re.compile(r'(?=\[)|(?<=\])|\.')
    
    def __init__(self,
                 key_name: str,
                 sub_path: str = '',
                 database: redis.Redis = None,
                 config: Optional[Union[dict, list]] = None,
                 allow_new_key: bool = True,
                 reuse_root: bool = False,
                 jsonpath_parse_cache_maxsize: int = 1000,
                 ) -> None:
        """
        基于Redis的全局配置文件
        :param key_name: 配置文件名, 不要重复
        :param sub_path: 简单JSONPath, 不支持多值返回(多值返回第一个匹配). abc[0].abc
        :param database: redis.Redis 对象，可以通过 redis.Redis(host='', port='', db=0, password='') 创建
        :param config: 默认根目录为 {}; key 不能留空或包含 '[. $@,*]"
        :param allow_new_key: 遇到不存在的key是否创建
        :param reuse_root: 复用根目录，不再重新 SET，也将忽略输入的 config
        :param jsonpath_parse_cache_maxsize: jsonpath_parse 缓存大小
        """
        assert database is not None, 'database is None!'
        sub_path = f".{sub_path.strip('$. ')}"
        if sub_path == '.' and config is None and allow_new_key:
            config = {}
        if not reuse_root and config is not None:
            database.execute_command('JSON.SET', key_name, sub_path, json.dumps(config))

        self.key_name = key_name
        self.sub_path = sub_path
        self.database = database
        self.allow_new_key = allow_new_key
        self.jsonpath_parse: Callable[[str], jsonpath.Child] = lru_cache(
            maxsize=jsonpath_parse_cache_maxsize)(lambda string: parse(string))

    def _execute_command(self, json_cmd: str, *args, **options) -> Any:
        return self.database.execute_command(f'JSON.{json_cmd}', self.key_name, *args, **options)

    def _ensure_path_exists(self, path: str):
        if not path:
            return
        path_L = self._split_path(path)
        path_L.pop()
        _path = ''
        for p in path_L:
            _path += f".{p}"
            if self._execute_command('TYPE', _path) is None:
                if p[0] == '[' and p[-1] == ']':
                    raise ValueError(f'path does not exist: {_path}')
                self._execute_command('SET', _path, '{}')

    def _get_path(self, key: Optional[Union[str, int]] = None) -> str:
        p = ''
        if self.sub_path:
            p += self.sub_path
        if isinstance(key, int):
            p += f'[{key}]'
        elif key:
            p = p.rstrip('.')
            p += f".{key.strip('$. ')}"
        assert p
        return p

    def _decode_value(self, value: Union[bytes, str], json_type: str = None) -> Any:
        decoded_value = value.decode('utf-8') if isinstance(value, bytes) else value
        if json_type is None:
            json_type = self._json_type
        if json_type == 'integer':
            return int(decoded_value)
        elif json_type == 'number':
            return float(decoded_value)
        elif json_type == 'boolean':
            return True if decoded_value == 'true' else False
        elif json_type in ['string', 'array', 'object']:
            return json.loads(decoded_value)
        else:
            return None

    def __getitem__(self, key: Union[str, int]) -> 'GlobalInfo':
        return type(self)(
            key_name=self.key_name,
            sub_path=self._get_path(key),
            database=self.database,
            allow_new_key=self.allow_new_key,
        )

    def __setitem__(self, key: Optional[Union[str, int]], value: Any) -> None:
        if isinstance(value, type(self)):
            return
        path = self._get_path(key)
        if self.allow_new_key:
            self._ensure_path_exists(path)
        self._execute_command('SET', path, self._dumps(value))

    def __iadd__(self, other: Union[int, float, List]) -> 'GlobalInfo':
        json_type = self._json_type
        if isinstance(other, (int, float)) and json_type in ['integer', 'number']:
            self._execute_command('NUMINCRBY', self._get_path(), other)
        elif isinstance(other, list) and json_type == 'array':
            other_ = [self._dumps(v) for v in other]
            self._execute_command('ARRAPPEND', self._get_path(), *other_)
        else:
            raise TypeError(f'Error type: {type(other)}, {json_type}')
        return self

    def __isub__(self, other: Union[int, float]) -> 'GlobalInfo':
        if isinstance(other, (int, float)):
            self.__iadd__(-other)
        else:
            raise TypeError(f'Error type: {type(other)}')
        return self

    def __bool__(self) -> bool:
        try:
            return bool(len(self))
        except TypeError:
            return bool(self.v)

    def __len__(self) -> Optional[int]:
        json_type = self._json_type
        if json_type == 'string':
            return self._execute_command('STRLEN', self._get_path())
        elif json_type == 'array':
            return self._execute_command('ARRLEN', self._get_path())
        elif json_type == 'object':  # 可能费带宽
            return len(self.v)
        else:
            raise TypeError(f"object of type '{json_type}' has no len()")

    def insert(self, value: Any, index: int = 0):
        self._execute_command('ARRINSERT', self._get_path(), index, self._dumps(value))
        
    def append(self, value: Any):
        self._execute_command('ARRAPPEND', self._get_path(), self._dumps(value))

    def pop(self, key: Union[str, int] = -1) -> Any:
        json_type = self._json_type
        if isinstance(key, str) and json_type == 'object':
            script = """
                local value = redis.call('JSON.GET', KEYS[1], ARGV[1])
                redis.call('JSON.DEL', KEYS[1], ARGV[1])
                return value
            """
            sha = self.database.script_load(script)
            value = self.database.evalsha(sha, 1, self.key_name, self._get_path(key))
        elif isinstance(key, int) and json_type == 'array':
            value = self._execute_command('ARRPOP', self._get_path(), key)
        else:
            raise TypeError(f'Error type: {type(key)}, {json_type}')
        return self._decode_value(value)
    
    def delete(self, key: Optional[Union[str, int]] = None) -> int:
        # key=None 删除自身
        return self._execute_command('DEL', self._get_path(key))
    
    def cover_dict(self, d: dict, only_new=False, allow_new=False) -> dict:
        # 默认 只覆盖已有的
        fail_pairs: List[Tuple[List, Any]] = []
        for keys, value in dict_to_pair(d):
            key = '.'.join(keys)
            path = self._get_path(key)
            if only_new:  # 只加入新的
                if self._execute_command('TYPE', path) is None:
                    self._ensure_path_exists(path)
                    self._execute_command('SET', path, self._dumps(value))
                else:
                    fail_pairs.append((keys, value))
            else:
                if allow_new:  # 全覆盖
                    self._ensure_path_exists(path)
                    self._execute_command('SET', path, self._dumps(value))
                elif self._execute_command('TYPE', path) is not None:  # 只覆盖已有的
                    self._execute_command('SET', path, self._dumps(value))
                else:
                    fail_pairs.append((keys, value))
        return pair_to_dict(fail_pairs)

    @property
    def v(self) -> Any:
        value = self._execute_command('GET', self.sub_path)
        return self._decode_value(value)

    @property
    def type(self) -> Optional[type]:
        json_type = self._json_type
        if json_type == 'string':
            return str
        elif json_type == 'array':
            return list
        elif json_type == 'object':
            return dict
        elif json_type == 'integer':
            return int
        elif json_type == 'number':
            return float
        elif json_type == 'boolean':
            return bool
        elif json_type == 'null':
            return type(None)
        else:
            return None
            
    @property
    def parent(self) -> Optional['GlobalInfo']:
        if self.sub_path == '.':
            return None
        path_L = self._split_path(self.sub_path)
        path_L.pop()
        if not path_L:
            return self
        return type(self)(
            key_name=self.key_name,
            sub_path='.'.join(path_L),
            database=self.database,
            allow_new_key=self.allow_new_key,
        )

    @property
    def _json_type(self) -> Optional[str]:
        ret: bytes = self._execute_command('TYPE', self.sub_path)
        if ret is None:  # path 不存在
            return None
        return ret.decode('utf-8')

    @classmethod
    def _split_path(cls, path: str) -> List[str]:
        return list(filter(None, cls.split_path_re.split(path)))

    @staticmethod
    def _dumps(value: Any) -> Optional[Union[int, float, str, bool]]:
        if isinstance(value, (list, dict, str, bool, type(None))):
            value = json.dumps(value)
        elif not isinstance(value, (int, float)):
            raise TypeError(f'Error type: {type(value)}')
        return value


class GlobalInfoMem:  # 模拟一个无需redis的内存版本
    split_path_re = re.compile(r'(?=\[)|(?<=\])|\.')
    
    def __init__(self,
                 key_name: str,
                 sub_path: str = '',  # 简单的jsonpath
                 database: redis.Redis = None,
                 config: Optional[Union[dict, list]] = None,
                 allow_new_key: bool = True,
                 jsonpath_parse_cache_maxsize: int = 1000,
                 **kwargs,
                 ) -> None:
        sub_path = f".{sub_path.strip('$. ')}"
        if sub_path == '.' and config is None and allow_new_key:
            config = {}
            
        self.key_name = key_name
        self.sub_path = sub_path
        self.config = config
        self.database = database
        self.allow_new_key = allow_new_key
        self.jsonpath_parse: Callable[[str], jsonpath.Child] = lru_cache(
            maxsize=jsonpath_parse_cache_maxsize)(lambda string: parse(string))

    def _get_path(self, key: Optional[Union[str, int]] = None) -> str:
        p = ''
        if self.sub_path:
            p += self.sub_path
        if isinstance(key, int):
            p += f'[{key}]'
        elif key:
            p = p.rstrip('.')
            key = key.strip('$. ')
            keys = key.split('.')
            for i, k in enumerate(keys):
                try:
                    keys[i] = f'"{int(k)}"'  # 这里数字要加引号
                except:
                    ...
            p += f".{'.'.join(keys)}"
        assert p
        return p

    def __getitem__(self, key: Union[str, int]) -> 'GlobalInfoMem':
        return type(self)(
            key_name=self.key_name,
            sub_path=self._get_path(key),
            config=self.config,
            database=self.database,
            allow_new_key=self.allow_new_key,
        )

    def __setitem__(self, key: Optional[Union[str, int]], value: Any):
        if isinstance(value, type(self)):
            return
        path = self._get_path(key)
        jsonpath_expr = self.jsonpath_parse(self._norm_path(path))
        if self.allow_new_key:
            jsonpath_expr.update_or_create(self.config, value)
        else:
            jsonpath_expr.update(self.config, value)

    def __iadd__(self, other: Union[int, float, list]) -> 'GlobalInfoMem':
        _type = self.type
        if isinstance(other, (int, float)) and _type in [int, float]:
            keys = self._path_to_keys(self.sub_path)
            if len(keys) == 1:
                self.config[keys[0]] += other
            elif len(keys) > 1:  # 线程安全
                get(keys[:-1], self.config)[keys[-1]] += other
        elif isinstance(other, list) and _type == list:
            v: list = self.v
            v += other
        else:
            raise TypeError(f'Error type: {type(other)}, {_type}')
        return self

    def __isub__(self, other: Union[int, float]) -> 'GlobalInfo':
        if isinstance(other, (int, float)):
            self.__iadd__(-other)
        else:
            raise TypeError(f'Error type: {type(other)}')
        return self

    def __bool__(self) -> bool:
        return bool(self.v)

    def __len__(self) -> bool:
        return len(self.v)

    def insert(self, value: Any, index: int = 0):
        v: list = self.v
        v.insert(index, value)
        
    def append(self, value: Any):
        v: list = self.v
        v.append(value)

    def pop(self, key: Union[str, int] = -1) -> Any:
        _type = self.type
        if isinstance(key, str) and _type == dict:
            keys = self._path_to_keys(self._get_path(key))
            if len(keys) == 1:
                value = self.config.pop(keys[0])
            else:
                value = get(keys[:-1], self.config).pop(keys[-1])
        elif isinstance(key, int) and _type == list:
            v: list = self.v
            value = v.pop(key)
        else:
            raise TypeError(f'Error type: {type(key)}, {_type}')
        return value
    
    def delete(self, key: Optional[Union[str, int]] = None) -> int:
        # key=None 删除自身
        if key is None:
            keys = self._path_to_keys(self._get_path())
            if len(keys) == 0:
                del self.config
            else:
                put(keys, self.config, delete=True)
        else:
            self.pop(key)
        return 1
    
    def cover_dict(self, d: dict, only_new=False, allow_new=False) -> dict:
        # 默认 只覆盖已有的
        fail_pairs: List[Tuple[List, Any]] = []
        for keys, value in dict_to_pair(d):
            key = '.'.join(keys)
            path = self._get_path(key)
            jsonpath_expr = self.jsonpath_parse(self._norm_path(path))
            full_keys = self._path_to_keys(self._get_path()) + keys
            if only_new:  # 只加入新的
                if jsonpath_expr.find(self.config):
                    fail_pairs.append((keys, value))
                else:
                    put(full_keys, self.config, value)
            else:
                if allow_new:  # 全覆盖
                    put(full_keys, self.config, value)
                elif jsonpath_expr.find(self.config):  # 只覆盖已有的
                    put(full_keys, self.config, value)
                else:
                    fail_pairs.append((keys, value))
        return pair_to_dict(fail_pairs)

    @property
    def v(self) -> Any:
        jsonpath_expr = self.jsonpath_parse(self._norm_path(self.sub_path))
        matchs = jsonpath_expr.find(self.config)
        assert matchs, '没有值!'
        return matchs[0].value

    @property
    def type(self) -> Optional[type]:
        return type(self.v)
            
    @property
    def parent(self) -> Optional['GlobalInfoMem']:
        if self.sub_path == '.':
            return None
        path_L = self._split_path(self.sub_path)
        path_L.pop()
        if not path_L:
            return self
        return type(self)(
            key_name=self.key_name,
            sub_path='.'.join(path_L),
            config=self.config,
            database=self.database,
            allow_new_key=self.allow_new_key,
        )
    
    @classmethod
    def _split_path(cls, path: str) -> List[str]:
        return list(filter(None, cls.split_path_re.split(path)))
    
    @classmethod
    def _path_to_keys(cls, path: str) -> List[Union[str, int]]:
        path_L = cls._split_path(path)
        keys = []
        for p in path_L:
            if p[0] == '[' and p[-1] == ']':
                keys.append(int(p[1:-1]))
            else:
                if len(p) > 1 and (p[0] == p[-1] == '\'' or p[0] == p[-1] == '"'):
                    keys.append(p[1:-1])
                else:
                    keys.append(p)
        return keys
    
    @staticmethod
    def _norm_path(path: str) -> str:
        return f'${path}'.strip('.')
