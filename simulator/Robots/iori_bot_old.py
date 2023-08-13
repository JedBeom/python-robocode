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

            print(f"target: {targetDegree:.2f}, now: {self.angleBot:.2f}")

            self.turn(targetDegree)
            self.radarTurn(targetDegree)
            self.gunTurn(targetDegree)

            self.pause(10)

            distance = math.sqrt(dx**2 + dy**2)
            self.move(distance)

            print(f"{distance} move completed")
            self.pause(10)
            
            return

        self.turn(self.clockwise*10)
        self.radarTurn(self.clockwise*10)
        self.gunTurn(self.clockwise*10)

        if self.round%4 == 0:
            self.move(self.round // 4)
        
        
    def sensors(self):  #NECESARY FOR THE GAME
        """Tick each frame to have datas about the game"""
        
        # self.pos = self.getPosition() #return the center of the bot
        self.angleGun = self.getGunHeading() #Returns the direction that the robot's gun is facing
        self.angleBot = self.getHeading() #Returns the direction that the robot is facing
        self.angleRadar = self.getRadarHeading() #Returns the direction that the robot's radar is facing
        self.leftEnemies = self.getEnemiesLeft() #return a list of the enemies alive in the battle
        
    def onHitByRobot(self, robotId, robotName):
        self.rPrint("damn a bot collided me!")

    def onHitWall(self):
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 

        self.move(-10)
        self.turn(30)
        self.rPrint('ouch! a wall !')
    
    def onRobotHit(self, robotId, robotName): # when My bot hit another
        self.rPrint('collision with:' + str(robotName)) #Print information in the robotMenu (click on the righ panel to see it)
       
    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): #NECESARY FOR THE GAME
        """ When i'm hit by a bullet"""
        self.reset() #To reset the run fonction to the begining (auomatically called on hitWall, and robotHit event) 
        self.move(-20)
        self.rPrint ("hit by " + str(bulletBotName) + "with power:" +str( bulletPower))
        
    def onBulletHit(self, botId, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a bot"""
        self.rPrint ("fire done on " +str( botId))

    def onBulletMiss(self, bulletId):#NECESARY FOR THE GAME
        """when my bullet hit a wall"""
        self.rPrint ("the bullet "+ str(bulletId) + " fail")
        self.pause(1) #wait 10 frames
        
    def onRobotDeath(self):#NECESARY FOR THE GAME
        """When my bot die"""
        self.rPrint ("damn I'm Dead")
    
    def onTargetSpotted(self, botId, botName, botPos):#NECESARY FOR THE GAME
        "when the bot see another one"
        
        self.clockwise = 0
        angle = self.calcAngle(botPos.x(), botPos.y())[0]
        print("target angle:", angle)
        self.radarTurn(angle - self.angleRadar)
        self.gunTurn(angle - self.angleGun)
        self.fire(3)
        self.rPrint("I see the bot:" + str(botId) + "on position: x:" + str(botPos.x()) + " , y:" + str(botPos.y()))

        self.clockwise = 1
    
