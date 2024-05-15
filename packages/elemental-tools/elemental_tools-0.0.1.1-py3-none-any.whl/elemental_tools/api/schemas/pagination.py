from typing import Generator, Union

from icecream import ic
from pydantic import BaseModel


class PaginationSchema(BaseModel):
    """
    Pagination Schema:

    Access page from list or generator (self.get_page);
    Return Pagination Headers (self.headers);


    """

    page_size: int = 50
    page_num: int = 1
    page_count: int = 0
    row_count: int = 0

    def get_page(self, cursor: Union[Generator, list], schema=None):
        _result = []
        count = 0
        try:

            self.page_count = int(-(-self.row_count // self.page_size))

            start_index = (self.page_num - 1) * self.page_size
            end_index = start_index + self.page_size

            for idx, value in enumerate(cursor):
                idx += 1

                if idx >= start_index and not idx > end_index:
                    count += 1
                    if schema is not None:
                        _result.append(schema(**value).model_dump())
                        continue

                    _result.append(value)

                elif idx > end_index:
                    break

        except Exception as e:
            print(e)

        if isinstance(cursor, list):
            list_len = len(cursor)
        else:
            list_len = len(list(cursor))

        self.row_count = count + list_len
        return _result

    def headers(self):
        _result = {}
        for key, value in self.model_dump().items():
            _result[key] = str(value)

        return _result

