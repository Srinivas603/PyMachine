import sys

import pygame

from bullet import Bullet

from alien import Alien

from time import sleep

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
	""" Responds to keypress and mouse"""
	"""start a new game when player presses play game"""
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)
			
def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""start a new game when a player clicks on play button"""
	
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#reset the game settings
		ai_settings.initialize_dynamic_settings()
		#hide the cursor
		pygame.mouse.set_visible(False)
		
		#reset the game statistica
		stats.reset_stats()
		stats.game_active = True
		
		#empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
		
		#create the new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
			
def check_keydown_events(event,ai_settings,screen,ship,bullets):
	#responds when we press right
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_RIGHT:
			#move the ship to right
			ship.moving_right = True
				
		if event.key == pygame.K_LEFT:
				#move ship left
				ship.moving_left = True
				
		elif event.key == pygame.K_SPACE:
			fire_bullet(ai_settings,screen,ship,bullets)
			
		elif event.key == pygame.K_q:
			sys.exit()
			
def fire_bullet(ai_settings,screen,ship,bullets):
	"""fire bullet when the limit is not reached"""
	#creat a new bullet and add it to the group
	if len(bullets) < ai_settings.bullets_allowed: 
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
		
		
def check_keyup_events(event,ship):
	#responds when we press left
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_RIGHT:
			ship.moving_right = False
				
		if event.key == pygame.K_LEFT:
			ship.moving_left = False
				
			
				

	

	
def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets):
	#check for any bullets that have hit aliens
	#if so get rid of the aliens and the bullets
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	
	if(len(aliens)) == 0:
		#destroy existing bullets,speed up the game and create new fleet
		bullets.empty()
		ai_settings.increase_speed()
		create_fleet(ai_settings,screen,ship,aliens)
		
def update_bullets(ai_settings,screen,ship,aliens,bullets):
	"""updates bullet position and get rid of old bullets"""
	#update bullete position
	bullets.update()
	
	#get rid of bullets that have disappeared
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
			
	check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets)
			
def get_number_aliens_x(ai_settings,alien_width):
	"""determine the number of aliens that fit in to a row"""
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x/(2*alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings,ship_height,alien_height):
	"""determine the number of rows of aliens that fit into a screen"""
	available_space_y = (ai_settings.screen_height-( 3 * alien_height)-ship_height)
	number_rows = int(available_space_y/(2 * alien_height))
	return number_rows
	
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""create an alien and place it in a row"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	
	aliens.add(alien)
	
def create_fleet(ai_settings, screen, ship, aliens):
	"""Create a full fleet of aliens"""
	#create alien and find the number of aliens in arow
	alien = Alien(ai_settings,screen)
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	#create first row of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)
			

	

			
def change_fleet_direction(ai_settings,aliens):
	"""Drop the entire fleet and changes the direction"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
		
	ai_settings.fleet_direction *= -1
	
def check_fleet_edges(ai_settings,aliens):
	"""respond appropriatly if any alien has reached edges"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
	
	
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	"""respond if the ship being hit by alien"""
	if stats.ships_left > 0:
		
		#ships left
		stats.ships_left -= 1
	
		#empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()
	
		#create the neww fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
	
		#pause
		sleep(0.5)
		
	else:
		pygame.mouse.set_visible(True)
		stats.game_active = False
	
def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	"""check if any alien has reached bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			"""treate this same as ship hit"""
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
	
def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
	"""check if the fleet is at edge,then updates the position of all aliens"""
	check_fleet_edges(ai_settings,aliens)
	"""update position of the all aliens in the fleet"""
	aliens.update()
	
	#look for alien and ship collision
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
		
	#look for the aliens bottom
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
	
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
	screen.fill(ai_settings.bg_color)
	#redraw all the bullets behind the ship and alliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	
	#draw the play button if the game is active
	if not stats.game_active:
		play_button.draw_button()
	
	#make most recently drawn screen available
	pygame.display.flip()
	
		

	
	
	
	
		
			

		
