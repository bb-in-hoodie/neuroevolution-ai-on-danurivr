class Simulation:
	def __init__(self, total_frames, fps=60, stage_rad=30, bomb_area=40):
		self.total_frames = total_frames
		self.fps = fps
		self.stage_rad = stage_rad
		self.bomb_area = bomb_area

		# private
		self.__bomb_list = []
		self.__frame_count = 1

	def get_bomb_list(self):
		return self.__bomb_list

	def add_bomb(self, bomb):
		self.__bomb_list.append(bomb)

	def remove_bombs(self, bombs):
		if (len(bombs) > 0):
			for bomb in bombs:
				self.__bomb_list.remove(bomb)

	def get_frame_count(self):
		return self.__frame_count

	def inc_frame_count(self):
		self.__frame_count += 1