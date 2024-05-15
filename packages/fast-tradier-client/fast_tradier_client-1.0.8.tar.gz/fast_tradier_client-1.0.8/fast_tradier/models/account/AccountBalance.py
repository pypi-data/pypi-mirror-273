from dataclasses import dataclass
from typing import Dict, Optional

from fast_tradier.models.DataClassModelBase import DataClassModelBase
from fast_tradier.models.ModelBase import NewModelBase

class Cash(NewModelBase):
    cash_available: float
    sweep: int
    unsettled_funds: float

class Margin(NewModelBase):
    fed_call: int
    maintenance_call: int
    option_buying_power: float
    stock_buying_power: float
    stock_short_value: int
    sweep: int

class Pdt(NewModelBase):
    fed_call: int
    maintenance_call: int
    option_buying_power: float
    stock_buying_power: float
    stock_short_value: int

class AccountBalance(NewModelBase):
    option_short_value: Optional[int] = None
    total_equity: float
    account_number: str
    account_type: str
    close_pl: float
    current_requirement: float
    equity: int
    long_market_value: float
    market_value: float
    open_pl: float
    option_long_value: float
    option_requirement: int
    pending_orders_count: int
    short_market_value: int
    stock_long_value: float
    total_cash: float
    uncleared_funds: int
    pending_cash: int
    margin: Optional[Margin]  = None
    cash: Optional[Cash] = None
    pdt: Optional[Pdt] = None