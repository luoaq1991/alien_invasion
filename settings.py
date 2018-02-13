class Settings():
	def __init__(self):
		
		#屏幕设置
		self.screen_width=1024
		self.screen_height=768
		self.bg_color=(230,230,230)
		
		#设置飞船速度
		self.ship_speed_factor=1.5
		
		#飞船命
		self.ship_limit = 3
		
		#子弹设置
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		#子弹数量
		self.bullets_allowed = 3
		
		#外星人设置
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 15
		self.fleet_direction = 1
		
		
