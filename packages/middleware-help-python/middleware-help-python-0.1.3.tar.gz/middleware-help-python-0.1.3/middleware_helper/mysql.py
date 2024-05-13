# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  middleware-help-python
# FileName:     mysql.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
from mysql.connector import connect
from middleware_helper.libs import logger
from mysql.connector.cursor_cext import CMySQLCursor
from middleware_helper.network import filter_system_port_list


class Mysql(object):

    def __init__(self, **mysql_params_map):
        self.host = mysql_params_map.get('host') or '127.0.0.1'
        self.port = mysql_params_map.get("port") or '3306'
        self.user = mysql_params_map.get("user") or 'root'
        self.password = mysql_params_map.get("password") or 'Admin@123'
        self.database = mysql_params_map.get("database") or 'mysql'
        self.charset = mysql_params_map.get("charset") or 'utf8'
        self.conn = self.retry_connection()

    def __connect_to_mysql(self) -> connect:
        try:
            if isinstance(self.port, list):
                __port = filter_system_port_list(data_port=self.port, default_port=3306)
            else:
                __port = self.port
            # 建立连接
            conn = connect(
                host=self.host,
                user=self.user,
                port=__port,
                charset=self.charset,
                password=self.password,
                database=self.database
            )
            return conn
        except Exception as e:
            logger.error(e)
            return None

    def retry_connection(self) -> connect:
        conn = self.__connect_to_mysql()
        i = 0
        while conn is None or not conn.is_connected():
            if i > 9:
                logger.warning("尝试连接数据库10次以上，最终未能成功")
                break
            else:
                if i > 0:
                    logger.warning("尝试重连数据库...")
                    time.sleep(1)
                conn = self.__connect_to_mysql()
            i = i + 1
        return conn

    @classmethod
    def convert_tuple_to_dict(cls, records: list, column_names: tuple) -> list:
        # 将元组列表转换为字典列表
        result_list = []
        for row in records:
            row_dict = {}
            for index, value in enumerate(row):
                column_name = column_names[index]
                row_dict[column_name] = value
            result_list.append(row_dict)
        return result_list

    @classmethod
    def cursor_query_data(cls, cursor: CMySQLCursor, sql: str) -> list:
        # 执行 SQL 查询语句
        cursor.execute(sql)
        # 获取查询结果
        records = cursor.fetchall()
        # 获取列名
        column_names = cursor.column_names
        result_list = cls.convert_tuple_to_dict(records=records, column_names=column_names)
        return result_list

    def execute_sql(self, sql: str, action: str, is_need_close: bool = True) -> list:
        results = None
        if self.conn and self.conn.is_connected():
            cursor: CMySQLCursor = self.conn.cursor()
            if action in ("insert", "update", "delete"):
                try:
                    cursor.execute(sql)
                    self.conn.commit()
                except Exception as e:
                    logger.error(e)
                    self.conn.rollback()
            elif action == "select":
                try:
                    # 获取查询结果
                    results = self.cursor_query_data(sql=sql, cursor=cursor)
                except Exception as e:
                    logger.error(e)
            else:
                pass
            if is_need_close is True:
                cursor.close()
                self.conn.close()
        else:
            logger.error("当前连接不正常.")
        return results

    @classmethod
    def convert_key_value_str(cls, **kwargs) -> tuple:
        field_list, value_list = list(), list()
        for key, value in kwargs.items():
            if value is None:
                value = ''
            field_list.append("`{}`".format(key))
            if isinstance(value, str):
                value = "'{}'".format(value)
            else:
                value = str(value)
            value_list.append(value)
        field_str = "(" + ", ".join(field_list) + ")"
        value_str = "(" + ", ".join(value_list) + ")"
        return field_str, value_str

    def insert_order_sql(self, data_info: dict, table_name: str, is_need_close: bool) -> list:
        field_str, value_str = self.convert_key_value_str(**data_info)
        sql = "insert into " + "`{}` {} values {};".format(table_name, field_str, value_str)
        return self.execute_sql(sql=sql, action="insert", is_need_close=is_need_close)
