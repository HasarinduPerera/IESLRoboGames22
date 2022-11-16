from controller import Robot
from controller import Receiver
import json

robot = Robot()
timestep = int(robot.getBasicTimeStep())
receiver = robot.getDevice("receiver")
receiver.enable(10)

left = robot.getDevice('left wheel motor')
right = robot.getDevice('right wheel motor')

left.setPosition(float("inf"))
right.setPosition(float("inf"))

left.setVelocity(3.0)
right.setVelocity(3.0)

while robot.step(timestep) != -1:
    while receiver.getQueueLength() > 0:
        receiver_data = json.loads(receiver.getData().decode('utf-8'))
        time = receiver_data['time']
        collectibles = receiver_data['collectibles']
        rupees = receiver_data['rupees']
        dollars = receiver_data['dollars']
        goal = receiver_data['goal']
        # debug data extraction
        print(time, collectibles, rupees, dollars, goal)
        
        
        
        
        receiver.nextPacket()
    pass
    