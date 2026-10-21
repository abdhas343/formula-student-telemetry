
import csv
import random
import time
import os

# Formula Student - Live Telemetry Simulator

os.makedirs("data", exist_ok=True)

speed = 0
temperature = 28.0
battery = 100.0

with open("data/live_telemetry.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Time",
        "Speed",
        "Temperature",
        "Battery",
        "Status"
    ])

    print("LIVE TELEMETRY SIMULATION STARTED")
    print("---------------------------------")

    for second in range(120):

        # Acceleration and braking cycles
        if second % 20 < 12:
            speed += random.randint(2, 7)
        else:
            speed -= random.randint(3, 8)

        speed = max(0, min(speed, 120))

        # Simulated battery temperature
        temperature += random.uniform(-0.2, 0.8)

        # Simulated battery consumption
        battery -= random.uniform(0.05, 0.15)
        battery = max(0, battery)

        # System diagnostics
        if temperature > 40:
            status = "WARNING"
        else:
            status = "NORMAL"

        writer.writerow([
            second,
            speed,
            round(temperature, 1),
            round(battery, 1),
            status
        ])

        # Make data available to dashboard
        file.flush()

        print(
            f"Time: {second}s | "
            f"Speed: {speed} km/h | "
            f"Temp: {temperature:.1f} C | "
            f"Battery: {battery:.1f}% | "
            f"Status: {status}"
        )

        time.sleep(1)

print("Simulation completed.")
