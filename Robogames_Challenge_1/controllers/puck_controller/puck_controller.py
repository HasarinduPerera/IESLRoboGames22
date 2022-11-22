from controller import Robot
from controller import Receiver
import json

robot = Robot()
timestep = int(robot.getBasicTimeStep())
receiver = robot.getDevice("receiver")
receiver.enable(10)

# Motor setup
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

left_motor.setVelocity(3.0)
right_motor.setVelocity(3.0)

# PS setup
left_proximity_sensor = robot.getDevice('ps7')
right_proximity_sensor = robot.getDevice('ps0')

left_proximity_sensor.enable(timestep)
right_proximity_sensor.enable(timestep)

# Camera setup
camera = robot.getDevice('camera')
camera.enable(timestep)


while robot.step(timestep) != -1:

    while receiver.getQueueLength() > 0:
        # Assign receiver values
        receiver_data = json.loads(receiver.getData().decode('utf-8'))
        time = receiver_data['time']
        collectibles = receiver_data['collectibles']
        rupees = receiver_data['rupees']
        dollars = receiver_data['dollars']
        goal = receiver_data['goal']
        robot = receiver_data['robot']
        robotAngleDegrees = receiver_data['robotAngleDegrees']
        
        print(time, collectibles, rupees, dollars, goal, robot, robotAngleDegrees) # debug data extraction
        
        # get values from PS
        left_ps_value = left_proximity_sensor.getValue()
        right_ps_value = right_proximity_sensor.getValue()
        
        print(left_ps_value, right_ps_value) # Debug PS
        
        # Simple OA
        if left_ps_value > 90 and right_ps_value < left_ps_value:
            left_motor.setVelocity(0.0)
            right_motor.setVelocity(4.0)
        elif right_ps_value > 90 and right_ps_value > left_ps_value:
            left_motor.setVelocity(0.0)
            right_motor.setVelocity(4.0)
        else:
            left_motor.setVelocity(3.0)
            right_motor.setVelocity(3.0)
            
        
        
        
        receiver.nextPacket()
    pass