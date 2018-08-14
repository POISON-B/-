#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-6-15 下午3:16
# @Author  : Shark
# @Site    : 
# @File    : excel_to_db.py
# @Software: PyCharm
# import pymysql
# import pymysql.cursors

import csv
import datetime
import time

from config import *
from Tools_function import *
from db_Initialization import *


class ReadExcle(object):
    def __init__(self):
        self.project_list = list()
        self.ev_list = list()
        self.address_json = {
            "longitude": None,
            "latitude": None,
            "province": None,
            "city": None,
            "country": None,
            "address": None
        }

    def handle_data(self, file_name):
        csv_data = csv.reader(open(file_name))
        for line in csv_data:
            project_md5_info = project_md5(line[0] + line[4])

            address_dict_json_info = address_dict_json(ADDRESS_JSON)

            if project_md5_info in address_dict_json_info.keys():
                line.append(address_dict_json_info[project_md5_info])

            else:
                lat = get_Lat_lon(line[1] + line[4])
                address = get_address(lat)
                self.address_json['longitude'] = lat['lng']
                self.address_json['latitude'] = lat['lat']
                self.address_json['province'] = address['province']
                self.address_json['city'] = address['city']
                self.address_json['country'] = address['district']
                self.address_json['address'] = address['address']
                address_dict_json_info[project_md5_info] = self.address_json

                insert_json(address_dict_json_info, ADDRESS_JSON)
                line.append(self.address_json)

            logger.info('正在格式化{0}项目的地址信息'.format(line[0]))
            if line[1] and line[2] and line[3]:
                address_id = get_area_from_db(line[1], line[2], line[3])
                line[1] = address_id['province_id']
                line[2] = address_id['city_id']
                line[3] = address_id['district_id']

                self.project_list.append(line)

            elif not line[1] or not line[2] or not line[3]:
                line[1] = line[5]['province']
                line[2] = line[5]['city']
                line[3] = line[5]['country']
                address_id = get_area_from_db(line[1], line[2], line[3])
                line[1] = address_id['province_id']
                line[2] = address_id['city_id']
                line[3] = address_id['district_id']

                self.project_list.append(line)
        return self.project_list

    def handle_evinfo_data(self, file_name):
        csv_ev_data = csv.reader(open(file_name))
        for line in csv_ev_data:
            year_time = clean_time(line[16])
            line[16] = year_time
            create_time = clean_time(line[7])
            line[7] = create_time
            clean_value = remove_spec_char(line[4])
            line[4] = bytes(clean_value, encoding="utf8")
            if ev_type_map[line[3]] == 1 or 2:
                line[11] = value_clean(line[11])
                line[12] = value_clean(line[12])
                line[13] = value_clean(line[13])
                line[14] = value_clean(line[14])
                line[15] = value_clean(line[15])
            elif ev_type_map[line[3]] == 3:
                line[10] = value_clean(line[10])
                line[11] = value_clean(line[11])
                line[12] = value_clean(line[12])
                line[13] = value_clean(line[13])
                line[14] = value_clean(line[14])
                line[15] = value_clean(line[15])
                line[18] = value_clean(line[18])
                line[19] = value_clean(line[19])
            else:
                line[10] = value_clean(line[10])
                line[11] = value_clean(line[11])
                line[12] = value_clean(line[12])
                line[13] = value_clean(line[13])
                line[14] = value_clean(line[14])
                line[15] = value_clean(line[15])
                line[18] = value_clean(line[18])
            brand_id = db_brand_query.filter(db_brand.name == line[2]).first()  # 电梯品牌查询
            if brand_id:
                line[2] = brand_id.uuid
            else:
                line[2] = None
            self.ev_list.append(line)
        return self.ev_list


class DataToDb(object):
    def __init__(self, weibao_name):
        self.weibao_name = weibao_name
        self.project_update_number = 0
        self.project_insert_number = 0
        self.project_error_number = 0
        self.elevator_update_number = 0
        self.elevator_insert_number = 0
        self.elevator_error_number = 0
        self.reagecode_none_update = 0
        self.reagecode_none_insert = 0

    def create_project(self, file_name):
        """
        :param:创建项目 生成分布式唯一id（用pysnowflake或用 JPype直接调用java) 查询根据项目名数据库projectinfo表如果项目存在则判断信息
        是否合格，合格则跳过，不合格则更新信息。不存在则创建项目


        :return: 不反回值

        """
        for line in ReadExcle().handle_data(file_name):

            try:
                projects = projectInfo_domain_query.filter(db_projectInfo.name.like('%' + line[0][:20])).all()

                if len(projects) > 1:
                    for project in projects:
                        if project.address == line[4]:
                            logger.warning('项目{0}已存在,更新信息'.format(line[0]))
                            update_project(project, line)

                            self.project_update_number += 1
                        elif project.name == line[0][:20] and project.country == line[3]:
                            logger.info('项目{0}已存在，更新信息'.format(line[0]))
                            update_project(project, line)

                            self.project_update_number += 1
                        elif project.province == line[1] or project.country == line[3] or project.city == line[2]:
                            logger.error('{0}项目可能和数据库中的项目冲突，确认之后再导入'.format(line[0]))
                            with open('项目冲突.csv', 'a') as f:
                                f.write(str(line) + '\n')
                                self.project_error_number += 1

                        else:
                            poj = projectInfo_domain_query.filter_by(name=line[0], address=line[4]).first()
                            if projects[-1] == project and not poj:
                                logger.info('{0}项目不存在，新增...'.format(line[0]))
                                new_uuid = gen_uuid_for_db()
                                new_uuid = judge_uuid(new_uuid, projectInfo_domain_query)
                                project_info = db_projectInfo(
                                    uuid=new_uuid,
                                    name=line[0][:20],
                                    createAt=datetime.datetime.now().date(),
                                    createBy=CREATE_BY,
                                    address=line[4],
                                    latitude=line[5]['latitude'],
                                    longitude=line[5]['longitude'],
                                    province=line[1],
                                    city=line[2],
                                    country=line[3],
                                )
                                db_session.add(project_info)
                                db_session.commit()
                                self.project_insert_number += 1
                            else:
                                continue

                elif not projects:
                    logger.info('{0}项目不存在，新增...'.format(line[0]))
                    new_uuid = gen_uuid_for_db()
                    new_uuid = judge_uuid(new_uuid, projectInfo_domain_query)
                    project_info = db_projectInfo(
                        uuid=new_uuid,
                        name=line[0][:20],
                        createAt=datetime.datetime.now().date(),
                        createBy=CREATE_BY,
                        address=line[4],
                        latitude=line[5]['latitude'],
                        longitude=line[5]['longitude'],
                        province=line[1],
                        city=line[2],
                        country=line[3],
                    )
                    db_session.add(project_info)
                    db_session.commit()
                    self.project_insert_number += 1

                else:
                    logger.warning('项目{0}已存在,更新信息'.format(line[0]))
                    projects[0].name = line[0][:20]
                    projects[0].createAt = datetime.datetime.now().date()
                    projects[0].createBy = CREATE_BY
                    projects[0].address = line[4]
                    projects[0].latitude = line[5]['latitude']
                    projects[0].longitude = line[5]['longitude']
                    projects[0].province = line[1]
                    projects[0].country = line[3]

                    db_session.commit()
                    self.project_update_number += 1
            except TypeError:
                logger.error('{}数据库查询出错'.format(line[0]))

    def create_elevator_info(self, file_name):
        """
        :param:根据注册代码判断电梯是否存在，存在则进行信息匹对，相同则更新。不存在则根据项目名获得唯一id，创建新的电梯信息。此处要操
        作多张表（ev_info ...）

        :return: 不返回值

        """

        for line in ReadExcle().handle_evinfo_data(file_name):

            project_id = projectInfo_domain_query.filter_by(name=line[0][:20], address=line[17]).first()  # 项目名字查询数据库是否存在

            ev_info = db_ev_query.filter_by(regCode=line[4]).first()  # 注册代码查询数据库中是否存在 不严谨需要增加条件

            if not project_id:
                logger.error('{0}项目不存在，请重新核对，添加项目'.format(line[0]))
                with open('项目不存在.csv', 'a') as f:
                    f.write(str(line) + '\n')
                continue
            else:

                if not line[4]:  # 注册代码为空的处理方法
                    logger.warning('由于注册代码为空，直接创建电梯信息')
                    ev_id = db_ev_query.filter_by(projectId=project_id.uuid, evOrder=line[1]).first()
                    if ev_id:
                        ev_id.brandId = line[2]
                        ev_id.useFor = usefor[line[3]]
                        ev_id.type = ev_type_map[line[3]]
                        ev_id.deviceNumber = ''
                        ev_id.manufacturer = line[6]
                        ev_id.productionDate = line[7]
                        ev_info.productionNumber = line[8]
                        ev_id.modelNumber = line[9]
                        ev_id.evOrder = line[1]
                        ev_id.createAt = datetime.datetime.now().date(),
                        ev_id.createBy = CREATE_BY
                        ev_id.userLock = 0

                        type_id = line[3]
                        info_save(line, type_id, ev_id.uuid)
                        self.reagecode_none_update += 1
                        ceate_maintenance(line, self.weibao_name, ev_id.uuid)  # 绑定维保单位
                    else:
                        new_uuid = gen_uuid_for_db()  # 生成电梯信息表的uuid
                        new_uuid = judge_uuid(new_uuid, db_ev_query)  # 判断uuid是否存在
                        ev_info_save(line, new_uuid, project_id)

                        self.reagecode_none_insert += 1
                        ceate_maintenance(line, self.weibao_name, new_uuid)
                        type_id = line[3]
                        info_save(line, type_id, new_uuid)  # 根据电梯类型直梯表、扶梯表等插入数据 由于注册代码为空暂时放弃更改

                elif ev_info:
                    logger.warning('{0}注册代码已存在,进一步鉴别{1}'.format(line[4], line[0]))
                    if ev_info.projectId == project_id.uuid:
                        logger.info('{0}注册代码和数据库中信息一致，信息更新 {1}'.format(line[4], line[0]))
                        ev_info.projectId = project_id.uuid
                        ev_info.useFor = usefor[line[3]]
                        ev_info.type = ev_type_map[line[3]]
                        ev_info.deviceNumber = ''
                        ev_info.manufacturer = line[6]
                        ev_info.productionDate = line[7]
                        ev_info.productionNumber = line[8]
                        ev_info.modelNumber = line[9]
                        ev_info.evOrder = line[1]
                        ev_info.createAt = datetime.datetime.now().date()
                        ev_info.createBy = CREATE_BY
                        ev_info.status = 1
                        ev_info.userLock = 0

                        db_session.commit()
                        type_id = line[3]
                        ev_uuid = ev_info.uuid
                        info_save(line, type_id, ev_uuid)  # 电梯注册代码存在，传入电梯表uuid
                        self.elevator_update_number += 1
                        ceate_maintenance(line, self.weibao_name, ev_uuid)
                    elif ev_info.productionNumber == line[8]:
                        ev_info.projectId = project_id.uuid
                        ev_info.useFor = usefor[line[3]]
                        ev_info.type = ev_type_map[line[3]]
                        ev_info.deviceNumber = ''
                        ev_info.manufacturer = line[6]
                        ev_info.productionDate = line[7]
                        ev_info.productionNumber = line[8]
                        ev_info.modelNumber = line[9]
                        ev_info.evOrder = line[1]
                        ev_info.createAt = datetime.datetime.now().date()
                        ev_info.createBy = CREATE_BY
                        ev_info.status = 1
                        ev_info.userLock = 0

                        db_session.commit()
                        type_id = line[3]
                        ev_uuid = ev_info.uuid
                        info_save(line, type_id, ev_uuid)  # 电梯注册代码存在，传入电梯表uuid
                        self.elevator_update_number += 1
                        ceate_maintenance(line, self.weibao_name, ev_uuid)

                    else:
                        logger.error('{0}注册代码与其他电梯注册代码冲突,在错误文件中查看项目{1}'.format(line[4], line[0]))
                        with open('错误数据.csv', 'a') as f:
                                f.write(str(line) + '\n')

                else:
                    new_uuid = gen_uuid_for_db()  # 生成电梯信息表的uuid
                    new_uuid = judge_uuid(new_uuid, db_ev_query)  # 判断uuid是否存在
                    logger.info('项目{0}注册代码{1}的电梯信息不存在，新增'.format(line[0], line[4]))
                    ev_info_save(line, new_uuid, project_id)

                    type_id = line[3]
                    info_save(line, type_id, new_uuid)
                    self.elevator_insert_number += 1
                    ceate_maintenance(line, self.weibao_name, new_uuid)


if __name__ == '__main__':

    company_list = [
        '达州市富菱电梯工程有限公司'
    ]
    for i in company_list:
        info = DataToDb(i)
        # print('{0}的项目开始导入。。。。'.format(i))
        # info.create_project('csv文件/{0}/项目上传文件.csv'.format(i))
        # logger.info('项目信息导入完成，新增项目{0}条，更新项目{1}条'.format(info.project_insert_number, info.project_update_number))

        # time.sleep(5)
        logger.info('{0}的电梯开始导入。。。。'.format(i))
        info.create_elevator_info('csv文件/电梯导入模板文件.csv')
        logger.info('电梯导入完成，新增了{0}条，更新了{1}条'.format(info.elevator_insert_number, info.elevator_update_number))
        logger.info('注册代码为空的电梯新增{0}台，更新{1}台'.format(info.reagecode_none_insert, info.reagecode_none_insert))

