import sys
import pygame

from bullet import Bullet
from alien import Alien
from random import randint

#响应按键
def check_keydown_events(event,ai_settings,screen,ship,bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right=True
				
	elif event.key == pygame.K_LEFT:
		ship.moving_left=True
		
	elif event.key == pygame.K_UP:
		ship.moving_up=True
		
	elif event.key == pygame.K_DOWN:
		ship.moving_down=True
		
	elif event.key == pygame.K_SPACE:
		#调用方法,生成子弹,并将子弹放入编组
		fire_bullet(ai_settings,screen,ship,bullets)
		
	#关闭游戏
	elif event.key == pygame.K_q:
		sys.exit()
		
	#print(str(event.key))
	

#响应松开
def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right=False
				
	elif event.key == pygame.K_LEFT:
		ship.moving_left=False
	
	elif event.key == pygame.K_UP:
		ship.moving_up=False
	
	elif event.key == pygame.K_DOWN:
		ship.moving_down=False


#按下空格,生成子弹,判断数量
def fire_bullet(ai_settings,screen,ship,bullets):
	#判断
	if  len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		#在编组内加入子弹
		bullets.add(new_bullet)
		


def check_events(ai_settings,screen,ship,bullets):
	#监视键盘及鼠标事件
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
			
		#键盘左右移动
		#分为按下和弹起
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
			
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		

def update_screen(ai_settings,screen,ship,aliens,bullets):
	#重新绘制屏幕时颜色需要跟进
	screen.fill(ai_settings.bg_color)
	
	ship.blitme()
	aliens.draw(screen)
	
	#绘制每个子弹在屏幕上
	for bullet in bullets.sprites():
		bullet.draw_bullet()
				
	#最近绘制的屏幕可见(时时刷新屏幕)
	pygame.display.flip()
	
def update_bullets(bullets):
	
	#更新子弹位置
	bullets.update()
		
	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	#向x发射子弹
	# ~ for bullet in bullets.copy():
		# ~ if bullet.rect.centerx >= 1200:
			# ~ bullets.remove(bullet)
	#print(len(bullets))
	

def create_fleet(ai_settings,screen,ship,aliens):
	#初始化外星人
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	
	#计算每行外星人数量
	number_aliens_x = get_number_aliens_x(ai_settings,alien_width)
	#计算行数
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	
	#逐行,逐列创建外星人
	for row_number in range(number_rows):
		random_num=randint(0,int(number_aliens_x))
		for alien_number in range(random_num):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
		

#计算放外星人的空间及数量
def get_number_aliens_x(ai_settings,alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width 
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	

#创建外星人
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	

#外星人行数
def get_number_rows(ai_settings,ship_height,alien_height):
	#计算放置空间,为飞船射击留白
	available_space_y = (ai_settings.screen_height - 
							(3 * alien_height) - ship_height)
							
	number_rows =  int(available_space_y / (2 * alien_height))
	return number_rows
	

def update_aliens(aliens):
	aliens.update()


