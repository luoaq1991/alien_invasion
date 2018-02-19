import json

#游戏信息统计类
class GameStats():
	
	def __init__(self,ai_settings):
		self.ai_settings = ai_settings
		self.reset_stats()
		
		#游戏开始为非激活类
		self.game_active = False
		
		#游戏最高得分,不会改变
		self.filename = "score.json"
		self.high_score = self.get_his_high_score()
		
		
	def reset_stats(self):
		self.ships_left = self.ai_settings.ship_limit
		#显示分数
		self.score = 0
		#显示等级
		self.level = 1
		
	def get_his_high_score(self):
		try:
			with open(self.filename) as f_obj:
				his_high_score = json.load(f_obj)
		except FileNotFoundError:
			return 0
		else:
			return his_high_score

