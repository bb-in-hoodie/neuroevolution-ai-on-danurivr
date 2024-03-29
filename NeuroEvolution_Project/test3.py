from genetic.genetic import GeneticAlgorithm

ga = GeneticAlgorithm(population=15, crossover_prob=0.4, generation=60, mutation_prob=0.001, total_frames=3600, network_size=[6, 6, 6, 2], use_velocity=True)
best_enemies = ga.run()