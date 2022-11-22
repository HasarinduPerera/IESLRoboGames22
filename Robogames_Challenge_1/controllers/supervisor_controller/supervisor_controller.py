from controller import Robot, Supervisor, Emitter
import random, json
import math
from math import sqrt, acos, asin

EXCHANGE_RATE = 360

positions = set()
positions.add((0.84, -0.84))
positions.add((0.12, -0.84))
positions.add((-0.84, -0.84))
positions.add((-0.84, 0.12))
positions.add((0.12, 0.37))
positions.add((0.85, 0.62))

supervisor = Supervisor()
root_node = supervisor.getRoot()
children = root_node.getField("children")
timestep = int(supervisor.getBasicTimeStep())
collectibles = []
robot = supervisor.getFromDef('dave')
emitter = supervisor.getDevice("emitter")

rupees = 0
dollars = 0
currentTime = 0
goalPosition = (0.016, 1.096, 0)
walletCapacity = 3000

def placeCollectible(currentTime):
    if currentTime % 4992 == 0 and len(collectibles) < 2:
        position = random.sample(list(positions), 1)
        positions.remove(position[0])
        collectibleDef = "collectible" + str(currentTime)
        collectibleString = "DEF " + collectibleDef + " Ball { translation " + str(position[0][0]) + " " + str(position[0][1]) + " 0.03" + " color 1 0.6667 0 }"
        children.importMFNodeFromString(-1, collectibleString)
        collectibles.append(supervisor.getFromDef(collectibleDef))
    
def printScore():
    print("You have", rupees, "rupees and", dollars, "dollars")
    
def getDistance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
    
outside = True # To stop the score from printing repeatedly when inside goal
    
def detectCollisions():
    global rupees
    global outside
    global dollars
    global goalPosition

    robotPosition = robot.getPosition()
    
    for collectible in list(collectibles):
        collectiblePosition = collectible.getPosition()
        
        if getDistance(robotPosition, collectiblePosition) < 0.085:
            collectibles.remove(collectible)
            collectible.remove()
            positions.add((collectiblePosition[0], collectiblePosition[1]))
            rupees += 1000
            if rupees > walletCapacity:
                rupees = walletCapacity
            printScore()
            
    if getDistance(goalPosition, robotPosition) < 0.15:
        dollars += rupees / EXCHANGE_RATE
        rupees = 0
        
        if outside:
            printScore()
        
        outside = False
        
    else:
        outside = True
        
def sendData():
    global collectibles
    robotPosition = robot.getPosition()
    rotationMatrix = robot.getOrientation()
    angle, sign = acos(rotationMatrix[0]) / math.pi * 180, asin(rotationMatrix[3]) / math.pi * 180
    if sign < 0.0:
        angle *= -1
        angle += 360

    data = {}
    data["time"] = currentTime
    data["collectibles"] = []
    data["rupees"] = rupees
    data["dollars"] = dollars
    data["goal"] = (goalPosition[0], goalPosition[1])
    data["robot"] = (robotPosition[0], robotPosition[1])
    data["robotAngleDegrees"] = angle
    
    for collectible in collectibles:
        collectiblePosition = collectible.getPosition()
        data["collectibles"].append((collectiblePosition[0], collectiblePosition[1]))

    emitter.send(json.dumps(data).encode('utf-8'))
        
while supervisor.step(timestep) != -1:
    detectCollisions()
    placeCollectible(currentTime)
    sendData()
    currentTime += timestep
