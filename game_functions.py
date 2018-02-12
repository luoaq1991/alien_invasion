import sys
import pygame

#响应按键
def check_keydown_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=True
				
	elif event.key==pygame.K_LEFT:
		ship.moving_left=True
		
	elif event.key==pygame.K_UP:
		ship.moving_up=True
		
	elif event.key==pygame.K_DOWN:
		ship.moving_down=True
		
	#print(str(event.key))
	

#响应松开
def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
				
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False
	
	elif event.key==pygame.K_UP:
		ship.moving_up=False
	
	elif event.key==pygame.K_DOWN:
		ship.moving_down=False
	

def check_events(ship):
	#监视键盘及鼠标事件
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
			
		#键盘左右移动
		#分为按下和弹起
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ship)
			
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)
		

		

def update_screen(ai_settings,screen,ship):
	#重新绘制屏幕时颜色需要跟进
	screen.fill(ai_settings.bg_color)
	ship.blitme()
				
	#最近绘制的屏幕可见(时时刷新屏幕)
	pygame.display.flip()
	
