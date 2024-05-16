from testcase import TestCase
from problem import Problem


__all__ = [
    'SIZE_T_UINT64',
    'SIZE_T_INT64',
    'SIZE_T_UINT32',
    'SIZE_T_INT32',
    'TestCase',
    'Problem'
]


SIZE_T_UINT64 = 1 << 64
SIZE_T_INT64 = 1 << 63
SIZE_T_UINT32 = 1 << 32
SIZE_T_INT32 = 1 << 31
