import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import pandas as pd
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')
import mns_common.constant.db_name_constant as db_name_constant


# 黑名单操作

def save_black_stock(symbol,
                     name,
                     str_day,
                     str_now_date,
                     choose_reason,
                     choose_reason_detail):
    black_choose_dict = {
        "_id": symbol,
        "symbol": symbol,
        "name": name,
        "str_day": str_day,
        "str_now_date": str_now_date,
        "choose_reason": choose_reason,
        "choose_reason_detail": choose_reason_detail
    }
    black_choose_df = pd.DataFrame(black_choose_dict, index=[1])
    mongodb_util.save_mongo(black_choose_df, db_name_constant.SELF_BLACK_STOCK)
