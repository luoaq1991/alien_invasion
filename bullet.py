import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	
	def __init__(self,ai_settings,screen,ship):
		
		#飞船位置创建子弹
		super().__init__()
		self.screen=screen
		
		#创建子弹的矩形,继而设定位置
		self.rect=pygame.Rect(0,0,ai_settings.bullet_width,
			ai_settings.bullet_height)
		self.rect.centerx=ship.rect.centerx
		self.rect.top=ship.rect.top
		
		#储存子弹位置
		self.y=float(self.rect.y)
		
		self.color=ai_settings.bullet_color
		self.speed_factor=ai_settings.bullet_speed_factor
		
	def 
		
