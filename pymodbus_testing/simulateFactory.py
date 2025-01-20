import random
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
#from pymodbus.transaction import ModbusRtuFramer

# Generate random sensor values
def generate_sensor_data():
    temperature = random.uniform(20.0, 30.0)  # Simulating temperature between 20 and 30 degrees Celsius
    speed = random.uniform(1.0, 10.0)  # Simulating speed between 1 and 10 m/s
    counter = random.randint(0, 100)  # Simulating a counter with a random integer between 0 and 100
    return temperature, speed, counter

# Set up the Modbus datastore and context
def create_modbus_server():
    # Create Modbus slave context (holds the registers)
    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(3, [1, 2, 3])  # Define 3 holding registers (for temperature, speed, counter)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    return context, store

# Set values in the Modbus holding registers (simulate sensor data)
def update_modbus_registers(store):
    temperature, speed, counter = generate_sensor_data()
    
    # Store the values into the holding registers
    store.setValues(3, 0, [int(temperature * 10)])  # Temperature register (scaled by 10)
    store.setValues(3, 1, [int(speed * 10)])  # Speed register (scaled by 10)
    store.setValues(3, 2, [counter])  # Counter register

    # Print values for debugging
    print(f"Updated Sensor Values -> Temperature: {temperature:.2f}°C, Speed: {speed:.2f} m/s, Counter: {counter}")

# Start the Modbus server and continuously update values
def start_modbus_server():
    context, store = create_modbus_server()
    
    # Start the Modbus TCP server on port 5020
    print("Starting Modbus server on localhost:5020...")
    try:
        while True:
            update_modbus_registers(store)  # Update the registers with new sensor values
            StartTcpServer(context, address=("127.0.0.1", 5020))  # Start the server
            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        print("Modbus server stopped.")

if __name__ == "__main__":
    start_modbus_server()
