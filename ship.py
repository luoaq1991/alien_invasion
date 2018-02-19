import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	#初始化位置
	def __init__(self,ai_settings,screen):
		super().__init__()
		self.screen=screen
		
		#加载图像
		self.image=pygame.image.load('images/ship.bmp')
		
		#获取外接矩形,获得模型(图片及窗口)
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()
		self.ai_settings=ai_settings
		
		#飞船初始位置设置(x轴居中,y轴位于窗口底部)
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom
		#self.rect.centery=self.screen_rect.centery
		
		#储存飞机的位置,用float
		self.center_x=float(self.rect.centerx)
		self.center_y=float(self.rect.centery)
		
		#移动标志
		self.moving_right=False
		self.moving_left=False
		self.moving_up=False
		self.moving_down=False
		
	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center_x += self.ai_settings.ship_speed_factor
			
		if self.moving_left and self.rect.left > 0:
			self.center_x -= self.ai_settings.ship_speed_factor
			
		
		#前后移动,注意窗口的左上角坐标为(0,0)
		# ~ if self.moving_up and self.rect.top > 0:
			# ~ self.center_y -= self.ai_settings.ship_speed_factor
			
		# ~ if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			# ~ self.center_y += self.ai_settings.ship_speed_factor
			
		#根据center设定rect
		self.rect.centerx=self.center_x
		self.rect.centery=self.center_y
		
	def blitme(self):
		#指定位置画飞船
		self.screen.blit(self.image,self.rect)
		
	def center_ship(self):
		self.center = self.screen_rect.centerx
		
	
		
