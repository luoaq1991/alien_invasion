

#游戏信息统计类
class GameStats():
	
	def __init__(self,ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		
		#游戏开始为非激活类
		self.game_active = False
		
		#游戏最高得分,不会改变
		self.high_score = 0
		
	def reset_stats(self):
		self.ships_left = self.ai_settings.ship_limit
		#显示分数
		self.score = 0
		#显示等级
		self.level = 1

