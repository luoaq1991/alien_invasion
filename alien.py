import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	
	
	def __init__(self,ai_settings,screen):
		 
		#初始化起始位置
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings

		#加载图像,描边
		self.image = pygame.image.load("images/alien.bmp")
		self.rect = self.image.get_rect()

		#设置初始位置
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#储存坐标
		self.x = float(self.rect.x)
		
	def blitme(self):
		#绘制外星人
		self.screen.blit(self.image,self.rect)
		
	#更新位置
	def update(self):
		self.x += self.ai_settings.alien_speed_factor
		self.rect.x = self.x
		 
	
		 
		 
		 
	
