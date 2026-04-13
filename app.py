from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "energy_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            voltage REAL,
            current REAL,
            power REAL,
            energy REAL,
            frequency REAL,
            pf REAL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return "IoT Energy Server is running!"


@app.route("/iot-data", methods=["GET"])
def iot_data():
    try:
        voltage = request.args.get("voltage", type=float)
        current = request.args.get("current", type=float)
        power = request.args.get("power", type=float)
        energy = request.args.get("energy", type=float)
        frequency = request.args.get("frequency", type=float)
        pf = request.args.get("pf", type=float)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO measurements (timestamp, voltage, current, power, energy, frequency, pf)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, voltage, current, power, energy, frequency, pf))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "status": "success",
            "id": new_id,
            "timestamp": timestamp,
            "data": {
                "voltage": voltage,
                "current": current,
                "power": power,
                "energy": energy,
                "frequency": frequency,
                "pf": pf
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/latest", methods=["GET"])
def latest():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, voltage, current, power, energy, frequency, pf
        FROM measurements
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"status": "empty", "message": "No data yet"})

    return jsonify({
        "id": row[0],
        "timestamp": row[1],
        "voltage": row[2],
        "current": row[3],
        "power": row[4],
        "energy": row[5],
        "frequency": row[6],
        "pf": row[7]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)