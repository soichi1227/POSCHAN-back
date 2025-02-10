import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect("pos_app.db")
cursor = conn.cursor()

# ✅ 外部キー制約を有効化
cursor.execute("PRAGMA foreign_keys = ON;")


# 商品マスタテーブルの作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS product_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    price INTEGER NOT NULL
);
""")

# 取引テーブルの作成（テーブル名を transactions に変更）
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datetime TEXT NOT NULL,
    emp_code TEXT NOT NULL,
    store_code TEXT NOT NULL,
    pos_no TEXT NOT NULL,
    total_amt INTEGER NOT NULL
);
""")

# 取引明細テーブルの作成（外部キー参照の修正）
cursor.execute("""
CREATE TABLE IF NOT EXISTS transaction_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_code TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_price INTEGER NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),  -- 修正
    FOREIGN KEY (product_id) REFERENCES product_master(id)
);
""")

# サンプル商品データ投入
cursor.executemany("INSERT OR IGNORE INTO product_master (code, name, price) VALUES (?, ?, ?)", [
    ("12345678901", "おーいお茶", 150),
    ("98765432101", "ソフラン", 300),
    ("11122233344", "福島産お米", 188),
])

# 変更を保存
conn.commit()
conn.close()

print("データベース初期化完了")
