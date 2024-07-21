from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Function to get stock data with pagination and include R&D / Rev
def get_stock_data(page, per_page):
    offset = (page - 1) * per_page
    conn = sqlite3.connect('stocks_data.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM stocks')
    total_records = cursor.fetchone()[0]
    
    cursor.execute('''
    SELECT s.*, k.value as rd_rev
    FROM stocks s
    LEFT JOIN key_metrics k
    ON s.ticker_id = k.ticker_id AND k.key = 'researchAndDevelopementToRevenueTTM'
    LIMIT ? OFFSET ?
    ''', (per_page, offset))
    
    data = cursor.fetchall()
    conn.close()
    
    return data, total_records

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data, total_records = get_stock_data(page, per_page)
    total_pages = (total_records + per_page - 1) // per_page
    return render_template('index.html', data=data, page=page, per_page=per_page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
