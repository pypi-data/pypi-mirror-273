# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  qlvClient
# FileName:     proxy.py
# Description:  TODO
# Author:       GIGABYTE
# CreateDate:   2024/04/17
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import typing as t

from qlv_client.utils import logger
from qlv_client.api import OrderService
from qlv_client.repository import QlvConfigRepository


class QlvService(object):

    @classmethod
    def get_lock_order(cls, lock_order_params: dict) -> t.Dict:
        logger.info("根据政策匹配，开始获取劲旅系统被锁定的订单...")
        kwargs = QlvConfigRepository.get_request_base_params(inter_name="lock_order")
        kwargs.update(lock_order_params)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.lock_order(**kwargs)
        result["policy_args"] = lock_order_params
        result["data_info"] = result.pop("datainfojson", None)
        return result

    @classmethod
    def set_unlock_order(cls, order_id: int, oper: str, order_state: str, order_lose_type: str, remark: str) -> bool:
        logger.info("出票{}，开始解锁劲旅平台订单<{}>".format("成功" if order_state == "1" else "失败", order_id))
        kwargs = QlvConfigRepository.get_request_base_params(inter_name="unlock_order")
        unlock_order_params = QlvConfigRepository.get_unlock_order_params(
            order_id=order_id, oper=oper, order_state=order_state, order_lose_type=order_lose_type, remark=remark
        )
        kwargs.update(unlock_order_params)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.unlock_order(**kwargs)
        if result.get("code") == 1:
            logger.info("劲旅平台订单<{}>解锁成功.".format(order_id))
            return True
        else:
            message = result.get("message")
            if "解锁失败" in message:
                # 说明订单是未锁定状态
                return True
            else:
                logger.error(result)
                return False

    @classmethod
    def unlock_reason_with_flag(cls, flag: bool, order_id: int, oper: str, remark: str) -> bool:
        unlock_reason_params = QlvConfigRepository.get_unlock_reason_params(
            flag=flag, order_id=order_id, oper=oper, remark=remark
        )
        return cls.set_unlock_order(**unlock_reason_params)

    @classmethod
    def loop_unlock_reason_with_flag(cls, flag: bool, order_id: int, oper: str, remark: str, attempts: int = 3):
        # 尝试3次解锁
        for i in range(attempts):
            is_succeed = QlvService.unlock_reason_with_flag(flag=flag, order_id=order_id, oper=oper, remark=remark)
            if is_succeed is True:
                break

    @classmethod
    def set_system_unlock_order(cls, order_id: int, flag: bool, oper: str, remark: str) -> bool:
        if flag is True:
            order_state = "1"
        else:
            order_state = "0"
        return cls.set_unlock_order(
            order_id=order_id, oper=oper, order_state=order_state, order_lose_type="系统", remark=remark
        )

    @classmethod
    def loop_set_unlock_order(cls, pre_order_id: int, flag: bool, oper: str, remark: str, attempts: int = 3) -> bool:
        is_success = False
        for _ in range(attempts):
            is_success = cls.set_system_unlock_order(order_id=pre_order_id, flag=flag, oper=oper, remark=remark)
            if is_success is True:
                break
        return is_success

    @classmethod
    def save_pay_info(cls, **kwargs) -> bool:
        logger.info("开始向劲旅系统回填采购信息...")
        args = QlvConfigRepository.get_request_base_params(inter_name="save_order_pay_info")
        order_pay_info = QlvConfigRepository.get_order_pay_info(**kwargs)
        args.update(order_pay_info)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.save_order_pay_info(**args)
        if result.get("code") == 0:
            message = result.get("message") or ''
            if "支付保存" in message:
                # 说名已经出票完成，再回填票号信息，就成了改签
                return True
            elif "重复数据" in message:
                # 说名已经填过了
                return True
            else:
                logger.error(result)
                return False
        else:
            logger.error("向劲旅系统回填采购信息成功.")
            return True

    @classmethod
    def save_payment_info(cls, **kwargs) -> bool:
        logger.info("开始向劲旅系统回填采购信息...")
        args = QlvConfigRepository.get_request_base_params(inter_name="save_order_pay_info")
        order_pay_info = QlvConfigRepository.get_order_pay_info(**kwargs)
        args.update(order_pay_info)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.save_order_pay_info(**args)
        if result.get("code") == 0:
            message = result.get("message") or ''
            if "支付保存" in message:
                # 说名已经出票完成，再回填票号信息，就成了改签
                return True
            elif "重复数据" in message:
                # 说名已经填过了
                return True
            else:
                logger.error(result)
                return False
        else:
            logger.error("向劲旅系统回填采购信息成功.")
            return True

    @classmethod
    def loop_save_payment_info(cls, payment_info: dict, attempts: int = 3) -> bool:
        flag = False
        for _ in range(attempts):
            flag = cls.save_payment_info(**payment_info)
            if flag is True:
                break
        return flag

    @classmethod
    def save_itinerary_info(cls, **kwargs) -> bool:
        logger.info("开始向劲旅系统回填票号信息...")
        args = QlvConfigRepository.get_request_base_params(inter_name="fill_order_itinerary_info")
        order_itinerary_info = QlvConfigRepository.get_order_itinerary_info(**kwargs)
        args.update(order_itinerary_info)
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.fill_order_itinerary_info(**args)
        if result.get("code") == 0:
            message = result.get("message") or ''
            if "票号保存" in message:
                # 说名已经出票完成，再回填票号信息，就成了改签
                return True
            elif "重复数据" in message:
                # 说名已经填过了
                return True
            else:
                logger.error(result)
                return False
        else:
            logger.warning("向劲旅系统回填票号信息成功.")
            return True

    @classmethod
    def save_itinerary_info_by_batch_itinerary(cls, pre_order_id: int, oper: str, itinerary_info: list) -> bool:
        logger.info("开始向劲旅系统回填票号信息...")
        args = QlvConfigRepository.get_request_base_params(inter_name="fill_order_itinerary_info")
        ticket_infos = list()
        for info in itinerary_info:
            passenger = info.get("passenger")
            card_id = info.get("card_id")
            itinerary_id = info.get("itinerary_id")
            if itinerary_id:
                departure_city = info.get("departure_city")
                arrive_city = info.get("arrive_city")
                val: str = "#".join([passenger, card_id, itinerary_id, departure_city, arrive_city])
                ticket_infos.append(val)
        if ticket_infos:
            order_itinerary_info = {
                "order_id": pre_order_id,
                "oper": oper,
                "ticket_infos": ";".join(ticket_infos)
            }
            args.update(order_itinerary_info)
            order_ser = OrderService(**QlvConfigRepository.get_host_params())
            result = order_ser.fill_order_itinerary_info(**args)
            if result.get("code") == 0:
                message = result.get("message") or ''
                if "票号保存" in message:
                    # 说名已经出票完成，再回填票号信息，就成了改签
                    return True
                elif "重复数据" in message:
                    # 说名已经填过了
                    return True
                else:
                    logger.error(result)
                    return False
            else:
                logger.warning("向劲旅系统回填票号信息成功.")
                return True
        else:
            return False

    @classmethod
    def loop_save_itinerary_info(cls, pre_order_id: int, itinerary_info: list, oper: str, attempts: int = 3) -> bool:
        flag = False
        for _ in range(attempts):
            flag = cls.save_itinerary_info_by_batch_itinerary(
                pre_order_id=pre_order_id, oper=oper, itinerary_info=itinerary_info

            )
            if flag is True:
                break
        return flag

    @classmethod
    def save_new_log(cls, pre_order_id: int, oper: str, logs: str) -> bool:
        logger.info("开始向劲旅系统给订单<{}>记录新日志...".format(pre_order_id))
        args = QlvConfigRepository.get_request_base_params(inter_name="write_order_log_new")
        args.update(dict(order_id=pre_order_id, oper=oper, logs=logs))
        order_ser = OrderService(**QlvConfigRepository.get_host_params())
        result = order_ser.write_order_log_new(**args)
        if result.get("code") == 0:
            logger.error("向劲旅系统给订单<{}>记录新日志失败...".format(pre_order_id))
            return False
        else:
            logger.info("向劲旅系统给订单<{}>记录新日志成功.".format(pre_order_id))
            return True

    @classmethod
    def loop_save_order_new_log(cls, pre_order_id: int, logs: str, oper: str, attempts: int = 3) -> bool:
        flag = False
        for _ in range(attempts):
            flag = cls.save_new_log(pre_order_id=pre_order_id, logs=logs, oper=oper)
            if flag is True:
                break
        return flag
