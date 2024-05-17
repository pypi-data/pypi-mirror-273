import socketio
import json
import requests
import base64
from datetime import datetime
from hashlib import sha256
import csv
from urllib3.exceptions import InsecureRequestWarning
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd
import logging
import functools
import os
import time


CACHE_FILE = "response_cache.json"
CACHE_EXPIRATION = 120  # Cache expiration time in seconds
response_cache = {}

requests.packages.urllib3.util.connection.HAS_IPV6 = False
url = "https://directlink.icicidirect.com/NewSecurityMaster/SecurityMaster.zip"
resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))

logger = logging.getLogger("engineio.client")
logger.propagate = False
logger.setLevel(logging.CRITICAL)


class SocketEventBreeze(socketio.ClientNamespace):

    def __init__(self, namespace, breeze_instance):
        super().__init__(namespace)
        self.breeze = breeze_instance
        self.hostname = "https://uatstreams.icicidirect.com"
        self.sio = socketio.Client()
        # self.sio.on('disconnect', on_trigger)
        self.tokenlist = set()

    def connect(self):
        auth = {
            "user": self.breeze.user_id,
            "token": self.breeze.session_key,
            "appkey": self.breeze.api_key,
        }
        self.sio.connect(
            self.hostname,
            headers={"User-Agent": "python-socketio[client]/socket"},
            auth=auth,
            transports="websocket",
            wait_timeout=50,
        )

    def on_disconnect(self):
        self.sio.emit("disconnect", "transport close")

    def on_trigger(self):
        print("reconnection triggered")

    def on_message(self, data):

        data = self.breeze.parse_data(data)
        if "symbol" in data and data["symbol"] != None and len(data["symbol"]) > 0:
            data.update(self.breeze.get_data_from_stock_token_value(data["symbol"]))
        # print(self.breeze)
        if self.breeze.on_ticks != None:
            self.breeze.on_ticks(data)
        if self.breeze.on_ticks2 != None:
            self.breeze.on_ticks2(data)

    def rewatch(self):
        # print("rewatch",self.values)
        if len(self.tokenlist) > 0:
            self.sio.emit("join", list(self.tokenlist))
            self.sio.on("stock", self.on_message)

    def notify(self):
        self.sio.on("order", self.on_message)

    def watch(self, data, isStrategy=False):
        if isinstance(data, list):
            for entry in data:
                self.tokenlist.add(entry)
        else:
            self.tokenlist.add(data)
        self.sio.emit("join", data)
        self.sio.on("stock", self.on_message)
        self.sio.on("disconnect", self.on_trigger)
        self.sio.on("connect", self.rewatch)

    def unwatch(self, data):
        if isinstance(data, list):
            for entry in data:
                if entry in self.tokenlist:
                    self.tokenlist.discard(entry)
        else:
            if data in self.tokenlist:
                self.tokenlist.discard(data)

        self.sio.emit("leave", data)

    # @sio.on('reconnect')

    # print("I'm connected to the /chat namespace!")


class BreezeConnect:

    def __init__(self, api_key):  # needed for hashing json data
        self.user_id = None
        self.api_key = api_key
        self.session_key = None
        self.secret_key = None

        self.sio_handler = None
        self.api_handler = None
        self.on_ticks = None
        self.on_ticks2 = None
        self.stock_script_dict_list = []
        self.token_script_dict_list = []
        self.tux_to_user_value = {
            "orderFlow": {"B": "Buy", "S": "Sell", "N": "NA"},
            "limitMarketFlag": {"L": "Limit", "M": "Market", "S": "StopLoss"},
            "orderType": {"T": "Day", "I": "IoC", "V": "VTC"},
            "productType": {
                "F": "Futures",
                "O": "Options",
                "P": "FuturePlus",
                "U": "FuturePlus_sltp",
                "I": "OptionPlus",
                "C": "Cash",
                "Y": "eATM",
                "B": "BTST",
                "M": "Margin",
                "T": "MarginPlus",
            },
            "orderStatus": {
                "A": "All",
                "R": "Requested",
                "Q": "Queued",
                "O": "Ordered",
                "P": "Partially Executed",
                "E": "Executed",
                "J": "Rejected",
                "X": "Expired",
                "B": "Partially Executed And Expired",
                "D": "Partially Executed And Cancelled",
                "F": "Freezed",
                "C": "Cancelled",
            },
            "optionType": {"C": "Call", "P": "Put", "*": "Others"},
        }

    def ws_connect(self):
        if not self.sio_handler:
            self.sio_handler = SocketEventBreeze("/", self)
            self.sio_handler.connect()

    def ws_disconnect(self):
        if not self.sio_handler:
            self.sio_handler = SocketEventBreeze("/", self)
        self.sio_handler.on_disconnect()

    def get_data_from_stock_token_value(self, input_stock_token):
        try:
            output_data = {}
            stock_token = input_stock_token.split(".")
            exchange_type, stock_token = stock_token[0], stock_token[1].split("!")[1]
            exchange_code_list = {
                "1": "BSE",
                "4": "NSE",
                "13": "NDX",
                "6": "MCX",
            }
            exchange_code_name = exchange_code_list.get(exchange_type, False)
            if exchange_code_name == False:
                raise Exception(
                    "Stock-Token cannot be found due to wrong exchange-code."
                )
            elif exchange_code_name.lower() == "bse":
                stock_data = self.token_script_dict_list[0].get(stock_token, False)
                if stock_data == False:
                    raise Exception(
                        "Stock-Data does not exist in exchange-code BSE for Stock-Token "
                        + input_stock_token
                        + "."
                    )
            elif exchange_code_name.lower() == "nse":
                stock_data = self.token_script_dict_list[1].get(stock_token, False)
                if stock_data == False:
                    stock_data = self.token_script_dict_list[4].get(stock_token, False)
                    if stock_data == False:
                        raise Exception(
                            "Stock_Token does not exist in both exchange-code i.e. NSE or NFO for Stock-Token "
                            + input_stock_token
                            + "."
                        )
                    else:
                        exchange_code_name = "NFO"
            elif exchange_code_name.lower() == "ndx":
                stock_data = self.token_script_dict_list[2].get(stock_token, False)
                if stock_data == False:
                    raise Exception(
                        "Stock-Data does not exist in exchange-code NDX for Stock-Token "
                        + input_stock_token
                        + "."
                    )
            elif exchange_code_name.lower() == "mcx":
                stock_data = self.token_script_dict_list[3].get(stock_token, False)
                if stock_data == False:
                    raise Exception(
                        "Stock-Data does not exist in exchange-code MCX for Stock-Token "
                        + input_stock_token
                        + "."
                    )
            output_data["stock_name"] = stock_data[1]
            if exchange_code_name.lower() not in ["nse", "bse"]:
                product_type = stock_data[0].split("-")[0]
                if product_type.lower() == "fut":
                    output_data["product_type"] = "Futures"
                if product_type.lower() == "opt":
                    output_data["product_type"] = "Options"
                date_string = ""
                for date in stock_data[0].split("-")[2:5]:
                    date_string += date + "-"
                output_data["expiry_date"] = date_string[:-1]
                if len(stock_data[0].split("-")) > 5:
                    output_data["strike_price"] = stock_data[0].split("-")[5]
                    right = stock_data[0].split("-")[6]
                    if right.upper() == "PE":
                        output_data["right"] = "Put"
                    if right.upper() == "CE":
                        output_data["right"] = "Call"
            return output_data
        except Exception as e:
            return {}

    def get_stock_token_value(
        self,
        exchange_code="",
        stock_code="",
        product_type="",
        expiry_date="",
        strike_price="",
        right="",
        get_exchange_quotes=True,
        get_market_depth=True,
    ):
        if get_exchange_quotes == False and get_market_depth == False:
            raise Exception(
                "Either getExchangeQuotes must be true or getMarketDepth must be true"
            )
        else:
            exchange_code_name = ""
            exchange_code_list = {
                "BSE": "1.",
                "NSE": "4.",
                "NDX": "13.",
                "MCX": "6.",
                "NFO": "4.",
                "BFO": "2.",
            }
            exchange_code_name = exchange_code_list.get(exchange_code, False)
            if exchange_code_name == False:
                raise Exception(
                    "Exchange Code allowed are 'BSE', 'NSE', 'NDX', 'MCX', 'NFO', 'BFO'."
                )
            elif stock_code == "":
                raise Exception("Stock-Code cannot be empty.")
            else:
                token_value = False
                if exchange_code.lower() == "bse":
                    token_value = self.stock_script_dict_list[0].get(stock_code, False)
                elif exchange_code.lower() == "nse":
                    token_value = self.stock_script_dict_list[1].get(stock_code, False)
                else:
                    if expiry_date == "":
                        raise Exception(
                            "Expiry-Date cannot be empty for given Exchange-Code."
                        )
                    if product_type.lower() == "futures":
                        contract_detail_value = "FUT"
                    elif product_type.lower() == "options":
                        contract_detail_value = "OPT"
                    else:
                        raise Exception(
                            "Product-Type should either be Futures or Options for given Exchange-Code."
                        )
                    contract_detail_value = (
                        contract_detail_value + "-" + stock_code + "-" + expiry_date
                    )
                    if product_type.lower() == "options":
                        if strike_price == "":
                            raise Exception(
                                "Strike Price cannot be empty for Product-Type 'Options'."
                            )
                        else:
                            contract_detail_value = (
                                contract_detail_value + "-" + strike_price
                            )
                        if right.lower() == "put":
                            contract_detail_value = contract_detail_value + "-" + "PE"
                        elif right.lower() == "call":
                            contract_detail_value = contract_detail_value + "-" + "CE"
                        else:
                            raise Exception(
                                "Rights should either be Put or Call for Product-Type 'Options'."
                            )
                    if exchange_code.lower() == "ndx":
                        token_value = self.stock_script_dict_list[2].get(
                            contract_detail_value, False
                        )
                    elif exchange_code.lower() == "mcx":
                        token_value = self.stock_script_dict_list[3].get(
                            contract_detail_value, False
                        )
                    elif exchange_code.lower() == "nfo":
                        token_value = self.stock_script_dict_list[4].get(
                            contract_detail_value, False
                        )
                    elif exchange_code.lower() == "bfo":
                        token_value = self.stock_script_dict_list[5].get(
                            contract_detail_value, False
                        )
                if token_value == False:
                    raise Exception("Stock-Code not found.")
                exchange_quotes_token_value = False
                if get_exchange_quotes != False:
                    exchange_quotes_token_value = (
                        exchange_code_name + "1!" + token_value
                    )
                market_depth_token_value = False
                if get_market_depth != False:
                    market_depth_token_value = exchange_code_name + "2!" + token_value
                return exchange_quotes_token_value, market_depth_token_value

    def subscribe_feeds(
        self,
        stock_token="",
        exchange_code="",
        stock_code="",
        product_type="",
        expiry_date="",
        strike_price="",
        right="",
        get_exchange_quotes=True,
        get_market_depth=True,
        get_order_notification=False,
        get_strategy=None,
    ):
        if self.sio_handler:
            return_object = {}
            if get_order_notification == True:
                self.sio_handler.notify()
                return_object = {
                    "message": "Order Notification subscribed successfully"
                }
            if stock_token != "":
                if stock_token != "STRATEGY":
                    self.sio_handler.watch(stock_token, False)
                else:
                    self.sio_handler.watch(stock_token, True)
                return_object = {
                    "message": "Stock " + stock_token + " subscribed successfully"
                }

            elif get_order_notification == True and exchange_code == "":
                return return_object
            else:
                # self.sio_handler.reconnect()
                exchange_quotes_token, market_depth_token = self.get_stock_token_value(
                    exchange_code=exchange_code,
                    stock_code=stock_code,
                    product_type=product_type,
                    expiry_date=expiry_date,
                    strike_price=strike_price,
                    right=right,
                    get_exchange_quotes=get_exchange_quotes,
                    get_market_depth=get_market_depth,
                )
                if exchange_quotes_token != False:
                    self.sio_handler.watch(exchange_quotes_token)
                if market_depth_token != False:
                    self.sio_handler.watch(market_depth_token)
                return_object = {
                    "message": "Stock " + stock_code + " subscribed successfully"
                }
            return return_object

    def unsubscribe_feeds(
        self,
        stock_token="",
        exchange_code="",
        stock_code="",
        product_type="",
        expiry_date="",
        strike_price="",
        right="",
        get_exchange_quotes=True,
        get_market_depth=True,
    ):
        if self.sio_handler:
            if stock_token != "":
                self.sio_handler.unwatch(stock_token)
                return {
                    "message": "Stock " + stock_token + " unsubscribed successfully"
                }
            else:
                exchange_quotes_token, market_depth_token = self.get_stock_token_value(
                    exchange_code=exchange_code,
                    stock_code=stock_code,
                    product_type=product_type,
                    expiry_date=expiry_date,
                    strike_price=strike_price,
                    right=right,
                    get_exchange_quotes=get_exchange_quotes,
                    get_market_depth=get_market_depth,
                )
                if exchange_quotes_token != False:
                    self.sio_handler.unwatch(exchange_quotes_token)
                if market_depth_token != False:
                    self.sio_handler.unwatch(market_depth_token)
                return {"message": "Stock " + stock_code + " unsubscribed successfully"}

    def parse_market_depth(self, data, exchange):
        depth = []
        counter = 0
        for lis in data:
            counter += 1
            dict = {}
            if exchange == "1":
                dict["BestBuyRate-" + str(counter)] = lis[0]
                dict["BestBuyQty-" + str(counter)] = lis[1]
                dict["BestSellRate-" + str(counter)] = lis[2]
                dict["BestSellQty-" + str(counter)] = lis[3]
                depth.append(dict)
            else:
                dict["BestBuyRate-" + str(counter)] = lis[0]
                dict["BestBuyQty-" + str(counter)] = lis[1]
                dict["BuyNoOfOrders-" + str(counter)] = lis[2]
                dict["BuyFlag-" + str(counter)] = lis[3]
                dict["BestSellRate-" + str(counter)] = lis[4]
                dict["BestSellQty-" + str(counter)] = lis[5]
                dict["SellNoOfOrders-" + str(counter)] = lis[6]
                dict["SellFlag-" + str(counter)] = lis[7]
                depth.append(dict)
        return depth

    def parse_data(self, data):
        if (
            data
            and type(data) == list
            and len(data) > 0
            and type(data[0]) == str
            and "!" not in data[0]
            and len(data) == 10
        ):
            iclick_data = dict()
            iclick_data["stock_name"] = data[0]
            iclick_data["stock_description"] = data[1]
            iclick_data["recommended_price_and_date"] = data[2]
            iclick_data["target_price"] = data[3]
            iclick_data["sltp_price"] = data[4]
            iclick_data["part_profit_percentage"] = data[5]
            iclick_data["profit_price"] = data[6]
            iclick_data["exit_price"] = data[7]
            iclick_data["recommended_update"] = data[8]
            iclick_data["iclick_status"] = data[9]
            return iclick_data
        if (
            data
            and type(data) == list
            and len(data) > 0
            and type(data[0]) == str
            and "!" not in data[0]
            and len(data) == 28
        ):
            strategy_dict = dict()
            strategy_dict["strategy_date"] = data[0]
            strategy_dict["modification_date"] = data[1]
            strategy_dict["portfolio_id"] = data[2]
            strategy_dict["call_action"] = data[3]
            strategy_dict["portfolio_name"] = data[4]
            strategy_dict["exchange_code"] = data[5]
            strategy_dict["product_type"] = data[6]
            # strategy_dict['INDEX/STOCK'] = data[7]
            strategy_dict["underlying"] = data[8]
            strategy_dict["expiry_date"] = data[9]
            # strategy_dict['OCR_EXER_TYP'] = data[10]
            strategy_dict["option_type"] = data[11]
            strategy_dict["strike_price"] = data[12]
            strategy_dict["action"] = data[13]
            strategy_dict["recommended_price_from"] = data[14]
            strategy_dict["recommended_price_to"] = data[15]
            strategy_dict["minimum_lot_quantity"] = data[16]
            strategy_dict["last_traded_price"] = data[17]
            strategy_dict["best_bid_price"] = data[18]
            strategy_dict["best_offer_price"] = data[19]
            strategy_dict["last_traded_quantity"] = data[20]
            strategy_dict["target_price"] = data[21]
            strategy_dict["expected_profit_per_lot"] = data[22]
            strategy_dict["stop_loss_price"] = data[23]
            strategy_dict["expected_loss_per_lot"] = data[24]
            strategy_dict["total_margin"] = data[25]
            strategy_dict["leg_no"] = data[26]
            strategy_dict["status"] = data[27]
            return strategy_dict
        elif (
            data
            and type(data) == list
            and len(data) > 0
            and type(data[0]) == str
            and "!" not in data[0]
        ):
            order_dict = {}
            order_dict["sourceNumber"] = data[0]  # Source Number
            order_dict["group"] = data[1]  # Group
            order_dict["userId"] = data[2]  # User_id
            order_dict["key"] = data[3]  # Key
            order_dict["messageLength"] = data[4]  # Message Length
            order_dict["requestType"] = data[5]  # Request Type
            order_dict["messageSequence"] = data[6]  # Message Sequence
            order_dict["messageDate"] = data[7]  # Date
            order_dict["messageTime"] = data[8]  # Time
            order_dict["messageCategory"] = data[9]  # Message Category
            order_dict["messagePriority"] = data[10]  # Priority
            order_dict["messageType"] = data[11]  # Message Type
            order_dict["orderMatchAccount"] = data[12]  # Order Match Account
            order_dict["orderExchangeCode"] = data[13]  # Exchange Code
            if data[11] == "4" or data[11] == "5":
                order_dict["stockCode"] = data[14]  # Stock Code
                order_dict["orderFlow"] = self.tux_to_user_value["orderFlow"].get(
                    str(data[15]).upper(), str(data[15])
                )  # Order Flow
                order_dict["limitMarketFlag"] = self.tux_to_user_value[
                    "limitMarketFlag"
                ].get(
                    str(data[16]).upper(), str(data[16])
                )  # Limit Market Flag
                order_dict["orderType"] = self.tux_to_user_value["orderType"].get(
                    str(data[17]).upper(), str(data[17])
                )  # OrderType
                order_dict["orderLimitRate"] = data[18]  # Limit Rate
                order_dict["productType"] = self.tux_to_user_value["productType"].get(
                    str(data[19]).upper(), str(data[19])
                )  # Product Type
                order_dict["orderStatus"] = self.tux_to_user_value["orderStatus"].get(
                    str(data[20]).upper(), str(data[20])
                )  # Order Status
                order_dict["orderDate"] = data[21]  # Order  Date
                order_dict["orderTradeDate"] = data[22]  # Trade Date
                order_dict["orderReference"] = data[23]  # Order Reference
                order_dict["orderQuantity"] = data[24]  # Order Quantity
                order_dict["openQuantity"] = data[25]  # Open Quantity
                order_dict["orderExecutedQuantity"] = data[
                    26
                ]  # Order Executed Quantity
                order_dict["cancelledQuantity"] = data[27]  # Cancelled Quantity
                order_dict["expiredQuantity"] = data[28]  # Expired Quantity
                order_dict["orderDisclosedQuantity"] = data[
                    29
                ]  # Order Disclosed Quantity
                order_dict["orderStopLossTrigger"] = data[30]  # Order Stop Loss Triger
                order_dict["orderSquareFlag"] = data[31]  # Order Square Flag
                order_dict["orderAmountBlocked"] = data[32]  # Order Amount Blocked
                order_dict["orderPipeId"] = data[33]  # Order PipeId
                order_dict["channel"] = data[34]  # Channel
                order_dict["exchangeSegmentCode"] = data[35]  # Exchange Segment Code
                order_dict["exchangeSegmentSettlement"] = data[
                    36
                ]  # Exchange Segment Settlement
                order_dict["segmentDescription"] = data[37]  # Segment Description
                order_dict["marginSquareOffMode"] = data[38]  # Margin Square Off Mode
                order_dict["orderValidDate"] = data[40]  # Order Valid Date
                order_dict["orderMessageCharacter"] = data[
                    41
                ]  # Order Message Character
                order_dict["averageExecutedRate"] = data[42]  # Average Exited Rate
                order_dict["orderPriceImprovementFlag"] = data[43]  # Order Price Flag
                order_dict["orderMBCFlag"] = data[44]  # Order MBC Flag
                order_dict["orderLimitOffset"] = data[45]  # Order Limit Offset
                order_dict["systemPartnerCode"] = data[46]  # System Partner Code
            elif data[11] == "6" or data[11] == "7":
                order_dict["stockCode"] = data[14]  # stockCode
                order_dict["productType"] = self.tux_to_user_value["productType"].get(
                    str(data[15]).upper(), str(data[15])
                )  # Product Type
                order_dict["optionType"] = self.tux_to_user_value["optionType"].get(
                    str(data[16]).upper(), str(data[16])
                )  # Option Type
                order_dict["exerciseType"] = data[17]  # Exercise Type
                order_dict["strikePrice"] = data[18]  # Strike Price
                order_dict["expiryDate"] = data[19]  # Expiry Date
                order_dict["orderValidDate"] = data[20]  # Order Valid Date
                order_dict["orderFlow"] = self.tux_to_user_value["orderFlow"].get(
                    str(data[21]).upper(), str(data[21])
                )  # Order  Flow
                order_dict["limitMarketFlag"] = self.tux_to_user_value[
                    "limitMarketFlag"
                ].get(
                    str(data[22]).upper(), str(data[22])
                )  # Limit Market Flag
                order_dict["orderType"] = self.tux_to_user_value["orderType"].get(
                    str(data[23]).upper(), str(data[23])
                )  # Order Type
                order_dict["limitRate"] = data[24]  # Limit Rate
                order_dict["orderStatus"] = self.tux_to_user_value["orderStatus"].get(
                    str(data[25]).upper(), str(data[25])
                )  # Order Status
                order_dict["orderReference"] = data[26]  # Order Reference
                order_dict["orderTotalQuantity"] = data[27]  # Order Total Quantity
                order_dict["executedQuantity"] = data[28]  # Executed Quantity
                order_dict["cancelledQuantity"] = data[29]  # Cancelled Quantity
                order_dict["expiredQuantity"] = data[30]  # Expired Quantity
                order_dict["stopLossTrigger"] = data[31]  # Stop Loss Trigger
                order_dict["specialFlag"] = data[32]  # Special Flag
                order_dict["pipeId"] = data[33]  # PipeId
                order_dict["channel"] = data[34]  # Channel
                order_dict["modificationOrCancelFlag"] = data[
                    35
                ]  # Modification or Cancel Flag
                order_dict["tradeDate"] = data[36]  # Trade Date
                order_dict["acknowledgeNumber"] = data[37]  # Acknowledgement Number
                order_dict["stopLossOrderReference"] = data[
                    37
                ]  # Stop Loss Order Reference
                order_dict["totalAmountBlocked"] = data[38]  # Total Amount Blocked
                order_dict["averageExecutedRate"] = data[39]  # Average Executed Rate
                order_dict["cancelFlag"] = data[40]  # Cancel Flag
                order_dict["squareOffMarket"] = data[41]  # SquareOff Market
                order_dict["quickExitFlag"] = data[42]  # Quick Exit Flag
                order_dict["stopValidTillDateFlag"] = data[
                    43
                ]  # Stop Valid till Date Flag
                order_dict["priceImprovementFlag"] = data[44]  # Price Improvement Flag
                order_dict["conversionImprovementFlag"] = data[
                    45
                ]  # Conversion Improvement Flag
                order_dict["trailUpdateCondition"] = data[45]  # Trail Update Condition
                order_dict["systemPartnerCode"] = data[46]  # System Partner Code
            return order_dict
        exchange = str.split(data[0], "!")[0].split(".")[0]
        data_type = str.split(data[0], "!")[0].split(".")[1]
        if exchange == "6":
            data_dict = {}
            data_dict["symbol"] = data[0]
            data_dict["AndiOPVolume"] = data[1]
            data_dict["Reserved"] = data[2]
            data_dict["IndexFlag"] = data[3]
            data_dict["ttq"] = data[4]
            data_dict["last"] = data[5]
            data_dict["ltq"] = data[6]
            data_dict["ltt"] = datetime.fromtimestamp(data[7]).strftime("%c")
            data_dict["AvgTradedPrice"] = data[8]
            data_dict["TotalBuyQnt"] = data[9]
            data_dict["TotalSellQnt"] = data[10]
            data_dict["ReservedStr"] = data[11]
            data_dict["ClosePrice"] = data[12]
            data_dict["OpenPrice"] = data[13]
            data_dict["HighPrice"] = data[14]
            data_dict["LowPrice"] = data[15]
            data_dict["ReservedShort"] = data[16]
            data_dict["CurrOpenInterest"] = data[17]
            data_dict["TotalTrades"] = data[18]
            data_dict["HightestPriceEver"] = data[19]
            data_dict["LowestPriceEver"] = data[20]
            data_dict["TotalTradedValue"] = data[21]
            marketDepthIndex = 0
            for i in range(22, len(data)):
                data_dict["Quantity-" + str(marketDepthIndex)] = data[i][0]
                data_dict["OrderPrice-" + str(marketDepthIndex)] = data[i][1]
                data_dict["TotalOrders-" + str(marketDepthIndex)] = data[i][2]
                data_dict["Reserved-" + str(marketDepthIndex)] = data[i][3]
                data_dict["SellQuantity-" + str(marketDepthIndex)] = data[i][4]
                data_dict["SellOrderPrice-" + str(marketDepthIndex)] = data[i][5]
                data_dict["SellTotalOrders-" + str(marketDepthIndex)] = data[i][6]
                data_dict["SellReserved-" + str(marketDepthIndex)] = data[i][7]
                marketDepthIndex += 1
        elif data_type == "1":
            data_dict = {
                "symbol": data[0],
                "open": data[1],
                "last": data[2],
                "high": data[3],
                "low": data[4],
                "change": data[5],
                "bPrice": data[6],
                "bQty": data[7],
                "sPrice": data[8],
                "sQty": data[9],
                "ltq": data[10],
                "avgPrice": data[11],
                "quotes": "Quotes Data",
            }
            # For NSE & BSE conversion
            if len(data) == 21:
                data_dict["ttq"] = data[12]
                data_dict["totalBuyQt"] = data[13]
                data_dict["totalSellQ"] = data[14]
                data_dict["ttv"] = data[15]
                data_dict["trend"] = data[16]
                data_dict["lowerCktLm"] = data[17]
                data_dict["upperCktLm"] = data[18]
                data_dict["ltt"] = datetime.fromtimestamp(data[19]).strftime("%c")
                data_dict["close"] = data[20]
            # For FONSE & CDNSE conversion
            elif len(data) == 23:
                data_dict["OI"] = data[12]
                data_dict["CHNGOI"] = data[13]
                data_dict["ttq"] = data[14]
                data_dict["totalBuyQt"] = data[15]
                data_dict["totalSellQ"] = data[16]
                data_dict["ttv"] = data[17]
                data_dict["trend"] = data[18]
                data_dict["lowerCktLm"] = data[19]
                data_dict["upperCktLm"] = data[20]
                data_dict["ltt"] = datetime.fromtimestamp(data[21]).strftime("%c")
                data_dict["close"] = data[22]
        else:
            data_dict = {
                "symbol": data[0],
                "time": datetime.fromtimestamp(data[1]).strftime("%c"),
                "depth": self.parse_market_depth(data[2], exchange),
                "quotes": "Market Depth",
            }
        if exchange == "4" and len(data) == 21:
            data_dict["exchange"] = "NSE Equity"
        elif exchange == "1":
            data_dict["exchange"] = "BSE"
        elif exchange == "13":
            data_dict["exchange"] = "NSE Currency"
        elif exchange == "4" and len(data) == 23:
            data_dict["exchange"] = "NSE Futures & Options"
        elif exchange == "6":
            data_dict["exchange"] = "Commodity"
        return data_dict

    def api_util(self):
        try:
            headers = {"Content-Type": "application/json"}
            body = {"SessionToken": self.session_key, "AppKey": self.api_key}
            body = json.dumps(body, separators=(",", ":"))
            url = "https://uatapi.icicidirect.com/iciciDirectWebApi_core/api/v1/customerdetails"
            response = requests.get(url=url, data=body, headers=headers, verify=False)
            if response.json()["Success"] != None:
                base64_session_token = response.json()["Success"]["session_token"]
                result = base64.b64decode(base64_session_token.encode("ascii")).decode(
                    "ascii"
                )
                self.user_id = result.split(":")[0]
                self.session_key = result.split(":")[1]
            else:
                raise Exception(
                    "Could not authenticate credentials. Please check token and keys"
                )
        except Exception as e:
            raise Exception(
                "Could not authenticate credentials. Please check token and keys"
            )

    def load_cache(self):
        global response_cache
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as file:
                try:
                    response_cache = json.load(file)
                except json.JSONDecodeError:
                    response_cache = {}

    def save_cache(self):
        with open(CACHE_FILE, "w") as file:
            json.dump(response_cache, file)

    def cache_response(self, func):
        @functools.wraps(func)
        def wrapper(link, timeout=3):
            cache_key = str((link, str(timeout)))
            if cache_key in response_cache:

                cached_response = response_cache[cache_key]
                if time.time() - cached_response["timestamp"] <= CACHE_EXPIRATION:
                    print("Using cached response for:", link)
                    cached_response_data = cached_response["data"]
                    response = requests.Response()
                    response.status_code = cached_response_data["status_code"]
                    response._content = base64.b64decode(
                        cached_response_data["content"]
                    )
                    # response.url = link
                    return response

            try:
                print("network call..")
                # print(link,timeout)
                response = func(link)
                # print("response : ",response)
                response.raise_for_status()
                response_cache[cache_key] = {
                    "timestamp": time.time(),
                    "data": {
                        "status_code": response.status_code,
                        "content": base64.b64encode(response.content).decode("utf-8"),
                    },
                }
                self.save_cache()
                return response
            except requests.exceptions.Timeout:
                print(
                    f"The request timed out for: {link} as the server failed to respond"
                )
            except requests.exceptions.RequestException as e:
                print("An error occurred:", e)
            except Exception as e:
                print("An unexpected error occurred:", e)

        return wrapper

    def get_response(self, link, timeout=3):
        start = time.time()
        data = self.cache_response(requests.get)(link, timeout)
        end = time.time()
        print(f"execution time : {end - start}")
        return data

    def get_stock_script_list(self):
        try:
            self.load_cache()
            self.stock_script_dict_list = [{}, {}, {}, {}, {}, {}]
            self.token_script_dict_list = [{}, {}, {}, {}, {}, {}]
            link = "https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv"
            response = self.get_response(link)
            if response is not None:

                # download = s.get("https://traderweb.icicidirect.com/Content/File/txtFile/ScripFile/StockScriptNew.csv")
                cr = csv.reader(response.text.splitlines(), delimiter=",")
                my_list = list(cr)
                for row in my_list:
                    if row[2] == "BSE":
                        self.stock_script_dict_list[0][row[3]] = row[5]
                        self.token_script_dict_list[0][row[5]] = [row[3], row[1]]
                    elif row[2] == "NSE":
                        self.stock_script_dict_list[1][row[3]] = row[5]
                        self.token_script_dict_list[1][row[5]] = [row[3], row[1]]
                    elif row[2] == "NDX":
                        self.stock_script_dict_list[2][row[7]] = row[5]
                        self.token_script_dict_list[2][row[5]] = [row[7], row[1]]
                    elif row[2] == "MCX":
                        self.stock_script_dict_list[3][row[7]] = row[5]
                        self.token_script_dict_list[3][row[5]] = [row[7], row[1]]
                    elif row[2] == "NFO":
                        self.stock_script_dict_list[4][row[7]] = row[5]
                        self.token_script_dict_list[4][row[5]] = [row[7], row[1]]
                    elif row[2] == "BFO":
                        self.stock_script_dict_list[5][row[7]] = row[5]
                        self.token_script_dict_list[5][row[5]] = [row[7], row[1]]

        except Exception as e:
            print("error", e)
            # pass

    def generate_session(self, api_secret, session_token):
        self.session_key = session_token
        self.secret_key = api_secret
        self.api_util()
        self.get_stock_script_list()
        self.api_handler = ApificationBreeze(self)

    def get_customer_details(self, api_session=""):
        if self.api_handler:
            return self.api_handler.get_customer_details(api_session)

    def get_demat_holdings(self):
        if self.api_handler:
            return self.api_handler.get_demat_holdings()

    def get_funds(self):
        if self.api_handler:
            return self.api_handler.get_funds()

    def set_funds(self, transaction_type="", amount="", segment=""):
        if self.api_handler:
            return self.api_handler.set_funds(transaction_type, amount, segment)

    def get_historical_data(
        self,
        interval="",
        from_date="",
        to_date="",
        stock_code="",
        exchange_code="",
        product_type="",
        expiry_date="",
        right="",
        strike_price="",
    ):
        if self.api_handler:
            return self.api_handler.get_historical_data(
                interval,
                from_date,
                to_date,
                stock_code,
                exchange_code,
                product_type,
                expiry_date,
                right,
                strike_price,
            )

    def add_margin(
        self,
        product_type="",
        stock_code="",
        exchange_code="",
        settlement_id="",
        add_amount="",
        margin_amount="",
        open_quantity="",
        cover_quantity="",
        category_index_per_stock="",
        expiry_date="",
        right="",
        contract_tag="",
        strike_price="",
        segment_code="",
    ):
        if self.api_handler:
            return self.api_handler.add_margin(
                product_type,
                stock_code,
                exchange_code,
                settlement_id,
                add_amount,
                margin_amount,
                open_quantity,
                cover_quantity,
                category_index_per_stock,
                expiry_date,
                right,
                contract_tag,
                strike_price,
                segment_code,
            )

    def get_margin(self, exchange_code=""):
        if self.api_handler:
            return self.api_handler.get_margin(exchange_code)

    def place_order(
        self,
        stock_code="",
        exchange_code="",
        product="",
        action="",
        order_type="",
        stoploss="",
        quantity="",
        price="",
        validity="",
        validity_date="",
        disclosed_quantity="",
        expiry_date="",
        right="",
        strike_price="",
        user_remark="",
        order_type_fresh="",
        order_rate_fresh="",
        lots="",
    ):
        if self.api_handler:
            return self.api_handler.place_order(
                stock_code=stock_code,
                exchange_code=exchange_code,
                product=product,
                action=action,
                order_type=order_type,
                stoploss=stoploss,
                quantity=quantity,
                price=price,
                validity=validity,
                validity_date=validity_date,
                disclosed_quantity=disclosed_quantity,
                expiry_date=expiry_date,
                right=right,
                strike_price=strike_price,
                user_remark=user_remark,
                order_type_fresh=order_type_fresh,
                order_rate_fresh=order_rate_fresh,
                lots=lots,
            )

    def get_order_detail(self, exchange_code="", order_id=""):
        if self.api_handler:
            return self.api_handler.get_order_detail(exchange_code, order_id)

    def get_order_list(self, exchange_code="", from_date="", to_date=""):
        if self.api_handler:
            return self.api_handler.get_order_list(exchange_code, from_date, to_date)

    def cancel_order(self, exchange_code="", order_id=""):
        if self.api_handler:
            return self.api_handler.cancel_order(exchange_code, order_id)

    def modify_order(
        self,
        order_id="",
        exchange_code="",
        order_type="",
        stoploss="",
        quantity="",
        price="",
        validity="",
        disclosed_quantity="",
        validity_date="",
    ):
        if self.api_handler:
            return self.api_handler.modify_order(
                order_id,
                exchange_code,
                order_type,
                stoploss,
                quantity,
                price,
                validity,
                disclosed_quantity,
                validity_date,
            )

    def get_portfolio_holdings(
        self,
        exchange_code="",
        from_date="",
        to_date="",
        stock_code="",
        portfolio_type="",
    ):
        if self.api_handler:
            return self.api_handler.get_portfolio_holdings(
                exchange_code, from_date, to_date, stock_code, portfolio_type
            )

    def get_portfolio_positions(self):
        if self.api_handler:
            return self.api_handler.get_portfolio_positions()

    def get_quotes(
        self,
        stock_code="",
        exchange_code="",
        expiry_date="",
        product_type="",
        right="",
        strike_price="",
    ):
        if self.api_handler:
            return self.api_handler.get_quotes(
                stock_code,
                exchange_code,
                expiry_date,
                product_type,
                right,
                strike_price,
            )

    def get_option_chain_quotes(
        self,
        stock_code="",
        exchange_code="",
        expiry_date="",
        product_type="",
        right="",
        strike_price="",
    ):
        if self.api_handler:
            return self.api_handler.get_option_chain_quotes(
                stock_code,
                exchange_code,
                expiry_date,
                product_type,
                right,
                strike_price,
            )

    def square_off(
        self,
        source_flag="",
        stock_code="",
        exchange_code="",
        quantity="",
        price="",
        action="",
        order_type="",
        validity="",
        stoploss="",
        disclosed_quantity="",
        protection_percentage="",
        settlement_id="",
        margin_amount="",
        open_quantity="",
        cover_quantity="",
        product_type="",
        expiry_date="",
        right="",
        strike_price="",
        validity_date="",
        trade_password="",
        alias_name="",
        lots="",
    ):
        if self.api_handler:
            return self.api_handler.square_off(
                source_flag,
                stock_code,
                exchange_code,
                quantity,
                price,
                action,
                order_type,
                validity,
                stoploss,
                disclosed_quantity,
                protection_percentage,
                settlement_id,
                margin_amount,
                open_quantity,
                cover_quantity,
                product_type,
                expiry_date,
                right,
                strike_price,
                validity_date,
                trade_password,
                alias_name,
                lots,
            )

    def get_trade_list(
        self,
        from_date="",
        to_date="",
        exchange_code="",
        product_type="",
        action="",
        stock_code="",
    ):
        if self.api_handler:
            return self.api_handler.get_trade_list(
                from_date, to_date, exchange_code, product_type, action, stock_code
            )

    def get_trade_detail(self, exchange_code="", order_id=""):
        if self.api_handler:
            return self.api_handler.get_trade_detail(exchange_code, order_id)

    def get_names(self, exchange_code="", stock_code=""):
        if self.api_handler:
            return self.api_handler.get_names(exchange_code, stock_code)

    def preview_order(
        self,
        stock_code="",
        exchange_code="",
        product="",
        order_type="",
        price="",
        action="",
        quantity="",
        expiry_date="",
        right="",
        strike_price="",
        specialflag="",
        stoploss="",
        order_rate_fresh="",
    ):
        if self.api_handler:
            return self.api_handler.preview_order(
                stock_code,
                exchange_code,
                product,
                order_type,
                price,
                action,
                quantity,
                expiry_date,
                right,
                strike_price,
                specialflag,
                stoploss,
                order_rate_fresh,
            )


class ApificationBreeze:

    def __init__(self, breeze_instance):
        self.breeze = breeze_instance
        self.hostname = "https://uatapi.icicidirect.com/iciciDirectWebApi_core/api/v1/"
        self.base64_session_token = base64.b64encode(
            (self.breeze.user_id + ":" + self.breeze.session_key).encode("ascii")
        ).decode("ascii")

    def generate_headers(self, body):
        try:
            current_date = datetime.utcnow().isoformat()[:19] + ".000Z"
            checksum = sha256(
                (current_date + body + self.breeze.secret_key).encode("utf-8")
            ).hexdigest()
            headers = {
                "Content-Type": "application/json",
                "X-Checksum": "token " + checksum,
                "X-Timestamp": current_date,
                "X-AppKey": self.breeze.api_key,
                "X-SessionToken": self.base64_session_token,
            }
            return headers
        except Exception as e:
            print("generate_headers() Error - ", e)

    def make_request(self, method, endpoint, body, headers):
        try:
            url = self.hostname + endpoint
            if method == "GET":
                res = requests.get(url=url, data=body, headers=headers, verify=False)
                return res
            elif method == "POST":
                res = requests.post(url=url, data=body, headers=headers, verify=False)
                return res
            elif method == "PUT":
                res = requests.put(url=url, data=body, headers=headers, verify=False)
                return res
            elif method == "DELETE":
                res = requests.delete(url=url, data=body, headers=headers, verify=False)
                return res
            else:
                print("Invalid Request Method - Must be GET, POST, PUT or DELETE")
        except Exception as e:
            print("Error while trying to make request " + method + " " + url + " - ", e)

    def get_customer_details(self, api_session=""):
        try:
            if api_session == "" or api_session == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "api_session cannot be empty",
                }
                return response
            headers = {"Content-Type": "application/json"}
            body = {
                "SessionToken": api_session,
                "AppKey": self.breeze.api_key,
            }
            body = json.dumps(body, separators=(",", ":"))
            response = self.make_request("GET", "customerdetails", body, headers)
            response = response.json()
            if (
                "Success" in response
                and response["Success"] != None
                and "session_token" in response["Success"]
            ):
                del response["Success"]["session_token"]
            return response
        except Exception as e:
            print("get_customer_details() Error - ", e)

    def get_demat_holdings(self):
        try:
            body = {}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "dematholdings", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_demat_holdings() Error- ", e)

    def get_funds(self):
        try:
            body = {}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "funds", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_funds() Error - ", e)

    def set_funds(self, transaction_type="", amount="", segment=""):
        try:
            if (
                transaction_type == ""
                or transaction_type == None
                or amount == ""
                or amount == None
                or segment == ""
                or segment == None
            ):
                response = {"Success": "", "Status": 500, "Error": ""}
                if transaction_type == "" or transaction_type == None:
                    response["Error"] = "Transaction-Type cannot be empty"
                elif amount == "" or amount == None:
                    response["Error"] = "Amount cannot be empty"
                elif segment == "" or segment == None:
                    response["Error"] = "Segment cannot be empty"
                return response
            elif transaction_type.lower() not in ["debit", "credit"]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Transaction-Type should be either 'debit' or 'credit'",
                }
                return response
            if amount.isdigit():  # Check if the input does not consist only of digits
                if not int(amount) > 0:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Amount should be more than 0",
                    }
                    return response
            else:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Amount should only contain digits",
                }
                return response

            body = {
                "transaction_type": transaction_type,
                "amount": amount,
                "segment": segment,
            }
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "funds", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("set_funds() Error - ", e)

    def get_historical_data(
        self,
        interval="",
        from_date="",
        to_date="",
        stock_code="",
        exchange_code="",
        product_type="",
        expiry_date="",
        right="",
        strike_price="",
    ):
        try:
            if interval == "" or interval == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Interval cannot be empty",
                }
                return response
            elif interval.lower() not in ["1minute", "5minute", "30minute", "1day"]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Interval should be either '1minute', '5minute', '30minute', or '1day'",
                }
                return response
            elif exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            elif exchange_code.lower() not in ["nse", "nfo", "ndx", "mcx"]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code should be either 'nse', or 'nfo' or 'ndx' or 'mcx'",
                }
                return response
            elif from_date == "" or from_date == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "From-Date cannot be empty",
                }
                return response
            elif to_date == "" or to_date == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "To-Date cannot be empty",
                }
                return response
            elif stock_code == "" or stock_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Stock-Code cannot be empty",
                }
                return response
            elif exchange_code.lower() == "nfo":
                if product_type == "" or product_type == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Product-type cannot be empty for Exchange-Code 'nfo'",
                    }
                    return response
                elif product_type.lower() not in [
                    "futures",
                    "options",
                    "futureplus",
                    "optionplus",
                ]:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Product-type should be either 'futures', 'options', 'futureplus', or 'optionplus' for Exchange-Code 'NFO'",
                    }
                    return response
                elif product_type.lower() == "options" and (
                    strike_price == "" or strike_price == None
                ):
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Strike-Price cannot be empty for Product-Type 'options'",
                    }
                    return response
                elif expiry_date == "" or expiry_date == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Expiry-Date cannot be empty for exchange-code 'nfo'",
                    }
                    return response
            if interval == "1minute":
                interval = "minute"
            elif interval == "1day":
                interval = "day"
            body = {
                "interval": interval,
                "from_date": from_date,
                "to_date": to_date,
                "stock_code": stock_code,
                "exchange_code": exchange_code,
            }
            if product_type != "" and product_type != None:
                body["product_type"] = product_type
            if expiry_date != "" and expiry_date != None:
                body["expiry_date"] = expiry_date
            if strike_price != "" and strike_price != None:
                body["strike_price"] = strike_price
            if right != "" and right != None:
                body["right"] = right
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "historicalcharts", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_historical_data() Error - ", e)

    def add_margin(
        self,
        product_type="",
        stock_code="",
        exchange_code="",
        settlement_id="",
        add_amount="",
        margin_amount="",
        open_quantity="",
        cover_quantity="",
        category_index_per_stock="",
        expiry_date="",
        right="",
        contract_tag="",
        strike_price="",
        segment_code="",
    ):
        try:
            if exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            elif (
                product_type != ""
                and product_type != None
                and product_type.lower()
                not in [
                    "futures",
                    "options",
                    "futureplus",
                    "optionplus",
                    "cash",
                    "eatm",
                    "margin",
                ]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product-type should be either 'futures', 'options', 'futureplus', 'optionplus', 'cash', 'eatm', or 'margin'",
                }
                return response
            elif (
                right != ""
                and right != None
                and right.lower() not in ["call", "put", "others"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Right should be either 'call', 'put', or 'others'",
                }
                return response
            body = {"exchange_code": exchange_code}
            if product_type != "" and product_type != None:
                body["product_type"] = product_type
            if stock_code != "" and stock_code != None:
                body["stock_code"] = stock_code
            if cover_quantity != "" and cover_quantity != None:
                body["cover_quantity"] = cover_quantity
            if category_index_per_stock != "" and category_index_per_stock != None:
                body["category_index_per_stock"] = category_index_per_stock
            if contract_tag != "" and contract_tag != None:
                body["contract_tag"] = contract_tag
            if margin_amount != "" and margin_amount != None:
                body["margin_amount"] = margin_amount
            if expiry_date != "" and expiry_date != None:
                body["expiry_date"] = expiry_date
            if right != "" and right != None:
                body["right"] = right
            if strike_price != "" and strike_price != None:
                body["strike_price"] = strike_price
            if segment_code != "" and segment_code != None:
                body["segment_code"] = segment_code
            if settlement_id != "" and settlement_id != None:
                body["settlement_id"] = settlement_id
            if add_amount != "" and add_amount != None:
                body["add_amount"] = add_amount
            if open_quantity != "" and open_quantity != None:
                body["open_quantity"] = open_quantity
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "margin", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("add_margin() Error - ", e)

    def get_margin(self, exchange_code=""):
        try:
            if exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            body = {"exchange_code": exchange_code}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            print("headers---------------------->", headers)
            response = self.make_request("GET", "margin", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_margin() Error - ", e)

    def place_order(
        self,
        stock_code="",
        exchange_code="",
        product="",
        action="",
        order_type="",
        stoploss="",
        quantity="",
        price="",
        validity="",
        validity_date="",
        disclosed_quantity="",
        expiry_date="",
        right="",
        strike_price="",
        user_remark="",
        order_type_fresh="",
        order_rate_fresh="",
        lots="",
    ):
        try:
            if (
                stock_code == ""
                or stock_code == None
                or exchange_code == ""
                or exchange_code == None
                or product == ""
                or product == None
                or action == ""
                or action == None
                or order_type == ""
                or order_type == None
                or price == ""
                or price == None
                or action == ""
                or action == None
            ):
                if stock_code == "" or stock_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Stock-Code cannot be empty",
                    }
                    return response
                elif exchange_code == "" or exchange_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Exchange-Code cannot be empty",
                    }
                    return response
                elif product == "" or product == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Product cannot be empty",
                    }
                    return response
                elif action == "" or action == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Action cannot be empty",
                    }
                    return response
                elif order_type == "" or order_type == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Order-type cannot be empty",
                    }
                    return response
                elif validity == "" or validity == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Validity cannot be empty",
                    }
                    return response
            elif product.lower() not in [
                "futures",
                "options",
                "futureplus",
                "optionplus",
                "cash",
                "eatm",
                "margin",
            ]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product should be either 'futures', 'options', 'futureplus', 'optionplus', 'cash', 'eatm', or 'margin'",
                }
                return response
            elif action.lower() not in ["buy", "sell"]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Action should be either 'buy', or 'sell'",
                }
                return response
            elif order_type.lower() not in ["limit", "market", "stoploss"]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Order-type should be either 'limit', 'market', or 'stoploss'",
                }
                return response
            elif validity.lower() not in ["day", "ioc", "vtc"]:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Validity should be either 'day', 'ioc', or 'vtc'",
                }
                return response
            elif (
                right != ""
                and right != None
                and right.lower() not in ["call", "put", "others"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Right should be either 'call', 'put', or 'others'",
                }
                return response
            if exchange_code.lower() in ["mcx", "ndx"]:
                if lots == "" or lots == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Lots cannot be empty",
                    }
                    return response
            else:
                if quantity == "" or quantity == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Quantity cannot be empty",
                    }
                    return response
            body = {
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "product": product,
                "action": action,
                "order_type": order_type,
                "quantity": quantity,
                "price": price,
                "validity": validity,
                "order_type_fresh": order_type_fresh,
                "order_rate_fresh": order_rate_fresh,
                "lots": lots,
            }
            if stoploss != "" and stoploss != None:
                body["stoploss"] = stoploss
            if validity_date != "" and validity_date != None:
                body["validity_date"] = validity_date
            if disclosed_quantity != "" and disclosed_quantity != None:
                body["disclosed_quantity"] = disclosed_quantity
            if expiry_date != "" and expiry_date != None:
                body["expiry_date"] = expiry_date
            if right != "" and right != None:
                body["right"] = right
            if strike_price != "" and strike_price != None:
                body["strike_price"] = strike_price
            if user_remark != "" and user_remark != None:
                body["user_remark"] = user_remark
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("place_order() Error - ", e)

    def get_order_detail(self, exchange_code, order_id):
        try:
            if (
                exchange_code == ""
                or exchange_code == None
                or order_id == ""
                or order_id == None
            ):
                if exchange_code == "" or exchange_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Exchange-Code cannot be empty",
                    }
                    return response
                elif order_id == "" or order_id == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Order-Id cannot be empty",
                    }
                    return response
            body = {"exchange_code": exchange_code, "order_id": order_id}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_order_detail() Error - ", e)

    def get_order_list(self, exchange_code, from_date, to_date):
        try:
            if (
                exchange_code == ""
                or exchange_code == None
                or from_date == ""
                or from_date == None
                or to_date == ""
                or to_date == None
            ):
                if exchange_code == "" or exchange_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Exchange-Code cannot be empty",
                    }
                    return response
                elif from_date == "" or from_date == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "From-Date cannot be empty",
                    }
                    return response
                elif to_date == "" or to_date == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "To-Date cannot be empty",
                    }
                    return response
            body = {
                "exchange_code": exchange_code,
                "from_date": from_date,
                "to_date": to_date,
            }
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_order_list() Error - ", e)

    def cancel_order(self, exchange_code, order_id):
        try:
            if (
                exchange_code == ""
                or exchange_code == None
                or order_id == ""
                or order_id == None
            ):
                if exchange_code == "" or exchange_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Exchange-Code cannot be empty",
                    }
                    return response
                elif order_id == "" or order_id == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Order-Id cannot be empty",
                    }
                    return response
            body = {"exchange_code": exchange_code, "order_id": order_id}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("DELETE", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("cancel_order() Error - ", e)

    def modify_order(
        self,
        order_id,
        exchange_code,
        order_type,
        stoploss,
        quantity,
        price,
        validity,
        disclosed_quantity,
        validity_date,
    ):
        try:
            if (
                exchange_code == ""
                or exchange_code == None
                or order_id == ""
                or order_id == None
            ):
                if exchange_code == "" or exchange_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Exchange-Code cannot be empty",
                    }
                    return response
                elif order_id == "" or order_id == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Order-Id cannot be empty",
                    }
                    return response
            elif (
                order_type != ""
                and order_type != None
                and order_type.lower() not in ["limit", "market", "stoploss"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Order-type should be either 'limit', 'market', or 'stoploss'",
                }
                return response
            elif (
                validity != ""
                and validity != None
                and validity.lower() not in ["day", "ioc", "vtc"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Validity should be either 'day', 'ioc', or 'vtc'",
                }
                return response
            body = {
                "order_id": order_id,
                "exchange_code": exchange_code,
            }
            if order_type != "" and order_type != None:
                body["order_type"] = order_type
            if stoploss != "" and stoploss != None:
                body["stoploss"] = stoploss
            if quantity != "" and quantity != None:
                body["quantity"] = quantity
            if price != "" and price != None:
                body["price"] = price
            if validity != "" and validity != None:
                body["validity"] = validity
            if disclosed_quantity != "" and disclosed_quantity != None:
                body["disclosed_quantity"] = disclosed_quantity
            if validity_date != "" and validity_date != None:
                body["validity_date"] = validity_date
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("PUT", "order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("modify_order() Error - ", e)

    def get_portfolio_holdings(
        self, exchange_code, from_date, to_date, stock_code, portfolio_type
    ):
        try:
            if exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            body = {
                "exchange_code": exchange_code,
            }
            if from_date != "" and from_date != None:
                body["from_date"] = from_date
            if to_date != "" and to_date != None:
                body["to_date"] = to_date
            if stock_code != "" and stock_code != None:
                body["stock_code"] = stock_code
            if portfolio_type != "" and portfolio_type != None:
                body["portfolio_type"] = portfolio_type
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "portfolioholdings", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_portfolio_holdings() Error - ", e)

    def get_portfolio_positions(self):
        try:
            body = {}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "portfoliopositions", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_portfolio_positions() Error - ", e)

    def get_quotes(
        self, stock_code, exchange_code, expiry_date, product_type, right, strike_price
    ):
        try:
            if (
                exchange_code == ""
                or exchange_code == None
                or stock_code == ""
                or stock_code == None
            ):
                if exchange_code == "" or exchange_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Exchange-Code cannot be empty",
                    }
                    return response
                if stock_code == "" or stock_code == None:
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Stock-Code cannot be empty",
                    }
                    return response
            elif (
                product_type != ""
                and product_type != None
                and product_type.lower()
                not in [
                    "futures",
                    "options",
                    "futureplus",
                    "optionplus",
                    "cash",
                    "eatm",
                    "margin",
                ]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product-type should be either 'futures', 'options', 'futureplus', 'optionplus', 'cash', 'eatm', or 'margin'",
                }
                return response
            elif (
                right != ""
                and right != None
                and right.lower() not in ["call", "put", "others"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Right should be either 'call', 'put', or 'others'",
                }
                return response
            body = {"stock_code": stock_code, "exchange_code": exchange_code}
            if expiry_date != "" and expiry_date != None:
                body["expiry_date"] = expiry_date
            if product_type != "" and product_type != None:
                body["product_type"] = product_type
            if right != "" and right != None:
                body["right"] = right
            if strike_price != "" and strike_price != None:
                body["strike_price"] = strike_price
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "quotes", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_quotes() Error - ", e)

    def get_option_chain_quotes(
        self, stock_code, exchange_code, expiry_date, product_type, right, strike_price
    ):
        try:
            if (
                exchange_code == ""
                or exchange_code == None
                or exchange_code.lower() != "nfo"
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "exchange code should be nfo",
                }
                return response
            elif product_type == "" or product_type == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product-Type cannot be empty for Exchange-Code value as 'nfo'.",
                }
                return response
            elif product_type != "future" and product_type != "options":
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product-type should be either 'futures' or 'options' for Exchange-Code value as 'nfo'.",
                }
                return response
            elif stock_code == "" or stock_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "stock code cannot be empty",
                }
                return response
            elif product_type == "options":
                if (
                    (expiry_date == "" or expiry_date == None)
                    and (strike_price == "" or strike_price == None)
                    and (right == "" or right == None)
                ):
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Atleast two inputs are required out of Expiry-Date, Right & Strike-Price. All three cannot be empty'.",
                    }
                    return response
                elif (
                    (expiry_date != "" or expiry_date != None)
                    and (strike_price == "" or strike_price == None)
                    and (right == "" or right == None)
                ):
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Either Right or Strike-Price cannot be empty.",
                    }
                    return response
                elif (
                    (expiry_date == "" or expiry_date == None)
                    and (strike_price != "" or strike_price != None)
                    and (right == "" or right == None)
                ):
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Either Expiry-Date or Right cannot be empty.",
                    }
                    return response
                elif (
                    (expiry_date == "" or expiry_date == None)
                    and (strike_price == "" or strike_price == None)
                    and (right != None or right != "")
                ):
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Either Expiry-Date or Strike-Price cannot be empty.",
                    }
                    return response
                elif (right != "" or right != None) and (
                    right != "call" and right != "put" and right != "others"
                ):
                    response = {
                        "Success": "",
                        "Status": 500,
                        "Error": "Right should be either 'call', 'put', or 'others'.",
                    }
                    return response
            body = {"stock_code": stock_code, "exchange_code": exchange_code}
            if expiry_date != "" and expiry_date != None:
                body["expiry_date"] = expiry_date
            if product_type != "" and product_type != None:
                body["product_type"] = product_type
            if right != "" and right != None:
                body["right"] = right
            if strike_price != "" and strike_price != None:
                body["strike_price"] = strike_price
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "optionchain", body, headers)
            response = response.json()
            return response
        except:
            print("get_option_chain_quotes() Error -", e)

    def square_off(
        self,
        source_flag,
        stock_code,
        exchange_code,
        quantity,
        price,
        action,
        order_type,
        validity,
        stoploss,
        disclosed_quantity,
        protection_percentage,
        settlement_id,
        margin_amount,
        open_quantity,
        cover_quantity,
        product_type,
        expiry_date,
        right,
        strike_price,
        validity_date,
        trade_password,
        alias_name,
        lots,
    ):
        try:
            body = {
                "source_flag": source_flag,
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "quantity": quantity,
                "price": price,
                "action": action,
                "order_type": order_type,
                "validity": validity,
                "stoploss_price": stoploss,
                "disclosed_quantity": disclosed_quantity,
                "protection_percentage": protection_percentage,
                "settlement_id": settlement_id,
                "margin_amount": margin_amount,
                "open_quantity": open_quantity,
                "cover_quantity": cover_quantity,
                "product_type": product_type,
                "expiry_date": expiry_date,
                "right": right,
                "strike_price": strike_price,
                "validity_date": validity_date,
                "alias_name": alias_name,
                "trade_password": trade_password,
                "lots": lots,
            }
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("POST", "squareoff", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("square_off() Error - ", e)

    def get_trade_list(
        self, from_date, to_date, exchange_code, product_type, action, stock_code
    ):
        try:
            if exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            elif (
                product_type != ""
                and product_type != None
                and product_type.lower()
                not in [
                    "futures",
                    "options",
                    "futureplus",
                    "optionplus",
                    "cash",
                    "eatm",
                    "margin",
                ]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product-type should be either 'futures', 'options', 'futureplus', 'optionplus', 'cash', 'eatm', or 'margin'",
                }
                return response
            elif (
                action != ""
                and action != None
                and action.lower() not in ["buy", "sell"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Action should be either 'buy', or 'sell'",
                }
                return response
            body = {
                "exchange_code": exchange_code,
            }
            if from_date != "" and from_date != None:
                body["from_date"] = from_date
            if to_date != "" and to_date != None:
                body["to_date"] = to_date
            if product_type != "" and product_type != None:
                body["product_type"] = product_type
            if action != "" and action != None:
                body["action"] = action
            if stock_code != "" and stock_code != None:
                body["stock_code"] = stock_code
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "trades", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_trade_list() Error - ", e)

    def get_trade_detail(self, exchange_code, order_id):
        try:
            if exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            elif order_id == "" or order_id == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Order-Id cannot be empty",
                }
                return response
            body = {"exchange_code": exchange_code, "order_id": order_id}
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "trades", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("get_trade_detail() Error - ", e)

    def get_names(self, exchange_code, stock_code):
        try:
            lexchange_code = exchange_code.lower()
            stock_code = stock_code.upper()
            mapper_exchangecode_to_file = dict()
            mapper_exchangecode_to_file["nse"] = "NSEScripMaster.txt"
            mapper_exchangecode_to_file["bse"] = "BSEScripMaster.txt"
            mapper_exchangecode_to_file["cdnse"] = "CDNSEScripMaster.txt"
            mapper_exchangecode_to_file["fonse"] = "FONSEScripMaster.txt"
            required_file = zipfile.open(
                mapper_exchangecode_to_file.get(lexchange_code)
            )

            dataframe = pd.read_csv(required_file, sep=",", engine="python")

            print(dataframe.columns)
            print("length", len(dataframe.columns))
            df2 = dataframe[dataframe[' "ExchangeCode"'] == stock_code]
            if len(df2) == 0:
                df2 = dataframe[dataframe[' "ShortName"'] == stock_code]
            # print("df",df2)

            requiredresult = df2[
                [' "ShortName"', ' "ExchangeCode"', "Token", ' "CompanyName"']
            ]

            isec_stock = requiredresult[' "ShortName"'].to_string().split()[1]
            token = requiredresult["Token"].to_string().split()[1]
            exchange = requiredresult[' "ExchangeCode"'].to_string()

            if " " in exchange:
                exchange = exchange.split()[1]

            # print(value,"val")
            result = dict()
            result["exchange_code"] = exchange_code
            result["exchange_stock_code"] = exchange
            result["isec_stock_code"] = isec_stock
            result["isec_token"] = token
            result["company_name"] = " ".join(
                requiredresult[' "CompanyName"'].to_string().split()[1:]
            )
            response = json.dumps(result, indent=4)
            return response
        except Exception as e:
            print("get_names() Error - ", e)

    def preview_order(
        self,
        stock_code="",
        exchange_code="",
        product="",
        order_type="",
        price="",
        action="",
        quantity="",
        expiry_date="",
        right="",
        strike_price="",
        specialflag="",
        stoploss="",
        order_rate_fresh="",
    ):
        try:
            if exchange_code == "" or exchange_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Exchange-Code cannot be empty",
                }
                return response
            elif product == "" or product == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Product cannot be empty",
                }
                return response
            elif stock_code == "" or stock_code == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "stock code cannot be empty",
                }
                return response
            elif order_type == "" or order_type == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Order-type cannot be empty",
                }
                return response
            elif action == "" or action == None:
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Action cannot be empty",
                }
                return response
            elif (
                right != ""
                and right != None
                and right.lower() not in ["call", "put", "others"]
            ):
                response = {
                    "Success": "",
                    "Status": 500,
                    "Error": "Right should be either 'call', 'put', or 'others'",
                }
                return response

            body = {
                "stock_code": stock_code,
                "exchange_code": exchange_code,
                "product": product,
                "order_type": order_type,
                "price": price,
                "action": action,
                "quantity": quantity,
                "expiry_date": expiry_date,
                "right": right,
                "strike_price": strike_price,
                "specialflag": specialflag,
                "stoploss": stoploss,
                "order_rate_fresh": order_rate_fresh,
            }
            body = json.dumps(body, separators=(",", ":"))
            headers = self.generate_headers(body)
            response = self.make_request("GET", "preview_order", body, headers)
            response = response.json()
            return response
        except Exception as e:
            print("preview_order Error - ", e)
