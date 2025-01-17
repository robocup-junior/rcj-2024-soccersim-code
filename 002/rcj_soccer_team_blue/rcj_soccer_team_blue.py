from controller import Robot
from robot1 import MyRobot1
from robot2 import MyRobot2
from robot3 import MyRobot3

robot = Robot()
name = robot.getName()
robot_number = int(name[1])

if robot_number == 1:
    robot_controller = MyRobot1(robot)
    print("Starting Robot 1")
elif robot_number == 2:
    robot_controller = MyRobot2(robot)
    print("Starting Robot 2")
else:
    robot_controller = MyRobot3(robot)
    print("Starting Robot 3")

robot_controller.run()
