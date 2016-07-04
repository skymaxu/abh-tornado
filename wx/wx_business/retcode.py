#!/usr/bin/python
#coding: utf-8

# ret code
OK = 0  # ok/success
# 1000 - 1009  argument error
MISS_ARGUMENT = 1000     # missing argument error
INVALID_ARGUMENT_VALUE = 1001     # invalid argument value
# 1020 - 1029
AUTH_FAILED = 1020     # authenticated failed
# 1100 - 1199
USER_ID_NOT_EXIST = 1100

# retcode message
_RET_MSG_MAPPING = {
    OK: '',
    MISS_ARGUMENT: 'missing argument',
    INVALID_ARGUMENT_VALUE: 'invalid argument value',
    AUTH_FAILED: 'authenticated failed',
    USER_ID_NOT_EXIST: 'user not exist'
}

def get_ret_msg(retcode):
    """Get the message that ret code represents.

    Args:
        retcode: An integer ret code.

    Returns:
        A string message that ret code indicates.

        If this retcode is not defined, just return an empty string.
    """
    if retcode in _RET_MSG_MAPPING:
        return _RET_MSG_MAPPING[retcode]
    else:
        return ''


