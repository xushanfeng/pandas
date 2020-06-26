import time


def base_success_res(data):
    return {
        "server_time": int(time.time()),
        "result_code": 'success',
        "data": data
    }


def base_fail_res(data, msg=None):
    return {
        "server_time": int(time.time()),
        "result_code": 'error',
        "msg": msg,
        "data": data
    }
