class Settings():
	"""A class to store all the settings in Alien invasion."""
	
	def __init__(self):
		"""Initialize the game settings."""
		self.screen_width = 1500
		self.screen_height = 700
		self.bg_color = (255,255,255)
		
		#ship settings
		#self.ship_speed_factor = 1.5
		self.ship_limit = 3
		
		#bullet settings
		#self.bullet_speed_factor = 10
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 10
		
		#alien settings
		#self.alien_speed_factor = 1
		self.fleet_drop_speed = 2
		
		#fleet direction 1 represents right; -1 represents left
		#self.fleet_direction = 1
		
		#how quickly the game speeds up
		self.speedup_scale = 1.1
		
		self.initialize_dynamic_settings()
		self.increase_speed()
		
	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1.5
		self.alien_speed_factor = 1
		self.bullet_speed_factor = 10
		#fleet direction 1 represents right; -1 represents left
		self.fleet_direction = 1
		
	def increase_speed(self):
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		
		
		
