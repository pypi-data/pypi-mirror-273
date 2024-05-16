# coding: utf-8
# Project：erp_out_of_stock
# File：test.py
# Author：李福成
# Date ：2024-04-28 18:24
# IDE：PyCharm
from json import dumps

from apis.inventory import WmsSkuStock
from apis.order import OrderList, ChangeBatchItems, LogisticsInfo
from erp_apis.apis.user import login
from apis.afterSales import aftersaleList, aftersaleCommon, clearException, unconfirms, save
from erp_apis.apis.goods import ItemList

from apis.refund import refundListByafterId
from erpRequest import Session


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


def get_refund_order(code):
    resp = session.erp321Send(refundListByafterId(
        queryData=[
            {"k": "as_id", "v": code, "c": "@="}
        ]
    )).json()['ReturnValue']['datas']
    return None if resp == [] else resp[0]


def cancel_refund_confirm(id):
    session.erp321Send(cancelRefundConfirm(
        queryData=[id]
    ))


def unconfirm_aftersale(id):
    session.erp321Send(unconfirms(id))


def update_type(order):
    order["id"] = ""
    order["type"] = "普通退货"
    dump_str = dumps(order)
    session.erp321Send(save(dump_str))


if __name__ == '__main__':
    session = Session()
    session.erpSend(login(
        username="17671271393",
        password="Wh1761393@"
    ))

    # search = get_after_sale_order(code='78795429301452')
    # search = after.search(code='')
    # is_confirmed(search)
    # get_refund_order(search)
    # print(search)
    # as_id = search.get('id')
    # refund_order = get_refund_order(as_id)

    # pay_id = str(refund_order.get('pay_id'))
    # cancel_refund_confirm(pay_id)
    # unconfirm_aftersale(as_id)
    unconfirmed_after_sale_order = get_after_sale_order(code='78795429301452')

    update_type(unconfirmed_after_sale_order)
