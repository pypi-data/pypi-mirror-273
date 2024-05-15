# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  qlvClient
# FileName:     config.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/17
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""

failed_code = {
    "10000": {"code": 10000, "describe": "未知原因"},
    "10001": {"code": 10001, "describe": "页面元素未找到"},
    "10002": {"code": 10002, "describe": "航班官方变价"},
    "10003": {"code": 10003, "describe": "乘客重复下单"},
    "10004": {"code": 10004, "describe": "添加乘客后点击下一步出现未知弹框"},
    "10005": {"code": 10005, "describe": "本地订单重复入库导致主键冲突"},
    "10006": {"code": 10006, "describe": "未成年人出行弹出提示框"},
    "10007": {"code": 10007, "describe": "api接口获取订单状态已取消"},
    "10008": {"code": 10008, "describe": "创建订单失败，请重试或拨打携程客服电，电话(95010)预订"},
    "10009": {"code": 10009, "describe": "您预订的航班机票已售完，请重新查询预订"}
}

qvl_map = {
    "user_id": 186,
    "user_key": "9a68295ec90b1fc10ab94331c882bab9",
    "domain": "outsideapi.qlv88.com",
    "protocol": "http",
    "interfaces": {
        "lock_order": {
            "path": "/LockOrder.ashx",
            "method": "post"
        },
        "unlock_order": {
            "path": "/OrderUnlock.ashx",
            "method": "post"
        },
        "write_order_log_new": {
            "path": "/OrderLogWriteNew.ashx",
            "method": "post"},
        "save_order_pay_info": {
            "path": "/OrderPayInfoSave.ashx",
            "method": "post"},
        "fill_order_itinerary_info": {
            "path": "/BackfillTicketNumberNew.ashx",
            "method": "post"
        }
    }
}
