import math, numpy as np
from hellopy.gameobject.sprite import *
from hellopy.window import window
from random import randint
from hellopy.mouse import mouse
from hellopy.gameobject.circle import Circle
from hellopy.sound import Sound

__all__ = ['distance', 'Loong', 'Position', 'Ball', 'get_angle', 'move_to','player', 'bgm', 'sfx']



# 玩家类
class Player():
    def __init__(self):
        self.controller = mouse
        self.score = 0
        self.mode = 0
        self.finger_nodes = []

# 龙珠类
class Ball(Circle):
    def __init__(self,x=randint(0,window.w),y=randint(0,window.h),r=20,color="gold"):
        self._x = x
        self._y = y
        self._r = r
        self._color = color
        super().__init__(self.x,self.y,self.r,self.color)
    @ property
    def x(self):
        return self._x
    @ x.setter
    def x(self,x):
        self._x = x
        return self._x 
    
    @ property
    def y(self):
        return self._y
    @ y.setter
    def y(self,y):
        self._y = y
        return self._y
    def draw(self):
        super().draw()
    
    @ property
    def r(self):
        return self._r
    @ r.setter
    def r(self,r):
        self._r = r
        return self._r
    
    @ property
    def color(self):
        return self._color
    @ color.setter
    def color(self,color):
        self._color = color
        return self._color
    
    def draw(self):
        super().draw()
    
    def reset(self):
        self.x = randint(0, window.w)
        self.y = randint(0, window.h)

# 位置类
class Position():
    def __init__(self,x,y):
        self._x = x
        self._y = y

    @ property
    def x(self):
        return self._x
    @ x.setter
    def x(self,x):
        self._x = x
        return self._x
    
    @ property
    def y(self):
        return self._y
    @ y.setter
    def y(self,y):
        self._y = y
        return self._y
    
# 龙
class Loong():
    def __init__(self,length=2):
        self.head = Sprite(400,300,90,80,"https://pic.imgdb.cn/item/65d01dad9f345e8d03984642.png")
        self.speed = 20
        self.score = 0
        self._length = length
        self.head.x_speed = 1
        self.head.y_speed = 0
        self.bodys = [self.head]
        for i in range(self._length):
            new_body = Sprite(self.bodys[-1].x-50,self.bodys[-1].y,60,45,"https://pic.imgdb.cn/item/65d01dac9f345e8d03984400.png")
            self.bodys.append(new_body)
        self.tail = Sprite(self.bodys[-1].x-65,self.bodys[-1].y,110,45,"https://pic.imgdb.cn/item/65d19e369f345e8d03507793.png")
        self.bodys.append(self.tail)
        self.foot1 = Sprite(100,100,60,120,"https://pic.imgdb.cn/item/65d5b5569f345e8d035dd171.png")
        self.foot2 = Sprite(100,100,60,120,"https://pic.imgdb.cn/item/65d5b5569f345e8d035dd171.png")
     
    # 绘制龙    
    def draw(self):
        self.head_to(self.head)
        for item in self.bodys[-1::-1]:
            item.draw()
        self.foot1.draw()
        self.foot2.draw()
    
    # 移动龙
    def head_to(self, target):
        if distance(self.head,target) > 20:
            move_to(self.head,target,self.speed)
        for i in range(1,len(self.bodys)-1):
            if distance(self.bodys[i],self.bodys[i-1]) > 50:
                move_to(self.bodys[i],self.bodys[i-1],self.speed)
        if distance(self.bodys[-1],self.bodys[-2])>65:
            move_to(self.bodys[-1],self.bodys[-2],self.speed)
        a = len(self.bodys) // 3 - 1 
        if a < 1:
            a = 1
        self.foot1.x = self.bodys[a].x
        self.foot1.y = self.bodys[a].y
        self.foot1.angle = self.bodys[a].angle
        self.foot1.rotate_to(self.foot1.angle)

        b = len(self.bodys) // 3 * (-1) -1
        self.foot2.x = self.bodys[b].x
        self.foot2.y = self.bodys[b].y
        self.foot2.angle = self.bodys[b].angle
        self.foot2.rotate_to(self.foot2.angle)

    def collide(self, other):
        return self.head.collide(other)
    
    # 增加龙的长度
    @ property
    def length(self):
        return self._length
    @ length.setter
    def length(self, n):
        bl = n
        if bl < 2:
            bl = 2
        if self._length > bl:
            x = self._length - n
            self.bodys[-1].x = self.bodys[-1-x].x
            self.bodys[-1].y = self.bodys[-1-x].y
            self.bodys[-1].angle = self.bodys[-x].angle
            self.bodys = self.bodys[:(-x)] + [self.bodys[-1]]
            self._length = bl
            return self._length
        while self._length < bl:
            self.bodys.insert(-1,Sprite(self.bodys[-1].x,self.bodys[-1].y,60,45,"https://pic.imgdb.cn/item/65d01dac9f345e8d03984400.png"))
            self._length += 1
        return self._length

# 计算距离
def distance(a,b):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

# 坐标换算角度
def get_angle(vx,vy):
    return np.degrees(np.arctan2(vy, vx))

# 向某个物体按特定速度移动
def move_to(start,target,speed):
    if start.x == target.x and start.y == target.y:
        return
    vx = (target.x - start.x) / distance(start,target) * speed
    vy = (target.y - start.y) / distance(start,target) * speed
    start.x += vx
    start.y += vy
    angle = get_angle(vx, vy)
    start.rotate_to(angle)  

player = Player()
bgm = Sound("https://lldocs-1257261737.cos.ap-shanghai.myqcloud.com/sound/festival_bg.mp3")
bgm.set_volume(0.1)
sfx = Sound("https://r.leaplearner.com/a/1/gainTools.mp3")
sfx.set_volume(1.0)