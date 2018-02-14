#游戏信息统计类
class GameStats():
	
	def __init__(self,ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		
		#游戏开始为非激活类
		self.game_active = False
		
	def reset_stats(self):
		self.ships_left = self.ai_settings.ship_limit
		
	
