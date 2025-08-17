from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("devices.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect("devices.db")
    c = conn.cursor()
    c.execute("SELECT * FROM devices")
    devices = c.fetchall()

    # Stats
    total = len(devices)
    active = sum(1 for d in devices if d[3] == "Active")
    inactive = sum(1 for d in devices if d[3] == "Inactive")
    maintenance = sum(1 for d in devices if d[3] == "Maintenance")

    conn.close()
    return render_template("index.html", devices=devices, total=total, active=active, inactive=inactive, maintenance=maintenance)

@app.route('/add', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        name = request.form['name']
        dtype = request.form['type']
        status = request.form['status']
        conn = sqlite3.connect("devices.db")
        c = conn.cursor()
        c.execute("INSERT INTO devices (name, type, status) VALUES (?, ?, ?)", (name, dtype, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template("add_device.html")

@app.route('/delete/<int:id>')
def delete_device(id):
    conn = sqlite3.connect("devices.db")
    c = conn.cursor()
    c.execute("DELETE FROM devices WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render ka default port 10000 hai
    app.run(host="0.0.0.0", port=port, debug=False)
