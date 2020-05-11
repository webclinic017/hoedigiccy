"""
Atop Trade module.
https://github.com/ATOP-api/api-docs/blob/master/

Author: RedHoe
Date:   2020/05/05
Email:  lamusxiao@qq.com
"""
import urllib
import requests
import time
import base64
import hashlib
import hmac
from urllib import parse
import urllib.parse
import json
from urllib.parse import urljoin
from hoedigiccy.utils.web import AsyncHttpRequests

__all__ = ("AtopRestAPI", )

class AtopRestAPI:
    """Atop REST API client.

    Attributes:
        access_key: Account's ACCESS KEY.
        secret_key: Account's SECRET KEY.
        host: HTTP request host, default `https://api.a.top`.
    """

    def __init__(self, access_key, secret_key, host=None):
        """Initialize REST API client."""
        self._host = host or "https://api.a.top"
        self._access_key = access_key
        self._secret_key = secret_key
        self._account_id = None
    
    async def get_server_time(self):
        """获取服务器时间
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/trade/api/v1/getServerTime"
        success, error = await self.request("GET", uri)
        return success, error
    
    async def get_kline(self, market,typeKline,since='0'):
        """获取K线数据 Get latest trade information.

        Args:
            market: market name, e.g. `eth_usdt`.
            "type":"1min",1min,5min,15min,30min,1hour,6hour,1day,7day,30day
            "since":0  第一次为0,之后为响应的since的值即可
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/data/api/v1/getKLine"
        params = {
            "market": market,
            "type": typeKline,
            "since":since
        }
        success, error = await self.request("GET", uri, body=params, auth=True)
        return success, error
    
    async def get_market_config(self):
        """获取市场配置数据.
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/data/api/v1/getMarketConfig"
        params = {
        }
        success, error = await self.request("GET", uri)
        return success, error

    async def get_depth(self, market):
        """获取市场挂买挂卖深度数据 Get latest trade information.

        Args:
            symbol: Symbol name, e.g. `eth_usdt`.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/data/api/v1/getDepth"
        params = {
            "market": market
        }
        success, error = await self.request("GET", uri, body=params, auth=True)
        return success, error

    async def get_trades(self, market):
        """获取市场最近成交数据 Get latest trade information.

        Args:
            symbol: Symbol name, e.g. `eth_usdt`.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/data/api/v1/getTrades"
        params = {
            "market": market
        }
        success, error = await self.request("GET", uri, body=params, auth=True)
        return success, error
    
    async def get_balance(self):
        """获取账户资产 Get latest trade information.
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/trade/api/v1/getBalance"
        params = {}
        success, error = await self.request("GET", uri)
        return success, error

    async def get_open_orders(self,market,page,pagesize):
        """获取未完成订单（市场，页码，每页数量）
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/trade/api/v1/getOpenOrders"
        params = {
            "market": market,
            "page":page,
            "pageSize":pagesize
        }
        success, error = await self.request("GET", uri, body=params, auth=True)
        return success, error
    
    async def cancel(self,market,orderId):
        """撤单（orderId）
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/trade/api/v1/cancel"
        params = {
            "market": market,
            "id":orderId
        }
        success, error = await self.request("POST", uri, body=params, auth=True)
        return success, error

    async def batch_cancel(self,market,orderIdList):
        """ 批量撤单（datalist）
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        uri = "/trade/api/v1/batchCancel"
        params = {
            "market": market,
            "data":reList2StrBase64(orderIdList)
        }
        success, error = await self.request("POST", uri, body=params, auth=True)
        return success, error
    
    async def create_order(self, market, price, quantity, order_type, entrustType='0',client_order_id=None):
        ''' 创建委托单
        Args:
            symbol: Symbol name, e.g. `eth_usdt`.
            price: price e.g. '0.2653'
            quantity: number e.g. '100'
            order_type: 0:sell  1:buy
            entrustType: 0:limit 1:market
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        '''
        uri = "/trade/api/v1/order"
        info = {
            "market":market,
            "price":price,
            "number":quantity,
            "type":order_type,
            "entrustType":entrustType
        }
        success, error = await self.request("POST", uri, body=info, auth=True)
        return success, error

    async def batch_order(self, market, batchList):
        ''' 批量创建委托单
        Args:
            symbol: Symbol name, e.g. `eth_usdt`.
            price: price e.g. '0.2653'
            quantity: number e.g. '100'
            order_type: 0:sell  1:buy
            entrustType: 0:limit 1:market
        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        '''
        uri = "/trade/api/v1/batchOrder"
        info = {
            "market":market,
            "data":reList2StrBase64(batchList)
        }
        success, error = await self.request("POST", uri, body=info, auth=True)
        return success, error
    
    
    async def request(self, method, uri, params=None, body=None, auth=False):
        """Do HTTP request.
        Args:
            method: HTTP request method. `GET` / `POST` / `DELETE` / `PUT`.
            uri: HTTP request uri.
            params: HTTP query params.
            body:   HTTP request body.
            auth: If this request requires authentication.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        url = urljoin(self._host, uri)
        if auth:
            params = params if params else {}
            params.update({"accesskey": self._access_key,
                           "nonce": str(int(time.time()*1000))})
            for k,v in body.items():
                params[k] = str(v)
            host_name = urllib.parse.urlparse(self._host).hostname.lower()
            params["signature"] = create_signature(self._secret_key,params)
            # print(params)

        if method == "GET":
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/39.0.2171.71 Safari/537.36"
            }
        else:
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json"
            }
        _, success, error = await AsyncHttpRequests.fetch(method, url, params=params, data=body, headers=headers,
                                                          timeout=10)
        if error:
            return success, error
        if not isinstance(success, dict):
            success = json.loads(success)
        return success, None

# 参数验签方法
def create_signature(secret_key,info):
    ret = {
        "code": 0,
        "message": "create_signature success"
    }
    if secret_key is None or secret_key == "":
        ret["code"] = -1
        ret["message"] = "API key and secret key are required"
        return ret
    # 对参数进行排序 并加入&:
    qs0 = map_str(info)
    # print("qs0:",qs0)
    # 拼接好的字符串进行 哈希加密
    dig = hmac.new(secret_key.encode('utf-8'), bytes(qs0, encoding='utf-8'), digestmod=hashlib.sha256).digest()
    # print("dig:", dig)
    s = dig.hex()
    # print("s:", s)
    return s
# map 用&凭接为字符串
def map_str(inmap):
    keys = sorted(inmap.keys())
    qs0 = '&'.join(['%s=%s' % (key, parse.quote(str(inmap[key]), safe='')) for key in keys])
    return qs0
# lsit/dict base64编码
def reList2StrBase64(inlistOrdict):
    list2str = str(inlistOrdict)
    str2bytes = bytes(list2str, encoding = "utf8")
    str_encodes = str(base64.b64encode(str2bytes), encoding="utf-8")
    return str_encodes