import unittest
import pandas as pd
import numpy as np
from montecarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    
    def setUp(self):
        """Set up a Die instance for testing."""
        self.die = Die(np.array([1, 2, 3]))
        
    def test_init_faces(self):
        """Test that the Die object initializes correctly with faces."""
        self.assertEqual(list(self.die.faces), [1, 2, 3])
    
    def test_init_faces_invalid_type(self):
        """Test that initializing with a non-NumPy array raises TypeError."""
        with self.assertRaises(TypeError):
            Die([1, 2, 3])
    
    def test_init_faces_non_unique(self):
        """Test that initializing with non-unique faces raises ValueError."""
        with self.assertRaises(ValueError):
            Die(np.array([1, 1, 2]))

    def test_change_weight(self):
        """Test that changing the weight updates the die."""
        self.die.change_weight(2, 5.0)
        die_state = self.die.current_state()  
        self.assertEqual(die_state.loc[2], 5.0)

    def test_change_weight_invalid_type(self):
        """Test that change_weight raises correct error for invalid weight datatype."""
        with self.assertRaises(TypeError):
            self.die.change_weight(2, 'hi')

    def test_change_weight_invalid_face(self):
        """Test that change_weight raises correct error for invalid face."""
        with self.assertRaises(IndexError):
            self.die.change_weight(4, 3)

    def test_roll_time(self):
        """Test that rolling the die returns a list."""
        rolls = self.die.roll_time(10)
        self.assertEqual(len(rolls), 10)
        self.assertIsInstance(rolls, list)

    def test_current_state(self):
        """Test that current_state returns a pandas Series."""
        die_state = self.die.current_state()
        self.assertIsInstance(die_state, pd.Series)

    def test_get_faces(self):
        """Test that get_faces returns a numpy array."""
        die_returned_faces = self.die.get_faces()
        self.assertIsInstance(die_returned_faces, np.ndarray)

class TestGame(unittest.TestCase):
    def setUp(self):
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        self.game = Game([die1, die2])

    def test_init_game(self):
        """Test that the Game object initializes correctly."""
        self.assertIsInstance(self.game, Game)

    def test_init_invalid_dice_list(self):
        """Test that initializing with invalid dice list raises TypeError."""
        with self.assertRaises(TypeError):
            Game("not a list")  

    def test_init_mismatched_faces(self):
        """Test that initializing with dice with mismatched faces raises ValueError."""
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 4]))  
        with self.assertRaises(ValueError):
            Game([die1, die2]) 
    
    def test_play(self):
        """Test that the play method produces the correct DataFrame."""
        self.game.play(5)
        results = self.game.show_results(wide=1)
        self.assertEqual(results.shape, (5, len(self.game._Game__dice_list)))  
    
    def test_show_results_wide(self):
        """Test that show_results returns the DataFrame in wide format."""
        self.game.play(3)
        results = self.game.show_results(wide=1)
        self.assertIsInstance(results, pd.DataFrame)
        self.assertEqual(results.shape[1], 2)  

    def test_show_results_narrow(self):
        """Test that show_results returns the DataFrame in narrow format."""
        self.game.play(3)
        results = self.game.show_results(wide=0)
        self.assertIsInstance(results, pd.DataFrame)
        index_names = results.index.names
        expected_index_names = ['Roll Number', 'Die Number']
        self.assertEqual(index_names, expected_index_names)

        self.assertTrue(not results.empty, "The results dataframe should not be empty")

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)

    def test_init_analyzer(self):
        """Test that the Analyzer object initializes correctly."""
        self.assertIsInstance(self.analyzer, Analyzer)
        
    def test_analyzer_init_invalid_input(self):
        """Test that Analyzer raises ValueError for invalid Game object."""
        with self.assertRaises(ValueError):
            Analyzer("not a game object") 

    def test_jackpot(self):
        """Test that jackpot returns an integer."""
        jackpots = self.analyzer.jackpot()
        self.assertIsInstance(jackpots, int)

    def test_jackpot_value(self):
        """Test that jackpot returns an integer and calculates the correct value."""
        # Create a scenario where there are known jackpots
        die3 = Die(np.array([1, 2]))
        die4 = Die(np.array([1, 2]))

        die3.change_weight(2,0) 
        die4.change_weight(2, 0)
        game = Game([die3, die4])
        game.play(5)  

        analyzer = Analyzer(game)  
        jackpots = analyzer.jackpot()  
        # Assert the correctness of the jackpot count
        self.assertEqual(jackpots, 5, "Jackpot count should equal the number of rolls with identical faces.")

    def test_face_count(self):
        """Test that face_count returns a DataFrame."""
        face_counts = self.analyzer.face_count()
        self.assertIsInstance(face_counts, pd.DataFrame)
        self.assertIn(1, face_counts.columns)  

    def test_combo_count(self):
        """Test that combo_count returns a DataFrame."""
        combos = self.analyzer.combo_count()
        self.assertIsInstance(combos, pd.DataFrame)
        self.assertIn('Count', combos.columns)

    def test_permutation_count(self):
        """Test that permutation_count returns a DataFrame."""
        permutations = self.analyzer.permutation_count()
        self.assertIsInstance(permutations, pd.DataFrame)
        self.assertIn('Count', permutations.columns)

if __name__ == "__main__":
    unittest.main()
