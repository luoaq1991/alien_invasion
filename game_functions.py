import sys
import json
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien
from random import randint

#响应按键
def check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets):
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
		
		#保存并关闭游戏
		save_close(stats)
		
		
	#practice_14-1,按p开始游戏
	elif event.key == pygame.K_p:
		start_game(event,ai_settings,screen,stats,sb,ship,aliens,bullets)
		
		
	#print(str(event.key))
	
	
def save_close(stats):
	save_high_score(stats)
	sys.exit()
	


def save_high_score(stats):
	filename = str(stats.filename)
	with open(filename,'w') as f_obj:
		json.dump(stats.high_score,f_obj)
	

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
		


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	#监视键盘及鼠标事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_close()
			
		#键盘左右移动
		#分为按下和弹起
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets)
			
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
			
		#鼠标点击play事件
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
						bullets,mouse_x,mouse_y)
						
			
			

#玩家单机play后开始游戏
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,
						bullets,mouse_x,mouse_y):
	
	#按下开始游戏,重置游戏信息
	#play按钮切换到非激活状态
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#若重新开始游戏，则重置速度
		ai_settings.initialize_dynamic_settings()
		#隐藏鼠标访问
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		
		aliens.empty()
		bullets.empty()
		
		#重置记分牌
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		

def start_game(event,ai_settings,screen,stats,sb,ship,aliens,bullets):
	#practice_14-1 按p开始游戏
	if event.key == pygame.K_p and not stats.game_active:
		#重置游戏速度
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		
		aliens.empty()
		bullets.empty()
		
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		
		

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	#重新绘制屏幕时颜色需要跟进
	screen.fill(ai_settings.bg_color)
	
	#更新屏幕时需要将飞船和外星人同时更新
	ship.blitme()
	aliens.draw(screen)
	
	#绘制每个子弹在屏幕上
	for bullet in bullets.sprites():
		bullet.draw_bullet()
		
	sb.show_score()
	
	if not stats.game_active:
		play_button.draw_button()
				
	#最近绘制的屏幕可见(时时刷新屏幕)
	pygame.display.flip()
	
def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
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
	
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
	
		
#检测碰撞,碰撞即删除
def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	#若发生碰撞,则说明击中,则显示加分
	if collisions:
		#子弹可能同时碰撞多个外星人,分数应乘以击中数量
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats,sb)
	
	start_new_level(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
		

def start_new_level(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#若外星人被全部消灭，则清空子弹，加快游戏速度，并生成新的外星人。
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		
		#提升等级
		stats.level += 1
		sb.prep_level()
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
	

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	check_fleet_edges(ai_settings,aliens)
	aliens.update()
	
	for alien in aliens.copy():
		if alien.rect.top >= ai_settings.screen_height:
			aliens.remove(alien)
			#create_fleet(ai_settings,screen,ship,aliens)
			
	#碰撞结束游戏
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
	
	
	


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
def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	
	if stats.ships_left > 0:
		#船命-1
		stats.ships_left -= 1
		
		#更新飞船数量
		sb.prep_ships()
		
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
		pygame.mouse.set_visible(True)
	
	
def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#若触底,则算失败,重新开始
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			
			
#检查是否最高分
def check_high_score(stats,sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

	
	
	
	

	

