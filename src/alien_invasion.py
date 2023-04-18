import sys
import pygame
from time import sleep

from game_stats import GameStats
from button import Button
from settings import Settings
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion():

    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()

        # AI game Instances
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.play_button = Button(self, "Play")

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        # Watch for keyboard and mouse event
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _start_game(self):
        """Activate game and Reset Stats"""
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of remianing alien and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create new fleet and recenter ship
        self._create_fleet()
        self.ship.center_ship()

        # Mouse goes invisible when game starts
        pygame.mouse.set_visible(False)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_setting()
            self._start_game()
            self.sb.prep_score()

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif (event.key == pygame.K_ESCAPE) or (event.key == pygame.K_q):
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        elif (event.key == pygame.K_p) and (not self.stats.game_active):
            # Don't start a new game during an active game, that's probably
            #   an accidental keypress.
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullets(self):
        """Create a new bulelt and add it to the new bullet groups"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows  of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (3 * alien_height)

        # Create a full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size
         alien.x = alien_width + 2 * alien_width * alien_number
         alien.rect.x = alien.x
         alien.rect.y = alien_height + 2 * alien.rect.height * row_number
         self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """Eliminates Aliens and adds points to score and high score"""
        #Check for any bullets that have hit aliens.
        # if so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                            True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.settings.increase_speed()

    def _check_aliens_bottom(self):
        """ Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to ships being hit by aliens"""
        # Decrease Ships left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            #Pause
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # create a new fleet and recenter the ship()
        self._create_fleet()
        self.ship.center_ship()

        #Pause
        sleep(1)

    def _update_aliens(self):
        """Update the postion of all the aliens  in the fleet"""
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship Hit! Respawning ship!")
            print(f"Ships available: {self.stats.ships_left}")
            self._ship_hit()


        self._check_fleet_edges()
        self._check_aliens_bottom()

    def _update_bullets(self):
            # Update Bullet Position
            self.bullets.update()
            # get rid of bullets that have dissapeared
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

            self._check_bullet_alien_collisions()

    def _update_screen(self):
        """Update Images on the Screen and flip to the new screen"""
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        # Draw the Play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most visibly drawn screen visible
        pygame.display.flip()
        self.clock.tick()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()