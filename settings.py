class Settings():
	def __init__(self):
		
		#屏幕设置
		self.screen_width=800
		self.screen_height=600
		self.bg_color=(230,230,230)
		
		#飞船命
		self.ship_limit = 3
		
		#子弹设置
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		#子弹数量
		self.bullets_allowed = 3
		
		#外星人设置
		self.fleet_drop_speed = 15
		
		
		#游戏速度加快系数
		self.speedup_scale = 1.1
		
		#提高击中点数
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
		
		
	def initialize_dynamic_settings(self):
		
		#设置游戏内物体移动速度
		self.ship_speed_factor=1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		
		self.fleet_direction = 1
		
		#记分
		self.alien_points = 50
		
	
	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
		
