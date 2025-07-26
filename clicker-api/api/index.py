from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "API çalışıyor!"})

@app.route("/market", methods=["GET"])
def get_market():
    category = request.args.get("category")
    conn = get_db()
    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT * FROM products WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    products = [dict(row) for row in rows]
    return jsonify(products)

@app.route("/add", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    account = data.get("account")

    if not name or not category or not price or not account:
        return jsonify({"error": "Eksik bilgi"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, price, account) VALUES (?, ?, ?, ?)",
        (name, category, price, account)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Ürün eklendi"})

@app.route("/buy", methods=["POST"])
def buy_product():
    data = request.get_json()
    product_id = data.get("id")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Ürün bulunamadı"}), 404

    account = row["account"]
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Satın alındı", "account": account})
