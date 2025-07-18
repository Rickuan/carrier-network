import sqlite3
from datetime import datetime

conn = sqlite3.connect("carrier_network.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS Carrier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Node (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    x INTEGER NOT NULL, 
    y INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS OrderItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pickup_node INTEGER,
    delivery_node INTEGER,
    current_owner INTEGER,
    FOREIGN KEY(pickup_node) REFERENCES Node(id),
    FOREIGN KEY(delivery_node) REFERENCES Node(id),
    FOREIGN KEY(current_owner) REFERENCES Carrier(id)
);

CREATE TABLE IF NOT EXISTS OrderBundle (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE IF NOT EXISTS OrderBundleItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bundle_id INTEGER,
    order_id INTEGER,
    FOREIGN KEY(bundle_id) REFERENCES OrderBundle(id),
    FOREIGN KEY(order_id) REFERENCES OrderItem(id)
);

CREATE TABLE IF NOT EXISTS TransactionLog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    buyer_id INTEGER,
    seller_id INTEGER,
    order_id INTEGER,
    timestamp TEXT,
    FOREIGN KEY(buyer_id) REFERENCES Carrier(id),
    FOREIGN KEY(seller_id) REFERENCES Carrier(id),
    FOREIGN KEY(order_id) REFERENCES OrderItem(id)
);
""")
conn.commit()

# -------------------------------------------------
# BASIC OPERATIONS
# -------------------------------------------------

def add_carrier(name):
    cursor.execute("INSERT INTO Carrier (name) VALUES (?)", 
                   (name,))
    conn.commit()

def add_node(name, x, y):
    cursor.execute("INSERT INTO Node (name, x, y) VALUES (?, ?, ?)", 
                   (name, x, y))
    conn.commit()

def add_order(pickup, delivery, owner_id):
    cursor.execute("INSERT INTO OrderItem (pickup_node, delivery_node, current_owner) VALUES (?, ?, ?)",
                   (pickup, delivery, owner_id))
    conn.commit()

# 新增 bundle 並加上多筆 order
def create_bundle(order_ids):
    # cursor.execute("INSERT INTO OrderBundle (name) VALUES (?)", 
    #                (bundle_name,))
    bundle_id = cursor.lastrowid
    for oid in order_ids:
        cursor.execute("INSERT INTO OrderBundleItem (bundle_id, order_id) VALUES (?, ?)", (bundle_id, oid))
    conn.commit()

# 執行交易：buyer 向 seller 購買 order
def perform_transaction(buyer_id, order_id):
    # 找出現在的擁有者
    cursor.execute("SELECT current_owner FROM OrderItem WHERE id = ?", 
                   (order_id,))
    seller_id = cursor.fetchone()[0]

    # 更新 order 的擁有者
    cursor.execute("UPDATE OrderItem SET current_owner = ? WHERE id = ?", 
                   (buyer_id, order_id))

    # 紀錄交易
    cursor.execute("INSERT INTO TransactionLog (buyer_id, seller_id, order_id, timestamp) VALUES (?, ?, ?, ?)",
                   (buyer_id, seller_id, order_id, datetime.utcnow().isoformat()))

    conn.commit()


# -------------------------------------------------
# CREATE INITIAL DATABASE
# -------------------------------------------------

def init_carrier():
    add_carrier("Carrier A")
    add_carrier("Carrier B")
    add_carrier("Carrier C")

def init_node():
    # ---------------------------------------------
    # Note: Nodes with odd nodeID are always pickup nodes, vv
    # ---------------------------------------------
    add_node("Subway Station",323,-298)
    add_node("Book Shop", 9,102)
    add_node("Supermarket",-386,-41)
    add_node("Fire Station",-55,107)
    add_node("Police Station",198,-44)
    add_node("Hospital",-210,234)
    add_node("Pharmacy",-386,114)
    add_node("Post Office",-123,168)
    add_node("City Hall",24,95)
    add_node("Public Library",234,-330)
    add_node("Elementary School",499,-90)
    add_node("High School",-137,-9)
    add_node("University",-195,-103)
    add_node("Bank",-466,-372)
    add_node("ATM",206,-100)
    add_node("Shopping Mall",-302,470)
    add_node("Convenience Store",225,120)
    add_node("Gas Station",155,325)
    add_node("Bus Stop",120,183)
    add_node("Train Station",124,441)
    add_node("Airport",19,401)
    add_node("Restaurant",-476,288)
    add_node("Cafe",-451,224)
    add_node("Bakery",367,-339)
    add_node("Bar",268,460)
    add_node("Cinema",-283,-245)
    add_node("Theater",-28,40)
    add_node("Museum",-329,330)
    add_node("Art Gallery",-466,338)
    add_node("Gym",400,105)
    add_node("Park",-308,491)
    add_node("Playground",295,-290)
    add_node("Swimming Pool",-304,-65)
    add_node("Stadium",256,256)
    add_node("Church",19,-403)
    add_node("Hotel",-185,-470)
    add_node("Hostel",154,246)
    add_node("Courthouse",-135,-307)
    add_node("Recycling Center",-471,-78)
    add_node("Parking Lot",-390,-91)
    add_node("Zoo",119,-19)
    add_node("Night Club", -220,19)

def init_order():
    add_order(3,22,2)
    add_order(23,8,2)
    add_order(31,20,3)
    add_order(5,10,1)
    add_order(41,26,3)
    add_order(7,38,2)
    add_order(17,12,3)
    add_order(9,18,2)
    add_order(29,30,1)
    add_order(13,40,2)
    add_order(33,16,2)
    add_order(27,6,3)
    add_order(35,36,2)
    add_order(37,14,3)
    add_order(21,2,1)
    add_order(1,4,2)
    add_order(25,32,3)
    add_order(39,28,1)


if __name__ == "__main__":
    # init_carrier()
    # init_node()
    # init_order()

    # # ---------------------------------------------
    # # Note: Not tested yet
    # # ---------------------------------------------
    # create_bundle([1,2])
    # create_bundle([6,8])
    # perform_transaction(buyer_id=2, order_id=1)

    # cursor.execute("DROP TABLE OrderBundleItem")
    # cursor.execute("DROP TABLE OrderBundle")
    # conn.commit()

    print("📦 資料庫初始化完成 & 測試資料寫入！")