
import random
import csv
import os

# Formula Student Telemetry System

speed = 0
temperature = 28
battery = 100

# Create data folder
os.makedirs("data", exist_ok=True)

# Open CSV file
with open("data/telemetry.csv", "w", newline="") as file:

    writer = csv.writer(file)

    # Column names
    writer.writerow([
        "Time",
        "Speed",
        "Temperature",
        "Battery",
        "Status"
    ])

    print("FORMULA STUDENT TELEMETRY")
    print("-------------------------------")

    for second in range(20):

        # Acceleration and braking
        if second < 10:
            speed += random.randint(2, 8)
        else:
            speed -= random.randint(2, 6)

        speed = max(0, speed)

        # Battery temperature
        temperature += random.uniform(0.2, 1.5)

        # Battery consumption
        battery -= random.uniform(0.1, 0.5)

        # Temperature warning
        if temperature > 40:
            status = "WARNING"
        else:
            status = "NORMAL"

        # Save measurement to CSV
        writer.writerow([
            second,
            speed,
            round(temperature, 1),
            round(battery, 1),
            status
        ])

        # Display in terminal
        print(
            f"Time: {second}s | "
            f"Speed: {speed} km/h | "
            f"Temp: {temperature:.1f} C | "
            f"Battery: {battery:.1f}% | "
            f"Status: {status}"
        )

print("-------------------------------")
print("Telemetry data saved successfully!")


