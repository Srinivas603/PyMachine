import sys

import pygame

from settings import Settings

from ship import Ship

import game_functions as gf

from pygame.sprite import Group

from alien import Alien

from game_stats import GameStats

from button import Button

def run_game():
	#initialize the game and create screen object
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	#adding caption
	pygame.display.set_caption("Alien Invasion")
	
	#make the play button
	play_button = Button(ai_settings,screen,"play")
	
	#create ship
	ship = Ship(ai_settings,screen)
	
	#make an alien
	alien = Alien(ai_settings,screen)
	
	#Creating group to store bullets in 
	bullets = Group()
	
	#Creating group to store aliens
	aliens = Group()
	
	#Creating a fleet of aliens
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#creat an instance to store game statistics
	stats = GameStats(ai_settings)
	
	#writing a loop for the events and controllig it
	while True:
		
		#watch for keyboard and mouse events
		gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
			gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
		
			#updates the background colour and screen
			gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)
		
		
run_game()
