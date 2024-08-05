import math
import utils
import struct
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import time
import json


data = ""
team_data = ""
ball_data = ""
heading = ""
robot_pos = ""
direction = ""
robot_x = ""
robot_y = ""
robot_angle = ""
ball_x = 0.0
ball_y = 0.0
toop_be_zamin_x = 0
toop_be_zamin_y = 0
Flag_Loop = 0 
ball_dist = 0
ball_angle=0
last_ball_dist=0
ball_av=0
last_ball_x=0.0
last_ball_angle=0
strength=0.0
last_toop_be_zamin_x=0.0
robot3_pos=0
robot2_pos=0
robo1_pos=0
newbally2=0
newballx2=0
newbally3=0
newballx3=0
robotnumb=0
predictedX=0
robot1Datavalid=0
robot2Datavalid=0
robot3Datavalid=0
othersBallx=0
othersBally=0
othersBallxFinal=0
othersBallyFinal=0
robotNumber=0
is_turning=0
strength_robot3=0
ManRaftam=False
zavie_toop_be_robot=0
RedFlagRast=0
RedFlagChap=0


ASHAR = 3



class MyRobot1(RCJSoccerRobot):


    def sensors_update(self):
        global data
        global team_data
        global ball_data
        global heading
        global robot_pos
        global sonar_values
        global direction
        global robot_x
        global robot_y
        global robot_angle
        global ball_x
        global ball_y
        global ball_dist
        global ball_angle
        global ball_av
        global ball_dist
        global last_ball_dist
        global last_ball_x
        global strength
    
        data = self.get_new_data()
        while self.is_new_team_data():
            team_data = self.get_new_team_data()
        robot_angle = math.degrees(self.get_compass_heading())
        if robot_angle < 0:
            robot_angle += 360
        robot_pos = self.get_gps_coordinates()

        if self.name[0] == "B":
            robot_x = robot_pos[0]

            robot_y = robot_pos[1]
        else:
            robot_x = -robot_pos[0]
            robot_y = -robot_pos[1]
        robot_x = round(robot_x, ASHAR)
        robot_y = round(robot_y, ASHAR)

        sonar_values = self.get_sonar_values()
        if self.is_new_ball_data():
            ball_data = self.get_new_ball_data()
            last_ball_x=ball_x
            ball_x = ball_data["direction"][0]
            ball_y = ball_data["direction"][1]
            direction = utils.get_direction(ball_data["direction"])
            strength = ball_data["strength"]
        else:
            ball_data = None
            direction = None

        ball_angle = math.atan2(ball_y, ball_x)
        ball_angle = math.degrees(ball_angle)


    def move(self, left_speed, right_speed):
        left_speed,right_speed = right_speed,left_speed
        left_speed = min(max(left_speed, -10) , 10)
        right_speed = min(max(right_speed, -10) , 10)
        self.left_motor.setVelocity(left_speed)
        self.right_motor.setVelocity(right_speed)



    def go_to(self, x_maghsad, y_maghsad):

        delta_x = x_maghsad - robot_x
        delta_y = y_maghsad - robot_y
        zavie_maghsad = math.atan2(delta_y, delta_x) * (180 / math.pi)
        zavie_maghsad = (zavie_maghsad - 90)
        if zavie_maghsad < 0:
            zavie_maghsad += 360
        error_zavie = zavie_maghsad - robot_angle
        error_zavie = error_zavie - 180
        if error_zavie > 180:
            error_zavie -= 360
        elif error_zavie < -180:
            error_zavie += 360
        error_zavie = error_zavie * 3
        error_fasele = math.sqrt((x_maghsad - robot_x)**2 + (y_maghsad - robot_y)**2)
        if error_fasele < 0.5:
            error_fasele = round(error_fasele * 180,3)
        else:
            error_fasele = round(error_fasele * 50,3)
        error = error_zavie
        self.move(error_fasele - error+10, error_fasele + error+10)


    def Move_Loop(self, x, y):
        global Flag_Loop
        if x - 0.01 <= robot_x <= x + 0.01 and y - 0.01 < robot_y <= y + 0.01:
            Flag_Loop = 1
        elif -x - 0.01 <= robot_x <= -x + 0.01 and y - 0.01 < robot_y <= y + 0.01:
            Flag_Loop = 0
        if Flag_Loop == 0:
            self.go_to(x, y)
        elif Flag_Loop == 1:
            self.go_to(-x, y)


    def toop_be_zamin_update(self):
        global toop_be_zamin_x
        global toop_be_zamin_y
        global ball_dist
        global ball_angle
            
        r = 0.11886 * ball_dist - 0.02715


        ball_angle = math.atan2(ball_y, ball_x)
        ball_angle = math.degrees(ball_angle)
        if ball_angle < 0:
            ball_angle += 360
        theta = (ball_angle+robot_angle+90) % 360
        if theta < 0:
            theta += 360


        theta = math.radians(theta)
        pos_x = r * math.cos(theta)
        pos_y = r * math.sin(theta)
        pos_x = round(pos_x, ASHAR)
        pos_y = round(pos_y, ASHAR)          
        toop_be_zamin_x = robot_x + 2.5 * pos_x
        toop_be_zamin_y = robot_y + 1 * pos_y
        toop_be_zamin_x = round(toop_be_zamin_x, ASHAR)
        toop_be_zamin_y = round(toop_be_zamin_y, ASHAR)

    def turn(self):

        global is_turning
        global robot3Datavalid
        global robot2Datavalid
        global othersBallxFinal
        global othersBallyFinal
        global othersBally
        global othersBallx
        global zavie_robot_be_darvaze
        global zavie_toop_be_robot

        zavie_robot_be_darvaze = math.degrees(math.atan2(0, -0.75))
        last_zavie_toop_be_robot=zavie_toop_be_robot
        zavie_toop_be_robot=(robot_angle+ball_angle)%360

        if toop_be_zamin_y > robot_y:
            is_turning = 1
        if zavie_toop_be_robot > 350 or zavie_toop_be_robot < 10:
            is_turning = 0


        if ball_data!= None:

            if is_turning == 0 :

                if 330>zavie_toop_be_robot>30 :
                    self.gotoTheta(zavie_toop_be_robot - 90)
                else:
                    if strength>100 :
                        self.go_to(0,-0.6)
                    else:
                        self.gotoTheta(zavie_toop_be_robot - 90)

            elif is_turning==1:

                if robot_y<-0.55 and -0.4<robot_x<0.4 :
                    self.go_to(toop_be_zamin_x,toop_be_zamin_y)
                elif toop_be_zamin_x < robot_x:
                    self.gotoTheta(zavie_toop_be_robot - 90 - strength / 1.5)
                elif toop_be_zamin_x > robot_x:
                    self.gotoTheta(zavie_toop_be_robot - 90 + strength / 1.5)

                
        else:
            

            othersBallx = 0
            numberOfValidDatas = 0
            if robot3Datavalid == True:
                othersBallx = othersBallx + newballx3
                numberOfValidDatas += 1
            if robot2Datavalid == True:
                othersBallx = othersBallx + newballx2
                numberOfValidDatas += 1
            if numberOfValidDatas > 0:
                othersBallxFinal = othersBallx / numberOfValidDatas

            othersBally = 0
            numberOfValidDatas = 0
            if robot3Datavalid == True:
                othersBally = othersBally + newbally3
                
                numberOfValidDatas += 1
            if robot2Datavalid == True:
                othersBally = othersBally + newbally2
                robot2Datavalid = False
                numberOfValidDatas += 1
            if numberOfValidDatas > 0:
                othersBallyFinal = othersBally / numberOfValidDatas


            if newbally3<0.2 :
                if robot3Datavalid == True:
                    if strength_robot3<10:
                        self.go_to(othersBallxFinal,othersBallyFinal)
                    elif strength_robot3>10 and robot_y<0.4:
                        self.go_to(-othersBallxFinal/3,othersBallyFinal+0.1)
                    elif strength_robot3>10 and robot_y>0.4:
                        self.go_to(0, 0.4)
                elif robot3Datavalid == False:
                    self.go_to(-0.35,-0.2)
            else:
                self.go_to(-0.35,-0.2)


    def gotoTheta(self,moveTheta):
        self.go_to(robot_x+math.cos(moveTheta * 0.0174532925199433)*0.05, robot_y+math.sin(moveTheta * 0.0174532925199433)*0.05)

    def goal_keeper(self):

        
        global othersBally
        global othersBallx
        global robot2Datavalid
        global robot3Datavalid
        global othersBallxFinal
        global othersBallyFinal


        if ball_data != None:
        

            if toop_be_zamin_y<robot_y :

                if robot_x>0 and robot_x<0.3 or robot_x<0 and robot_x>-0.3 :
                    self.go_to(toop_be_zamin_x,0.55)
                elif robot_x>0:
                    self.go_to(0.3,0.55)
                elif robot_x<0:
                    self.go_to(-0.3,0.55)
            elif toop_be_zamin_y>robot_y and robot_x>0:
                self.go_to(0.3,toop_be_zamin_y)
            elif toop_be_zamin_y>robot_y and robot_x<0:
                self.go_to(-0.3,toop_be_zamin_y)
            else:
                self.go_to(0.3,0.55)

        else:
            
            othersBallx = 0
            numberOfValidDatas = 0
            if robot2Datavalid == True:
                othersBallx = othersBallx + newballx2
                numberOfValidDatas += 1
            if robot3Datavalid == True:
                othersBallx = othersBallx + newballx3
                numberOfValidDatas += 1
            if numberOfValidDatas > 0:
                othersBallxFinal = othersBallx / numberOfValidDatas
            

            othersBally = 0
            numberOfValidDatas = 0
            if robot2Datavalid == True:
                othersBally = othersBally + newbally2
                robot2Datavalid = False
                numberOfValidDatas += 1
            if robot3Datavalid == True:
                othersBally = othersBally + newbally3
                robot3Datavalid = False
                numberOfValidDatas += 1
            if numberOfValidDatas > 0:
                othersBallyFinal = othersBally / numberOfValidDatas

            
            
            if othersBallyFinal<robot_y :

                ManRaftam=False

                if robot_x>0 and robot_x<0.3 or robot_x<0 and robot_x>-0.3 :
                    self.go_to(othersBallxFinal,0.55)
                elif robot_x>0:
                    self.go_to(0.3,0.55)
                elif robot_x<0:
                    self.go_to(-0.3,0.55)
            elif othersBallyFinal>robot_y and robot_x>0:
                self.go_to(0.3,othersBallyFinal)
            elif toop_be_zamin_y>robot_y and robot_x<0:
                self.go_to(-0.3,othersBallyFinal)
            else:
                self.go_to(0.3,0.55)

            



    def send_data(self):


        if ball_data!=None:

            robot1Datavalid==True

            data = {"robotnumb":1,"ball_x": toop_be_zamin_x,"ball_y": toop_be_zamin_y,"goalkeepersit":ManRaftam,"robot_x":robot_x,"robot_y":robot_y,"redflagrast":RedFlagRast,"redflagchap":RedFlagChap}
            packet = json.dumps(data)
            self.team_emitter.send(packet)

        else:

            robot1Datavalid==False
            data = {"robotnumb":1,"no_data":robot1Datavalid,"goalkeepersit":ManRaftam,"robot_x":robot_x,"robot_y":robot_y,"redflagrast":RedFlagRast,"redflagchap":RedFlagChap}
            packet = json.dumps(data)
            self.team_emitter.send(packet)


    def receive_data(self):

        global robot2Datavalid
        global robot3Datavalid
        global newballx2
        global newballx3
        global newbally2
        global newbally3
        global robotNumber
        global strength_robot3

        while self.team_receiver.getQueueLength() > 0:
                
            self.team_receiver.getQueueLength()
            packet = self.team_receiver.getString()
            self.team_receiver.nextPacket()
            data = json.loads(packet)


            for key, value in data.items():


                if key=='robotnumb' and value==2:
                    robotNumber = 2
                if robotNumber == 2:
                    if key == 'ball_x':
                        newballx2=value
                    elif key == 'ball_y':
                        newbally2=value
                        robot2Datavalid = True
                        
                if key=='robotnumb' and value==3:
                    robotNumber = 3

                if robotNumber == 3:

                    if key == 'ball_x':
                        newballx3=value
                    elif key=="strength":
                        strength_robot3=value
                    elif key == 'ball_y':
                        newbally3=value
                        robot3Datavalid = True

    def Sos(self):

        global RedFlagRast
        global RedFlagChap

        if -0.32<robot_x<-0.1 and strength>=20:
            if robot_y>0.6:
                RedFlagRast=1
        elif 0.32>robot_x>0.1 and strength>=20:
            if robot_y>0.6:
                RedFlagChap=1
        else:
            RedFlagRast=0
            RedFlagChap=0



    def run(self):

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        while self.robot.step(TIME_STEP) != -1 :

            self.send_data()
            self.receive_data()

            if self.is_new_data():

                global ManRaftam

                self.sensors_update()
                self.toop_be_zamin_update()
                self.Sos()

                self.goal_keeper()
                

                self.send_data_to_team(self.player_id)

