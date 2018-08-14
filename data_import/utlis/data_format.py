#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午10:02
# @Author  : Shark
# @File    : data_format.py
# @Software: PyCharm
import codecs

from config import EV_TYPE_MAP, FILE_PATH, DRIVE_TYPE


lift_type_parameter = dict()


def lift_conversion(types: str):
    """
    电梯类型转换

    :param types: 电梯用途
    :return: 电梯类型数值
    """
    if types:
        return EV_TYPE_MAP[types]

    else:
        raise TypeError


def lift_type_1_or_2(info):
    return {
                'actuationForm': DRIVE_TYPE[info[10]],
                'floors': info[11],
                'station': info[12],
                'door': info[13],
                'maxLoad': info[14],
                'speed': info[15]
            }


def lift_type_3(info):
        return {
                    'floors': info[10],
                    'station': info[11],
                    'door': info[12],
                    'maxLoad': info[13],
                    'speedUp': info[14],
                    'speedDown': info[15],
                    'hydraulicCylinder': [18],
                    'jackingType': info[19]
                }


def lift_type_4(info):
        return {
                    'nominalSpeed': info[10],
                    'nominalWidth': info[11],
                    'inclinationAngle': info[12],
                    'transforAbility': info[13],
                    'liftingHeight': info[14],
                    'length': info[15],
                    'power': info[18]
                }


lift_type_parameter[1] = lift_type_1_or_2
lift_type_parameter[2] = lift_type_1_or_2
lift_type_parameter[3] = lift_type_3
lift_type_parameter[4] = lift_type_4


if __name__ == '__main__':
    pass