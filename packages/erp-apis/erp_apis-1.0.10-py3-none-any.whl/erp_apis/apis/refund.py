from typing import Optional, Union
from erp_apis.erpRequest import Request
from erp_apis.utils.util import dumps, getDefaultParams, JTable1, generateChangeBatchItems


def RefundRequest(data: dict, method: str = 'LoadDataToJSON',
                 url: str = '/app/order/refund/refund.aspx', **kwargs) -> Request:
    params = getDefaultParams({'defaultParams': ["ts___"], 'am___': method})
    if kwargs.get('params'):
        params.update(kwargs.get('params'))
    return Request(
        method='POST',
        url=url,
        params=params,
        data={
            **data
        },
        callback=JTable1
    )


# 根据售后单号查询退款单
def refundListByafterId(queryData: Optional[list] = None, page_num: int = 1, page_size: int = 500):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return RefundRequest({
        '_jt_page_size': page_size,
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "LoadDataToJSON",
                "Args": [
                    page_num,
                    dumps(queryData),
                    "{}"
                ]
            }
        ),
    },
        method='LoadDataToJSON'
    )


# 取消退款完成
def cancelRefundConfirm(queryData: Optional[list] = None):
    '''
    获取订单
    :param page_num: 页数
    :param page_size:  每页条数
    :param queryData:  查询条件
    :return: 查询结果
    '''
    if queryData is None: queryData = []
    return RefundRequest({
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "UnFinishs",
                "Args": queryData,
                "CallControl": "{page}"
            }
        ),
    },
        method='UnFinishs'
    )
