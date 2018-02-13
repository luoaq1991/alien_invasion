import sys
from time import sleep

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
	
	#更新屏幕时需要将飞船和外星人同时更新
	ship.blitme()
	aliens.draw(screen)
	
	#绘制每个子弹在屏幕上
	for bullet in bullets.sprites():
		bullet.draw_bullet()
				
	#最近绘制的屏幕可见(时时刷新屏幕)
	pygame.display.flip()
	
def update_bullets(ai_settings,screen,ship,aliens,bullets):
	
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
	
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
	
	
		
#检测碰撞,碰撞即删除
def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	if len(aliens) == 0:
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)
		
		

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
		#每行随机创建至少1个外星人
		random_num=randint(1,int(number_aliens_x))
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
	

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
	
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	for alien in aliens.copy():
		if alien.rect.top >= ai_settings.screen_height:
			aliens.remove(alien)
			#create_fleet(ai_settings,screen,ship,aliens)
			
	#碰撞结束游戏
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
	
	
	


def check_fleet_edges(ai_settings,aliens):
	for alien in aliens.sprites():
		#若触变,执行换方向
		if alien.check_edge():
			change_fleet_direction(ai_settings,aliens)
			break


def change_fleet_direction(ai_settings,aliens):
	#触变外星人乡下坠落,反向横移
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	


#飞船击中后
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	
	if stats.ships_left > 0:
		#船命-1
		stats.ships_left -= 1
		
		#清空数据
		aliens.empty()
		bullets.empty()
		
		#创建新外星人,飞船归位
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		
		#暂停
		sleep(0.5)
		
	else:
		stats.game_active = False
	
	
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#若触底,则算失败,重新开始
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

	
	
	
	

	

