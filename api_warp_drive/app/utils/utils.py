#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-18 下午1:30
# @Author  : Shark
# @File    : utils.py
# @Software: PyCharm


def parameter_check(k: str, kwargs: dict):
    if k in kwargs.keys():
        return kwargs[k]
    else:
        return None


def return_result(**kwargs):
    result = {
                "code": kwargs['code'] if 'code' in kwargs.items() else 0,
                "message": parameter_check('message', kwargs),
                "obj": {
                    "companyId": parameter_check('companyId', kwargs),
                    "date": str(parameter_check('date', kwargs)),
                    "projectInfo": parameter_check('projectInfo', kwargs),
                    "repairTask": kwargs['repairTask'] if 'repairTask' in kwargs.items() else 0,
                    "maintenanceTask": kwargs['maintenanceTask'] if 'maintenanceTask' in kwargs.items() else 0,
                    "month": parameter_check('month', kwargs),
                    "totalElevators": kwargs['totalElevators'] if 'totalElevators' in kwargs.items() else 0,
                    "totalEmployees": kwargs['totalEmployees'] if 'totalEmployees' in kwargs.items() else 0,
                    "total": kwargs['total'] if 'total' in kwargs.items() else 0,
                    "source": parameter_check('source', kwargs),
                },
                "tokenStr": parameter_check('token', kwargs)
            }
    # for k in list(result.keys()):
    #     if result[k] is None:
    #         del result[k]
    print(result)
    return result


if __name__ == '__main__':
    return_result(companyId=5)

# {
#             "code": 0,
#             "message": "",
#             "obj": {
#                 "companyId": company_id,
#                 "date": today_month,
#                 "total": 0,
#                 "source": {
#                     "wechat": 0,
#                     "mix": 0,
#                     "nano": 0
#                 }
#             },
#             "tokenStr": token
#         }