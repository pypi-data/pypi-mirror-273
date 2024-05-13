#  The MIT License (MIT)
#
#  Copyright (c) 2024. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging

import pandas as pd
from config42 import ConfigManager

from sc_inclusive_balance_detail_analysis.analyzer.base_analyzer import BaseAnalyzer
from sc_inclusive_balance_detail_analysis.manifest_utils import ManifestUtils


class ManagerSummaryAnalyzer(BaseAnalyzer):
    """
    按客户经理汇总分析
    """

    def __init__(self, *, config: ConfigManager, excel_writer: pd.ExcelWriter, target_column_list: list):
        super().__init__(config=config, excel_writer=excel_writer)
        self._key_enabled = "inclusive.manager_summary.enabled"
        self._key_business_type = "inclusive.manager_summary.business_type"
        self._target_column_list = list()
        self._target_column_list.extend(target_column_list)

    def analysis(self, *, manifest_data: pd.DataFrame, previous_data: pd.DataFrame) -> pd.DataFrame:
        # 读取业务类型
        self._business_type = self._config.get(self._key_business_type)
        # 如果未启用，则直接返回上一次的分析数据
        if not self._enabled():
            # 处理缺少配置的情况下日志记录不到具体分析类型的问题
            business_type = self._business_type
            if business_type is None:
                business_type = self._key_business_type
            logging.getLogger(__name__).info("{} 分析未启用".format(business_type))
            return previous_data
        logging.getLogger(__name__).info("开始分析 {} 数据".format(self._business_type))

        # 没有统计列，则不处理
        if len(self._target_column_list) == 0:
            return previous_data
        data = pd.pivot_table(
            previous_data, values=self._target_column_list,
            index=[
                ManifestUtils.get_id_column_name(),
                ManifestUtils.get_name_column_name(),
                ManifestUtils.get_branch_column_name(),
            ],
            aggfunc="sum",
            fill_value=0,
            # 添加按列合计
            margins=True,
            margins_name="合计",
        )
        data.reset_index(inplace=True)
        logging.getLogger(__name__).info("完成分析 {} 数据".format(self._business_type))
        return data

    def write_origin_data(self):
        # 汇总不输出明细数据，否则会将真正的汇总给覆盖掉
        pass
