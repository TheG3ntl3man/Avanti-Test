from .database import Database
from typing import Dict, Any
from loguru import logger

class StockTag(Database):
    format = ["stock_id", "tag_id"]

    def __init__(self):
        super(StockTag, self).__init__()

    def associate_stock(self, stock_id: str, tag_id: str) -> Dict[str, Any]:
        """
            makes the association of tag and stock. Inserts this association in table.
        """
        query = "INSERT INTO stock_tag (stock_id, tag_id) " \
                "VALUES ({}, {})".format(stock_id, tag_id)
        stock_tag_info = self.execute(query)
        logger.info(stock_tag_info)
        return stock_tag_info

    def delete_stock_tag(self, stock_id: int, category: str, tag_name: str) -> Dict[str, Any]:
        query = "DELETE FROM stock_tag " \
                "WHERE stock_id = {} " \
                "AND tag_id = (SELECT id " \
                "FROM tag WHERE category = '{}' AND tag_name = '{}')".format(stock_id, category, tag_name)
        logger.info(query)
        stock_tag_info = self.execute(query)
        return stock_tag_info
