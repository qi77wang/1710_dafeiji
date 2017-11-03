#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File Name: 01_搭建界面.py
# Author: wangqi
# mail: qi77wang@163.com
# Created Time: 2017年10月24日 星期二 16时10分52秒

import pygame
import time
import random

#导入按键的检测
from pygame.locals import *

class Plane(object):
    """docstring for Plane"""
    def __init__(self, screen, name):
        self.screen = screen

        #存储飞机发射的子弹
        self.bulletList = []
        #设置飞机图片
        self.image = pygame.image.load(self.imageName).convert()
        self.name = name

    def display(self):
        #更新飞机的位置
        self.screen.blit(self.image, (self.x, self.y))

        #判断一下子弹的位置是否越界，如果是，那么就要删除这颗子弹
        #
        #这种方法会漏掉很多需要删除的数据
        # for i in self.bulletList:
        #     if i.y<0:
        #         self.bulletList.remove(i)

        needDelItemList = []
        
        for tmpBullet in self.bulletList:
            #if tmpBullet.y < 0,也可以，但不好，尽量不要直接调用对象的属性，尽量封装
             if tmpBullet.judgeOut():
            # if tmpBullet.y < 0:
                needDelItemList.append(tmpBullet)
        
        # print(len(needDelItemList))

        for tmpRemove in needDelItemList:
            self.bulletList.remove(tmpRemove)

        # print(len(self.bulletList))

        #显示子弹的位置，放在此处有考究，放到main中有点面向过程的意思，故放在飞机类中
        for bullet in self.bulletList:
            bullet.display()

            #修改所有子弹的位置，放在此处有考究，让子弹显示的逻辑是，整个程序在不停的刷新显示，
            #每次修改子弹的位置，刷新起来，看起来子弹就动了，所以在显示这里加上子弹move动作
            bullet.move()

    def shootBullet(self):
        newBullet = PublicBullet(self.x, self.y, self.screen, self.name)
        self.bulletList.append(newBullet)

class HeroPlane(Plane):
    """docstring for HeroPlane"""
    def __init__(self, screen, name):

        #设置飞机的默认位置        
        self.x = 230
        self.y = 600

        self.screen = screen

        #设置飞机图片
        self.imageName = "./feiji/hero.gif"
        super().__init__(screen, name)

    def moveLeft(self):
        self.x -= 10
    
    def moveRight(self):
        self.x += 10

    def moveUp(self):
        self.y -= 10

    def moveDown(self):
        self.y += 10



class EnemyPlane(Plane):
    """docstring for EnemyPlane"""
    def __init__(self, screen, name):
        
        #设置飞机的默认位置        
        self.x = 0
        self.y = 0

        #设置飞机图片
        self.imageName = "./feiji/enemy-1.gif"

        self.direction = "right"
        super().__init__(screen, name)

    def move(self):
        if self.direction == "right":
            self.x += 2
        # else:
        elif self.direction == "left":
            self.x -= 2

        if self.x > 480-50:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    def shootBullet(self):
        num = random.randint(1,100)
        if num == 88:
            super().shootBullet()

class PublicBullet(object):
    """docstring for PublicBullet"""
    def __init__(self, x, y, screen, planeName):
        self.planeName = planeName
        self.screen = screen

        if self.planeName == "hero":
            self.x = x+40
            self.y = y
            imageName = "./feiji/bullet-3.gif"
        elif self.planeName == "enemy":
            self.x = x+25
            self.y = y+30
            imageName = "./feiji/bullet-1.gif"
                        
        self.image = pygame.image.load(imageName).convert()
        
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        
    def move(self):
        if self.planeName == "hero":
            self.y -= 2
        elif self.planeName == "enemy":
            self.y += 2

    def judgeOut(self):
        if self.y > 830 or self.y < 0:
            return True
        else:
            return False

if __name__ == '__main__':
    
    #创建一个窗口
    screen = pygame.display.set_mode((480,830),0,32)
    #创建一个和窗口大小的图片，用来充当背景
    background = pygame.image.load("./feiji/background.png").convert()

    heroPlane = HeroPlane(screen, "hero")
    enemyPlane = EnemyPlane(screen, "enemy")

    while True:
        
        screen.blit(background,(0,0))
        
        heroPlane.display()
        
        enemyPlane.display()
        enemyPlane.move()
        enemyPlane.shootBullet()

        #按键检测
        for event in pygame.event.get():
            if event.type == QUIT:
                print("exit")
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    print("left")
                    heroPlane.moveLeft()
                elif event.key == K_d or event.key == K_RIGHT:
                    print("right")
                    heroPlane.moveRight()
                elif event.key == K_UP:
                    print("up")
                    heroPlane.moveUp()
                elif event.key == K_DOWN:
                    print("down")
                    heroPlane.moveDown()

                elif event.key == K_SPACE:
                    print("space")
                    heroPlane.shootBullet()

        #代码优化，不让占用太多资源
        time.sleep(0.01)
        
        pygame.display.update()
