import sqlite3
from pathlib import Path

class DB:
    def __init__(self,path="data/monitor.db"):
        Path(path).parent.mkdir(exist_ok=True)
        self.c=sqlite3.connect(path)
        self.c.execute("CREATE TABLE IF NOT EXISTS alerts(item_id TEXT PRIMARY KEY, price REAL, product_id TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP)")
        self.c.commit()
    def alerted(self,item):
        return self.c.execute("SELECT 1 FROM alerts WHERE item_id=?",(item,)).fetchone() is not None
    def add(self,item,price,product):
        self.c.execute("INSERT OR REPLACE INTO alerts(item_id,price,product_id) VALUES(?,?,?)",(item,price,product))
        self.c.commit()
