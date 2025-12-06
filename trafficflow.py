from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load dataset
def load_data():
    file_path = "C:/Users/HP/Desktop/TrafficFlow Prediction/vehicle_data_with_city.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

@app.route('/')
def index():
    return render_template('index.html', cities=df["City"].unique())

@app.route('/predict', methods=['POST'])
def predict():
    frame = int(request.form['frame'])
    car_count = int(request.form['car_count'])
    truck_count = int(request.form['truck_count'])
    bike_count = int(request.form['bike_count'])
    bus_count = int(request.form['bus_count'])
    other_vehicle_count = int(request.form['other_vehicle_count'])
    city = request.form['city']
    weather_condition = request.form['weather_condition']
    time_of_day = request.form['time_of_day']
    day_of_week = request.form['day_of_week']

    total_vehicles = car_count + truck_count + bike_count + bus_count + other_vehicle_count
    vehicle_density = round(total_vehicles / frame, 2) if frame != 0 else 0

    if vehicle_density > 10:
        traffic_condition = "High Traffic (Congested)"
    elif 5 <= vehicle_density <= 10:
        traffic_condition = "Moderate Traffic"
    else:
        traffic_condition = "Low Traffic (Free Flow)"

    severity = "Low" if vehicle_density <= 5 else "Moderate" if vehicle_density <= 10 else "High"
    
    vehicle_counts = {
        'Cars': car_count,
        'Trucks': truck_count,
        'Bikes': bike_count,
        'Buses': bus_count,
        'Other Vehicles': other_vehicle_count
    }

    bar_chart = generate_chart(vehicle_counts, "Vehicle Counts by Type", "Vehicle Type", "Count")
    density_chart = generate_chart({"Predicted Density": vehicle_density}, "Predicted Vehicle Density", "", "Density")
    
    return render_template('result.html', traffic_condition=traffic_condition, total_vehicles=total_vehicles, 
                           vehicle_density=vehicle_density, severity=severity, city=city, 
                           bar_chart=bar_chart, density_chart=density_chart)

def generate_chart(data, title, xlabel, ylabel):
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values(), color='skyblue')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
