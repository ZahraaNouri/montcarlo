# Die Class

import pandas as pd
import numpy as np

class Die():
    """
    A class representing a die with customizable faces and weights.

    A Die object allows rolling to generate random outcomes, adjusting the
    probability of each face via weights, and querying the current state of
    the die.

    Attributes:
    faces (np.ndarray): An array of unique symbols or numbers representing the die faces.
    w (list): A list of weights associated with each face. Defaults to 1.0 for all faces.
    __die_df (pd.Series): A private pandas Series holding faces and their weights.
    """

    
    def __init__(self, faces=[1, 2, 3, 4, 5, 6]):
          
        """
        Initializes a die with the given faces and assigns equal weights to each face, checks the faces to be 
        numpay array, checks the faces to avoid similar faces, and creates a dataframe of faces and weights (by default 1)

        Inputs:
            faces (np.ndarray): A NumPy array of unique symbols or numbers representing the die faces. Default value is 1 to 6 (standard dice)

        Raises:
            TypeError: If faces is not a NumPy array.
            ValueError: If faces are not unique or contain invalid data types (must be numeric or strings).

        Attributes:
            __die_df (pd.Series): A private pandas Series with faces as the index and weights as values.
        """
        
        self.faces = faces

        # Check if faces is a numpy array
        if not isinstance(self.faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array!")

        # Check for uniqueness of the faces
        if len(np.unique(self.faces)) != len(self.faces):
            raise ValueError("Faces are not Unique.")

        # Check for face type (only numbers and strings)
        arr_type = self.faces.dtype
        if not (np.issubdtype(arr_type, np.str_) or np.issubdtype(arr_type, np.number)):
            raise ValueError("Please Enter Number or String as Die Faces.")

        # Creating weight index series
        self.w = [1 for _ in range(len(self.faces))]

        # Save data_frame
        self.__die_df = pd.Series(self.w, index=self.faces)
    

    def change_weight(self, face, new_weight):
        """
        Changes the weight of a specified face of the die.

        Inputs:
            face (str or int): The face whose weight is to be changed.
            new_weight (float): The new weight for the specified face. Must be positive and castable to a number.

        Raises:
            IndexError: If the specified face is not valid.
            TypeError: If the new weight is not numeric or cannot be cast to a float.
        """
        
        # Check if the face is in the faces list
        if face in self.faces:
            #check if the weight is valid (positive number)
            if not isinstance(new_weight, (int, float)): 
                try:
                    new_weight=float(new_weight)
                except(ValueError, TypeError):
                    raise TypeError("Weight must be a number or castable to a number.")


            #check if the weight is positive 
            if new_weight < 0:
                raise ValueError("Weight must be positive")
                
            # Change the corresponding weight in the Series
            self.__die_df[face] = new_weight
            print(f"Weight of {face} changed to {new_weight}")
            
        else:
            raise IndexError("Face not found among the die faces")
            
                
    def roll_time(self, times=1):
        """
        Rolls the die a specified number of times and saves the result in a dataframe

        Inputs:
            times (int): The number of times to roll the die. Defaults to 1.

        Returns:
           samples(list): A list of outcomes corresponding to the rolls.

        Raises:
            ValueError: If 'times' is not a positive integer.
        """
        
        
        if not isinstance(times, int) or times <= 0:
            raise ValueError("The 'times' parameter must be a positive integer.")
        
        samples=self.__die_df.sample(n=times, replace=True, weights=self.__die_df.values).index.tolist()
        return samples

    def current_state(self):
        """
        Retrieves the current state of the die, including its faces and weights.

        Returns:
            die_df(pd.Series): A pandas Series with faces as the index and their respective weights as values.

        """
        #Provide a copy of the private data frame.
        die_df = self.__die_df.copy()
        return die_df

    def get_faces(self):
        """
        Retrieves the face values of the die.

        Returns:
            self.faces(np.ndarray): The faces of the die as a NumPy array.

        """
        return self.faces



#--------------------------------------------------------------------------------------


#Game Class 

import pandas as pd
import numpy as np

class Game():

    """
    A class representing a game consisting of rolling one or more dice multiple times.

    A Game object accepts a list of similar Die objects, rolls them for a specified
    number of times, and records the results. Results can be retrieved in wide or narrow formats.

    Attributes:
        __dice_list (list): A private list of Die objects used in the game.
        __play_df (pd.DataFrame): A private DataFrame holding the results of the most recent play.
    """

    
    def __init__(self, dice_list):
        """
        Initializes a game with a list of similar Die objects.

        Inputs:
            dice_list (list): A list of Die objects to be used in the game.

        Raises:
            TypeError: If dice_list is not a list or does not contain Die objects.
            ValueError: If the dice in the list do not have the same faces.
        """

        #Validate that the input is a list 
        if not isinstance(dice_list, list):
            raise TypeError("dice_list must be a list of Die objects.")
        
        #check that all dices have the same faces 
        faces_list = [set(die.get_faces()) for die in dice_list]
        if not all (faces == faces_list[0] for faces in faces_list):
            raise ValueError("All dice in the game must have the same faces")
        
        self.__dice_list = dice_list
        self.__play_df = pd.DataFrame()


    def play(self, times):

        """
        Rolls all dice in the game a specified number of times and records the outcomes.

        Inputs:
            times (int): The number of times to roll the dice.

        Raises:
            ValueError: If 'times' is not a positive integer.

        Changes:
            Updates the private attribute __play_df with the results of the rolls.
        """
        
        if not isinstance(times, int) or times <= 0:
            raise ValueError("The 'times' parameter must be a positive integer.")
        self.times = times
      
        # Reset the play data frame for a new game
        self.__play_df = pd.DataFrame()

        for i, dice in enumerate(self.__dice_list):
            roll_result = dice.roll_time(times)
            self.__play_df[i] = roll_result  # Use zero-based indexing for columns

        self.__play_df.index = range(1, times + 1)
        self.__play_df.columns = range(1, len(self.__dice_list)+1)

    def show_results(self, wide=1):

        """
        Returns the results of the most recent game in wide or narrow format.

        Input:
            wide (int): Format option for results. 1 for wide format (default) and 0 for narrow format.

        Returns:
            self.__play_df.copy(pd.DataFrame): A DataFrame of the results in the selected format.

        Raises:
            ValueError: If the 'wide' parameter is not 0 or 1.
        """

        if not (wide == 0 or wide == 1):
            raise ValueError("Wrong Entry for show results. Enter 1 for wide and 0 for narrow dataframe format")
        
        if wide == 0:
            narrow_df = self.__play_df.stack().reset_index()
            narrow_df.columns = ['Roll Number', 'Die Number', 'Outcome']
            narrow_df.set_index(['Roll Number', 'Die Number'], inplace=True)
            return narrow_df
        else:
            return self.__play_df.copy()
    
    def get_dice_faces(self):
        """
        Retrieves the face values of the dice used in the game.

        Returns:
            self.dice_faces(np.ndarray): An array of face values shared by all dice in the game.
        """
        self.dice_faces = self.__dice_list[0].get_faces()
        return(self.dice_faces)

    def get_event_number(self):
        """
        Retrieves the number of rolls (events) in the most recent game.

        Returns:
            self.times(int): The number of rolls played in the game.
        """
        return self.times



#-----------------------------------------------------------------------------------

#Analyzer Class

import pandas as pd
import numpy as np

class Analyzer():
    """
    A class to analyze the statistical properties of the outcomes from a single game.

    An Analyzer object computes metrics such as jackpots, face counts, distinct
    combinations, and permutations from the results of a game.

    Attributes:
        results (pd.DataFrame): The outcomes of the most recent game in wide format.
    """

    def __init__(self, game):
        """
        Initializes the Analyzer with a Game object and checks if the game is an object of Game

        Inputs:
            game (Game): A Game object containing the results to analyze.

        Raises:
            ValueError: If the input is not a Game object.
        """
        if not isinstance(game,Game):
            raise ValueError("Please Enter a Game Object")

        #  Acess the game's results in wide format
        self.results=game.show_results(1)

        self.faces=game.get_dice_faces()
        self.event_number = game.get_event_number()
      
    
    def jackpot(self):

        """
        Counts the number of jackpots in the game results.

        A jackpot is defined as all dice showing the same face in a roll.

        Returns:
            self.jackpot(int): The number of jackpots.
        """
        
        self.jackpot=pd.DataFrame()
        self.jackpot = self.results.nunique(axis = 1) == 1
    
      
        return(sum(self.jackpot))
        

    def face_count(self):
        """
        Computes the count of each face for every roll in the game.

        This method calculates how many times each face appears in each roll
        and organizes the results into a DataFrame.

        Returns:
        self.face_counter(pd.DataFrame): A DataFrame where:
                - Rows represent roll numbers.
                - Columns represent the face values of the dice.
                - Cell values are the counts of each face in a roll.
        """

        
        
        #create a df containing die faces 
        self.face_counter = pd.DataFrame(index= range(1, self.event_number+1), columns = self.faces)

        #Counting the number of faces showed up in each event 
        for face, event in self.results.iterrows():
            counts=event.value_counts()
            self.face_counter.loc[face] = [counts.get(col, 0) for col in self.faces]
        

        return self.face_counter

    def combo_count(self):

        """
        Computes distinct combinations of faces rolled and their counts.

        Combinations are order-independent and may include repetitions.

        Returns:
            combo_counts(pd.DataFrame): A DataFrame with combinations as the index and their counts in a column named 'Count'.
        """

        #convert each row to a sorted tuple -- order not matter 
        combos=self.results.apply(lambda x: tuple(sorted(x)), axis=1)
        
        #count occurrences of each combination 
        combo_counts = combos.value_counts().reset_index()
        combo_counts.columns = ['Combination', 'Count']
        combo_counts.set_index('Combination', inplace = True)
        
        return combo_counts
    
    def permutation_count(self):
        """
        Computes distinct permutations of faces rolled and their counts.

        Permutations are order-dependent and may include repetitions.

        Returns:
            pd.DataFrame: A DataFrame with permutations as the index and their counts in a column named 'Count'.

        """
        #convert each row to a sorted tuple -- order matters
        per=self.results.apply(lambda x: tuple(x), axis=1)
        
        #count occurrences of each combination 
        per_counts = per.value_counts().reset_index()
        
        per_counts.columns = ['Permutation', 'Count']
        per_counts.set_index('Permutation', inplace = True)
        return per_counts
    
        
