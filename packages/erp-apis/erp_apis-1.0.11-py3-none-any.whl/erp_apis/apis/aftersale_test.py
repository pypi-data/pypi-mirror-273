# coding: utf-8
# Project：erp_out_of_stock
# File：test.py
# Author：李福成
# Date ：2024-04-28 18:24
# IDE：PyCharm
from json import dumps

from afterSales import aftersaleList, unconfirms, save, aftersaleCommon, confirmReturnQty, confirmGoods
from apis.user import login
from refund import refundListByafterId, unfinish, finish, confirm
from erp_apis.erpRequest import Session

def get_after_sale_order(code):
    resp = session.erp321Send(aftersaleList(
        queryData=[
            # 退回快递单号
            {"k": "l_id", "v": code, "c": "@="}
        ],
        page_size=5,
    )).json()['ReturnValue']['datas']
    after_sale_order = None if resp == [] else resp[0]
    if after_sale_order is None:
        resp = session.erp321Send(aftersaleList(
            queryData=[
                # 原快递单号
                {"k": "order_l_id", "v": code, "c": "@="}
            ],
            page_size=5,
        )).json()['ReturnValue']['datas']
        after_sale_order = None if resp == [] else resp[0]
    print(after_sale_order)
    return after_sale_order


def get_refund_order(as_id):
    resp = session.erp321Send(refundListByafterId(
        queryData=[
            {"k": "as_id", "v": as_id, "c": "@="}
        ]
    )).json()['ReturnValue']['datas']
    return None if resp == [] else resp[0]


def unfinish_refund(pay_id):
    session.erp321Send(unfinish(
        queryData=[pay_id]
    ))


def finish_refund(pay_id):
    session.erp321Send(finish(
        queryData=[pay_id]
    ))


def unconfirm_aftersale(id):
    session.erp321Send(unconfirms(id))


def is_confirmed(order):
    status = order.get("status")
    if status is None:
        return False
    if status == "已确认":
        return True
    return False


# 判断实退数量不为0
def is_over_0_r_qty(order):
    r_qty = int(order.get('r_qty'))
    if r_qty is None:
        return False
    if r_qty >= 1:
        return True
    return False


# 判断货物状态是否为 卖家已收到退货
def is_received(order):
    good_status = order.get('good_status')
    if good_status is None:
        return False
    if good_status == '卖家已收到货':
        return True
    return False


def update_after_type(code):
    to_update = get_after_sale_order(code)
    if to_update.get("shop_type") == "仅退款":
        to_update["id"] = ""
        to_update["type"] = "普通退货"
        session.erp321Send(save(dumps(to_update)))


def confirm_after(as_id):
    session.erp321Send(aftersaleCommon(as_id))


def confirm_refund(pay_id):
    session.erp321Send(confirm(pay_id))


def confirm_refund_qty_and_goods_by_as_id(as_id):
    session.erp321Send(confirmReturnQty(as_id))
    session.erp321Send(confirmGoods(as_id))


if __name__ == '__main__':
    session = Session()
    session.erpSend(login(
        username="17671271393",
        password="Wh1761393@"
    ))

    code = '776389719299358'

    # 根据 退回快递单号 和 原快递单号 搜索售后单
    after_sale_order = get_after_sale_order(code)

    # if after_sale_order is None:
    #     # 创建无信息件，填写快递单号
    #     create_empty()
    #
    # # 确认编码一致
    # confirm_code()

    # 不处理订单状态为 已确认
    if not is_confirmed(after_sale_order):
        pass
    # 不处理 货物状态 为 卖家已收到退货
    if not is_received(after_sale_order):
        pass
    # 不处理 实退数量 不为 0
    if not is_over_0_r_qty(after_sale_order):
        pass

    # 根据售后单id获取退款单
    refund_order = get_refund_order(after_sale_order.get("id"))

    # 根据 内部退款号 取消退款完成
    unfinish_refund(refund_order.get("pay_id"))

    # 反确认售后单
    unconfirm_aftersale(after_sale_order.get("id"))

    # 如果线上类型为 仅退款 ,修改售后类型为 普通退货
    update_after_type(code)

    # 确认售后单
    confirm_after(after_sale_order.get("id"))

    # 重新根据售后单id获取退款单
    refund_order = get_refund_order(after_sale_order.get("id"))

    # 确认退款单
    confirm_refund(refund_order.get("pay_id"))

    # 退款完成
    finish_refund(refund_order.get("pay_id"))

    # 确认收到货物
    confirm_refund_qty_and_goods_by_as_id(after_sale_order.get("id"))
