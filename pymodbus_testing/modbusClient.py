from pymodbus.client import ModbusTcpClient

# Connect to the Modbus server
client = ModbusTcpClient('localhost', port=5020)
client.connect()

# Read the holding registers (temperature, speed, counter)
result = client.read_holding_registers(0, slave=1)  # Read registers 0-2
print(result)
temperature = result.registers[0] / 10.0
speed = result.registers[1] / 10.0
counter = result.registers[2]

# Read the coils (motor, valve)
result = client.read_coils(3, 2, slave=1)  # Read coils 3-4
motor_status = result.bits[0]
valve_status = result.bits[1]

print(f"Temperature: {temperature:.2f}°C, Speed: {speed:.2f} m/s, Counter: {counter}")
print(f"Motor: {'ON' if motor_status else 'OFF'}, Valve: {'OPEN' if valve_status else 'CLOSED'}")

# Disconnect the client
client.close()
