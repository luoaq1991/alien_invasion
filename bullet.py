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
		#self.x=float(self.rect.x)
		
		self.color=ai_settings.bullet_color
		self.speed_factor=ai_settings.bullet_speed_factor
		
	def update(self):
		#向上移动子弹(坐标)
		self.y -= self.speed_factor
		#self.x += self.speed_factor
		
		#更新方块位置
		self.rect.y=self.y
		#self.rect.x=self.x
		
	def draw_bullet(self):
		#绘制子弹
		pygame.draw.rect(self.screen,self.color,self.rect)
		
		
		
