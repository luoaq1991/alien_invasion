import sys
import pygame
#导入编组
from pygame.sprite import Group

#导入设置
from settings import Settings
#导入飞船
from ship import Ship
#导入外星人
from alien import Alien
#导入统计
from game_stats import GameStats
#导入计分板
from scoreboard import Scoreboard
#导入按钮
from button import Button

import game_functions as gf

def run_game():
	
	#初始化游戏界面
	pygame.init()
	
	#生成设置对象
	ai_settings=Settings()
	screen=pygame.display.set_mode(
		(ai_settings.screen_width,ai_settings.screen_height))
		
	pygame.display.set_caption("Alien Invasion")
	
	#创建play按钮
	play_button = Button(ai_settings,screen,"Play")
	
	#生成统计类
	stats = GameStats(ai_settings)
	
	#生成计分板
	sb = Scoreboard(ai_settings,screen,stats)
	
	#生成新飞船
	ship=Ship(ai_settings,screen)
	
	#子弹编组
	bullets = Group()
	aliens = Group()
	
	#生成外星人组
	alien = Alien(ai_settings,screen)
	gf.create_fleet(ai_settings,screen,ship,aliens)
	
	#游戏主循环
	while True:
		
		#调取监视事件
		gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
		
		if stats.game_active:
			#更新飞船位置
			ship.update()
			
			#更新子弹
			gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
			
			#更新外星人
			gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
		
		#刷新屏幕
		gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
		
		
		
run_game()
