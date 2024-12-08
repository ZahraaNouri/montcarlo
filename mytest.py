from montecarlo import Die, Game, Analyzer

# Create a die
die = Die([1, 2, 3])
print("Die created with faces:", die.get_faces())


# Change weight of a face
die.change_weight(2, 5)
print("Updated die state:")
print(die.current_state())

# Roll the die
rolls = die.roll_time(10)
print("Die rolls:", rolls)
