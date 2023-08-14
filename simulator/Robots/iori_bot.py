#! /usr/bin/python
#-*- coding: utf-8 -*-

from robot import Robot #Import a base Robot
import math


class IoriBot(Robot): #Create a Robot

    size = 0
    angleGun = 0
    angleBot = 0
    angleRadar = 0
    leftEnemies = []
    clockwise = 1
    round = 0
    spottedStep = 0

    
    def init(self):# NECESARY FOR THE GAME   To initialyse your robot
        
        #Set the bot color in RGB
        self.setColor(253, 153, 225)
        self.setGunColor(253, 153, 225)
        self.setRadarColor(253, 153, 225)
        self.setBulletsColor(253, 153, 225)
        
        self.radarVisible(True) # show the radarField
        self.setRadarField("thin")
        self.size = self.getMapSize()
        self.getPos = self.getPosition

        self.centerX = self.size.width() // 2
        self.centerY = self.size.height() // 2

    
    def calcAngle(self, targetX, targetY):
        x = self.getPosition().x()
        y = self.getPosition().y()
        dx = x - targetX
        dy = y - targetY

        angle = 90 - math.degrees(math.atan(dy/dx))
        if x < targetX:
            angle *= -1
        else:
            angle = 180 - angle

        return angle, dx, dy


    
    def run(self): #NECESARY FOR THE GAME  main loop to command the bot
        self.round += 1

        if self.round == 1:
            targetDegree, dx, dy = self.calcAngle(self.centerX, self.centerY)


            self.turn(targetDegree)
            self.turnRadarAndGun(targetDegree)

            self.pause(10)

            distance = math.sqrt(dx**2 + dy**2)
            self.move(distance)

            self.pause(10)
            
            return

        self.turnRadarAndGun(self.clockwise*10)

        if self.round%4 == 0:
            self.turn(self.round)
            self.move(self.round // 4)
        
    def sensors(self):  #NECESARY FOR THE GAME
        self.angleGun = self.getGunHeading() #Returns the direction that the robot's gun is facing
        self.angleBot = self.getHeading() #Returns the direction that the robot is facing
        self.angleRadar = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        self.leftEnemies = self.getEnemiesLeft() #return a list of the enemies alive in the battle
        
    def onHitByRobot(self, robotId, robotName):
        pass

    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 

        self.move(-10)
        self.turn(30)
        self.rPrint('ouch! a wall !')
    
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        pass
       
    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.move(-20)
        self.turn(10)
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        pass

    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        self.pause(1) #wait 10 frames
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        pass
    
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        self.spottedStep += 1

        dx = botPos.x() - self.getPosition().x()
        dy = botPos.y() - self.getPosition().y()

        distance = math.sqrt(dx**2 + dy**2)

        try:
            angle = self.calcAngle(botPos.x(), botPos.y())[0]
        except ZeroDivisionError:
            angle = 180
            if botPos.x() > self.getPosition().x():
                angle = 0

        if distance <= 500:

            weight = 1
            angleDiff = angle - self.angleRadar

            if angleDiff > 180:
                angleDiff -= 360
            elif angleDiff < -180:
                angleDiff += 360

            self.turnRadarAndGun((angleDiff)*weight)

            if self.spottedStep%4 == 0:
                self.fire(7)
        else:
            self.turn(angle - self.angleBot)
            self.move(distance//3)

        if self.spottedStep%2 == 0:
            self.clockwise *= -1

    def turnRadarAndGun(self, angle):
        self.radarTurn(angle)
        self.gunTurn(angle)
