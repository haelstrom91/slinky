
from abc import ABC, abstractmethod
import sqlite3

# class Connector(ABC):
class Connector:
    def __init__(self, source):
        self.source = source

    # @abstractmethod
    # def get_data(address, call, credentials = {}):
    #     pass

    def get_data(self, query):
        con = sqlite3.connect(f"data/{self.source}.db")
        cur = con.cursor()
        data = []
        if query:
            try:
                res = cur.execute(query)
                headers = list(map(lambda attr : attr[0], cur.description))
                data = [{header:row[i] for i, header in enumerate(headers)} for row in cur]
            except:
                data = [{"question unclear": 0}]
        con.close()
        return data

