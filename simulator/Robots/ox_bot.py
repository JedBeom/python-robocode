#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math

class Ox(Robot): #Create a Robot

    def calcAngle(self, targetX, targetY):
        x = self.getPosition().x()
        y = self.getPosition().y()
        dx = x -targetX
        dy = y - targetY

        angle = 90 - math.degrees(math.atan(dy/dx))
        if x < targetX:
            angle *= -1
        else:
            angle = 180 - angle
        return angle, dx, dy
    
    def init(self):# NECESARY FOR THE GAME   To initialyse your robot     
        
        #Set the bot color in RGB
        self.setColor(204, 102, 0)
        self.setGunColor(255, 128, 0)
        self.setRadarColor(128, 255, 0)
        self.setBulletsColor(204, 0, 0)
        self.cnt = 0
        
        #get the map size
        self.size = self.getMapSize() #get the map size
        self.radarVisible(True) # show the radarField
        
        self.setRadarField("thin")
        self.round = 0
    
    def run(self): #NECESARY FOR THE GAME  main loop to command the bot
        self.round += 1
        pos = self.getPosition() #return the center of the bot
        self.x = pos.x() #get the x coordinate
        self.y = pos.y() #get the y coordinate

        if self.round == 1:
            if self.y >= self.size.height()//2: # 0도
                self.move(self.size.height()-self.y-50)
                self.stop()
                self.turn(90)
                self.stop()
            else: # 180도
                self.turn(180)
                self.stop()
                self.move(self.y-self.size.height()-50)
                self.stop()
                self.turn(90)
                self.stop()

            self.gunTurn(self.getHeading())
            self.radarTurn(self.getHeading())
            self.radarTurn(90) #to turn the radar (negative values turn counter-clockwise)
            self.gunTurn(90)
        else:
            self.move(100)
            self.stop()
            self.gunTurn(self.getHeading())
            self.radarTurn(self.getHeading())
            self.radarTurn(90) #to turn the radar (negative values turn counter-clockwise)
            self.gunTurn(90)
            
    def sensors(self):  #NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""
        
        pos = self.getPosition() #return the center of the bot
        x = pos.x() #get the x coordinate
        y = pos.y() #get the y coordinate
        
        angle1 = self.getGunHeading() #Returns the direction that the robot's gun is facing
        angle2 = self.getHeading() #Returns the direction that the robot is facing
        angle3 = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        list = self.getEnemiesLeft() #return a list of the enemies alive in the battle
        for robot in list:
            id = robot["id"]
            name = robot["name"]
            # each element of the list is a dictionnary with the bot's id and the bot's name
        
    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event)
        self.move(-200)
        self.stop()
        self.turn(270 - self.getHeading())
        self.stop()
        self.rPrint('ouch! a wall !')
    
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        self.rPrint('collision with:' + str(robotName)) #Print information in the robotMenu (click on the righ panel to see it)
       
    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event)
        self.rPrint ("hit by " + str(bulletBotName) + "with power:" +str(bulletPower))
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str(botId))
        
    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("forever")
    
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        self.fire(3)
        self.fire(3)
        self.fire(3)
        if self.cnt % 10 == 0:
            self.gunTurn(1)
            self.radarTurn(1)
            self.cnt += 1
        self.pause(1) #wait 10 frames
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))