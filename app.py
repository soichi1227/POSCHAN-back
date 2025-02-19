from fastapi import FastAPI, HTTPException
import sqlite3
from sqlalchemy import  text
from pydantic import BaseModel
from datetime import datetime
from typing import List
from sqlalchemy.orm import sessionmaker
from db_control.connect import engine

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

import os

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://tech0-gen8-step4-pos-app-65.azurewebsites.net"],  # フロントエンドを許可
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST などすべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# 商品検索用のリクエストモデル
class ProductSearchRequest(BaseModel):
    code: str

# 購入リクエストモデル
class PurchaseItem(BaseModel):
    code: str
    quantity: int

class PurchaseRequest(BaseModel):
    emp_code: str
    store_code: str
    pos_no: str
    items: List[PurchaseItem]

@app.get("/")
def read_root():
    return {"message": "Welcome to POS API"}

# 商品検索API
@app.get("/product/{code}")
def get_product(code: str):
    # セッションの構築
    Session = sessionmaker(bind=engine)
    session = Session()
    # SQLを直接実行
    result = session.execute(
    text("SELECT PRD_ID, NAME, PRICE FROM m_product_sou WHERE CODE = :code"), 
        {"code": code}  
    )
    # 最初の行を取得
    product = result.fetchone()
    
    # conn = sqlite3.connect("pos_app.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT id, name, price FROM product_master WHERE code = ?", (code,))
    # product = cursor.fetchone()
    # conn.close()

    # セッションを閉じる
    session.close()
    print(product)
    if product:
        return {"id": product[0], "name": product[1], "price": product[2]}
    else:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    
    

# 購入API
@app.post("/purchase")
def purchase(request: PurchaseRequest):
    conn = sqlite3.connect("pos_app.db")
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO transaction (datetime, emp_code, store_code, pos_no, total_amt) VALUES (?, ?, ?, ?, ?)",
                (now, request.emp_code, request.store_code, request.pos_no, 0))
    transaction_id = cursor.lastrowid

    total_amount = 0
    for item in request.items:
        cursor.execute("SELECT PRD_ID, NAME, PRICE FROM m_product_sou WHERE CODE = ?", (item.code,))
        product = cursor.fetchone()
        if product:
            cursor.execute("INSERT INTO transaction_detail (transaction_id, product_id, product_code, product_name, product_price) VALUES (?, ?, ?, ?, ?)",
                        (transaction_id, product[0], item.code, product[1], product[2]))
            total_amount += product[2] * item.quantity
        else:
            conn.rollback()
            conn.close()
            raise HTTPException(status_code=400, detail=f"商品コード {item.code} が無効です")

    cursor.execute("UPDATE transaction SET total_amt = ? WHERE id = ?", (total_amount, transaction_id))
    conn.commit()
    conn.close()

    return {"success": True, "transaction_id": transaction_id, "total_amount": total_amount}
