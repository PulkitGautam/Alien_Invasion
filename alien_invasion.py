import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

# Overall Class to manage Alien_Invasion game assets and behaviour


class AlienInvasion:
    def __init__(self):           # To initialize the game setup and create resources

        # Initializes the background settings that Pygame needs to work properly
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()         # Creating a Group of Bullets
        self.aliens = pygame.sprite.Group()          # Creating a Fleet of Aliens

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def run_game(self):           # Starting the main loop of the game
        while True:
            self._check_events()                 # Checking for Events

            if self.stats.game_active:
                self.ship.update()                   # Updating Ship Position
                self._updating_bullets()             # Updating Bullet
                self._update_aliens()

            self._update_screen()                # Updating Screen

    def _check_events(self):
        for event in pygame.event.get():       # Check for Keyboard and Mouse Events
            if event.type == pygame.QUIT:      # Close the program if user wants to quit
                sys.exit()
            elif event.type == pygame.KEYDOWN:                 # Each Key press is taken as KEYDOWN event
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:                   # On Release of Key
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True
    
    def _fire_bullet(self):
        # Create a new bullet and add it to group
        if len(self.bullets) < self.settings.bullet_allowed:               # Limiting a Number of bullet at a time
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _updating_bullets(self):
        self.bullets.update()                # Updating Bullets
        self._check_bullet_alien_collisions()
    
        # Deleting Bullet once they reach top
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    # Check for Collision and deleting bullet and alien
    def _check_bullet_alien_collisions(self):
        collision = pygame.sprite.groupcollide(self.aliens,self.bullets, True, True)
        # object 1, object 2, delete_first, delete_second

        if collision:
            print("Alien Down!!!")

        if not self.aliens:
            self.bullets.empty()                 # Destroy existing bullets
            self._create_fleet()                 # Create new fleet
            self.settings.increase_speed()
    
    def _create_fleet(self):
        alien = Alien(self)                                # New Alien
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen_width - (2 * alien_width)          # Calculating space betwwen aliens
        number_aliens_x = available_space_x // (2 * alien_width)                    # and number of aliens in a row

        # Calculation No. of rows
        ship_height = self.ship.rect.height
        available_space_y = (self.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y//(2*alien_height)

        # Creating Fleet of Aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2*alien_height*row_number

        self.aliens.add(alien)                             # Adding alien to group

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Detect Alien Ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
            sys.exit()

        self._check_aliens_bottom()

    def ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(1)
        else:
            self.stats.game_active = False

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y +=self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)      # Fill the set Color
        if self.stats.game_active == False:
            self.play_button.draw_button()
            pygame.mouse.set_visible(True)
        if self.stats.game_active == True:
            self.ship.blitme()                            # Draws the image on Screen
            pygame.mouse.set_visible(False)
            for bullet in self.bullets.sprites():         # Loop for drawing each bullet
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

        pygame.display.flip()         # Constantly Updates Screen for changes in game elements

# Make a game instance, and run the game.
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()