from .simulation import Simulation
from .player import Player
from .enemy import Enemy

class Simulator:
	def __init__(self, total_frames, player_pos, enemy_num, network_size, fps=60, play_area=38, stage_rad=30, bomb_area=40, print_log=False):
		self.sim_list = [Simulation(i) for i in range(enemy_num)]
		for sim in self.sim_list:
			sim.assign_player(Player(sim, player_pos, fps, play_area))
			sim.assign_enemy(Enemy(network_size, stage_rad, play_area, bomb_area))
		self.total_frames = total_frames
		self.enemy_num = enemy_num
		self.fps = fps
		self.play_area = play_area
		self.stage_rad = stage_rad
		self.bomb_area = bomb_area
		self.print_log = print_log

		# Private
		self.__cur_frame = 0

	def run(self):		
		dead_enemies = 0
		while (self.__cur_frame < self.total_frames and dead_enemies < self.enemy_num):
			for i in range(self.enemy_num):
				# Fetch current enemy, player, and simulation
				sim = self.sim_list[i]
				player = sim.player
				enemy = sim.enemy

				# If cur enemy is already dead, no simulation is proceeded
				if enemy.is_dead:
					continue

				# Test purpose
				log = "[Enemy: %d, Frames: %d]"%(i, sim.get_frame_count())

				# Move the player, it will shoot a bomb randomly
				log_temp = player.move(enemy.pos)
				if log_temp != "":
					log += log_temp

				# Move the bombs and remove the ones whose position is too far
				removed_bombs = []
				for bomb in sim.get_bomb_list():
					bomb.move()

					# Destroy a bomb if it is out of the bomb area
					if (bomb.pos[0]**2 + bomb.pos[1]**2) > self.bomb_area**2:
						removed_bombs.append(bomb)

					# If a bomb hits the enemy, enemy dies
					dist_x = bomb.pos[0] - enemy.pos[0]
					dist_y = bomb.pos[1] - enemy.pos[1]
					dist = (dist_x**2 + dist_y**2)
					if dist < (bomb.rad+enemy.rad)**2:
						enemy.is_dead = True
						dead_enemies += 1

				sim.remove_bombs(removed_bombs)

				# Move the enemies and kill the ones who is hit by a bomb
				log += "\n"
				log += enemy.move(sim.get_bomb_list(), player.pos)
				log += "\n"

				# Increase the current frame count of the simulation by one
				sim.inc_frame_count()

				# Test purpose
				log += "Player: (%.3f, %.3f), Enemy: (%.3f, %.3f)"%(player.pos[0], player.pos[1], enemy.pos[0], enemy.pos[1])
				if len(sim.get_bomb_list()) > 0:
					log += "\n----- Bomb Moves -----"
					for bomb in sim.get_bomb_list():
						log += "\nBomb: (%.3f, %.3f)"%(bomb.pos[0], bomb.pos[1])
				if enemy.is_dead:
					log += " -> <DEAD!>"
				log += "\n===================================="

				# Print the log
				if self.print_log:
					print(log)

			# Increase the frame of the simulator	
			self.__cur_frame += 1

		# Print the final results
		print("\nFinal Results: ")
		for i in range(self.enemy_num):
			print("%d has survived %.2fseconds"%(i, (self.sim_list[i].get_frame_count()/self.fps)))