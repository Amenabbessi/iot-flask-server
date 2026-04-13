from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "IoT Flask Server is running!"

@app.route('/iot-data', methods=['GET', 'POST'])
def iot_data():
    if request.method == 'GET':
        voltage = request.args.get("voltage")
        current = request.args.get("current")
        power = request.args.get("power")
        energy = request.args.get("energy")
        frequency = request.args.get("frequency")
        pf = request.args.get("pf")

        data = {
            "voltage": voltage,
            "current": current,
            "power": power,
            "energy": energy,
            "frequency": frequency,
            "pf": pf
        }
    else:
        data = request.get_json()
        if data is None:
            return {"error": "No JSON received"}, 400

    print("Received:", data)

    with open("data.txt", "a") as f:
        f.write(str(data) + "\n")

    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)