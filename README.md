
# Monte Carlo Simulator

## Metadata
**Author:** Zahra Nouri  
**Project Name:** Monte Carlo Simulator

## Synopsis
The Monte Carlo Simulator allows users to create dice, play games, and analyze the results of those games. Here's how you can use the simulator:

### Installation
```bash
pip install -e .
```

### Usage

#### Create a Die
```python
from project import Die

# Create a fair die with faces 1 to 6
die = Die(np.array([1, 2, 3, 4, 5, 6]))

# Change the weight of face 2 to 5.0
die.change_weight(2, 5.0)

# Roll the die 10 times
rolls = die.roll_time(10)
```

#### Play a Game
```python
from project import Game

# Create two dice
die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))

# Play a game with the dice
game = Game([die1, die2])
game.play(100)  # Roll the dice 100 times

# Show results in wide format
results_wide = game.show_results(wide=1)

# Show results in narrow format
results_narrow = game.show_results(wide=0)
```

#### Analyze a Game
```python
from project import Analyzer

# Analyze the game
analyzer = Analyzer(game)

# Count jackpots
jackpots = analyzer.jackpot()

# Count face occurrences per roll
face_counts = analyzer.face_count()

# Count combinations
combo_counts = analyzer.combo_count()

# Count permutations
permutation_counts = analyzer.permutation_count()
```

## API Description

### Die Class
**Methods:**
- `__init__(self, faces=[1, 2, 3, 4, 5, 6])`: Initializes a die with the given faces.  
  - **Parameters:**  
    `faces` (np.ndarray): Unique symbols or numbers. Default is `[1, 2, 3, 4, 5, 6]`.  
  - **Raises:**  
    - `TypeError`: If `faces` is not a NumPy array.  
    - `ValueError`: If `faces` are not unique.  

- `change_weight(self, face, new_weight)`: Changes the weight of a specific face.  
  - **Parameters:**  
    `face` (int/str): Face to modify.  
    `new_weight` (float): New weight for the face. Must be positive.  
  - **Raises:**  
    - `IndexError`: If `face` is not valid.  
    - `TypeError`: If `new_weight` is not numeric.  

- `roll_time(self, times=1)`: Rolls the die a specified number of times.  
  - **Parameters:**  
    `times` (int): Number of rolls. Must be positive.  
  - **Returns:**  
    `list`: List of outcomes.  

- `current_state(self)`: Retrieves the current state of the die.  
  - **Returns:**  
    `pd.Series`: Pandas Series with faces as the index and their respective weights as values.  

- `get_faces(self)`: Retrieves the face values of the die.  
  - **Returns:**  
    `np.ndarray`: Array of die faces.  

---

### Game Class
**Methods:**
- `__init__(self, dice_list)`: Initializes the game with a list of dice.  
  - **Parameters:**  
    `dice_list` (list): List of `Die` objects.  
  - **Raises:**  
    - `TypeError`: If `dice_list` is not a list.  
    - `ValueError`: If dice do not have the same faces.  

- `play(self, times)`: Plays the game by rolling dice.  
  - **Parameters:**  
    `times` (int): Number of rolls.  
  - **Raises:**  
    `ValueError`: If `times` is not positive.  

- `show_results(self, wide=1)`: Displays results in wide or narrow format.  
  - **Parameters:**  
    `wide` (int): 1 for wide, 0 for narrow format.  
  - **Returns:**  
    `pd.DataFrame`: DataFrame of results.  
  - **Raises:**  
    `ValueError`: If `wide` is not 0 or 1.  

- `get_dice_faces(self)`: Retrieves dice faces used in the game.  
  - **Returns:**  
    `np.ndarray`: Array of dice faces.  

- `get_event_number(self)`: Retrieves the number of rolls.  
  - **Returns:**  
    `int`: Number of rolls.  

---

### Analyzer Class
**Methods:**
- `__init__(self, game)`: Initializes the analyzer with a game object.  
  - **Parameters:**  
    `game` (`Game`): A `Game` object.  
  - **Raises:**  
    `ValueError`: If `game` is not a `Game` object.  

- `jackpot(self)`: Counts the number of jackpots.  
  - **Returns:**  
    `int`: Number of jackpots.  

- `face_count(self)`: Counts face occurrences in each roll.  
  - **Returns:**  
    `pd.DataFrame`: DataFrame with roll numbers as rows, faces as columns.  

- `combo_count(self)`: Counts combinations of faces.  
  - **Returns:**  
    `pd.DataFrame`: DataFrame with combinations as the index and counts as a column.  

- `permutation_count(self)`: Counts permutations of faces.  
  - **Returns:**  
    `pd.DataFrame`: DataFrame with permutations as the index and counts as a column.  
