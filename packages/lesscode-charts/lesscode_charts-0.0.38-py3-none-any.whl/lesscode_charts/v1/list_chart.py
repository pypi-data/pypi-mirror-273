from typing import Union


class ListChart:
    @staticmethod
    def list_chart(columns: Union[list, dict], data: list):
        """

        :param columns: [{"title":"","dataIndex":""}] or {"名称":"字段名"}
        :param data:
        :return:
        """
        if isinstance(columns, dict):
            columns = [{"title": k, "dataIndex": v} for k, v in columns.items()]
        return {
            "columns": columns,
            "data": data
        }
