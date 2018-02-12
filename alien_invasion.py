import sys
import pygame

#导入设置
from settings import Settings
#导入飞船
from ship import Ship

import game_functions as gf

def run_game():
	
	#初始化游戏界面
	pygame.init()
	
	#生成设置对象
	ai_settings=Settings()
	screen=pygame.display.set_mode(
		(ai_settings.screen_width,ai_settings.screen_height))
		
	pygame.display.set_caption("Alien Invasion")
	
	#生成新飞船
	ship=Ship(ai_settings,screen)
	
	#游戏主循环
	while True:
		
		#调取监视事件
		gf.check_events(ship)
		#更新飞船位置
		ship.update()
		
		#刷新屏幕
		gf.update_screen(ai_settings,screen,ship)

run_game()
