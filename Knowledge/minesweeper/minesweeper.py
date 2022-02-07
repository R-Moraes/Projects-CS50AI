import itertools
import random
from copy import deepcopy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a teconditions['empty_sent']t-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|conditions['empty_sent']", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines = set()
        self.safes = set()
        
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            for cell in self.cells:
                self.mines.add(cell)
                
        return self.mines
        
    def coordinate(self, cell):
        coord = set()
        i,j = cell
        if i == 0:
            if j == 0:
                coord.add((i,j+1))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
            elif j == 7:
                coord.add((i,j-1))
                coord.add((i+1,j))
                coord.add((i+1,j-1))
            else:
                coord.add((i,j-1))
                coord.add((i,j+1))
                coord.add((i+1,j-1))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
        elif i == 7:
            if j == 0:
                coord.add((i,j+1))
                coord.add((i-1,j))
                coord.add((i-1,j+1))
            elif j == 7:
                coord.add((i,j-1))
                coord.add((i-1,j))
                coord.add((i-1,j-1))
            else:
                coord.add((i,j-1))
                coord.add((i,j+1))
                coord.add((i-1,j-1))
                coord.add((i-1,j))
                coord.add((i-1,j+1))
        else:
            if j == 0:
                coord.add((i-1,j))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
                coord.add((i-1,j+1))
                coord.add((i,j+1))
            elif j == 7:
                coord.add((i-1,j))
                coord.add((i+1,j))
                coord.add((i+1,j-1))
                coord.add((i-1,j-1))
                coord.add((i,j-1))
            else:
                coord.add((i-1,j-1))
                coord.add((i-1,j))
                coord.add((i-1,j+1))
                coord.add((i,j-1))
                coord.add((i,j+1))
                coord.add((i+1,j-1))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
        
        return coord      

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        cells = None
        if self.count == 0:
            for i,j in self.cells:
                cells = self.coordinate((i,j))
        if cells:        
            for cell in cells:
                self.safes.add(cell)
                
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            self.mines.add(cell)
            
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safes.add(cell)
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        self.position = []
        self.positions()
        
    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def coordinate(self, cell):
        coord = set()
        i,j = cell
        if i == 0:
            if j == 0:
                coord.add((i,j+1))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
            elif j == (self.width-1):
                coord.add((i,j-1))
                coord.add((i+1,j))
                coord.add((i+1,j-1))
            else:
                coord.add((i,j-1))
                coord.add((i,j+1))
                coord.add((i+1,j-1))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
        elif i == (self.height-1):
            if j == 0:
                coord.add((i,j+1))
                coord.add((i-1,j))
                coord.add((i-1,j+1))
            elif j == (self.width-1):
                coord.add((i,j-1))
                coord.add((i-1,j))
                coord.add((i-1,j-1))
            else:
                coord.add((i,j-1))
                coord.add((i,j+1))
                coord.add((i-1,j-1))
                coord.add((i-1,j))
                coord.add((i-1,j+1))
        else:
            if j == 0:
                coord.add((i-1,j))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
                coord.add((i-1,j+1))
                coord.add((i,j+1))
            elif j == (self.width-1):
                coord.add((i-1,j))
                coord.add((i+1,j))
                coord.add((i+1,j-1))
                coord.add((i-1,j-1))
                coord.add((i,j-1))
            else:
                coord.add((i-1,j-1))
                coord.add((i-1,j))
                coord.add((i-1,j+1))
                coord.add((i,j-1))
                coord.add((i,j+1))
                coord.add((i+1,j-1))
                coord.add((i+1,j))
                coord.add((i+1,j+1))
        
        return coord 
    
    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from econditions['empty_sent']isting knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbors = self.coordinate(cell)
        conditions = {
            'neighbors_safe': [],
            'empty_sent': [],
            'safe': [],
            'cells_mine': [],
            'mine': [],
            'cells_safe': [],
            'made': []
        }
    
        if count == 0:
            for cell in neighbors:
                self.mark_safe(cell)
                conditions['neighbors_safe'].append(cell)
        if len(neighbors) == count:
            for cell in neighbors: self.mark_mine(cell)
        for i in conditions['neighbors_safe']: neighbors.remove(i)
        
        if neighbors: self.knowledge.append(Sentence(neighbors, count))
        new_klg = None 
           
        for sent in self.knowledge:
            if not sent.cells: conditions['empty_sent'].append(sent)
            for cell in sent.cells:
                if cell in self.safes: conditions['safe'].append(cell)
                if cell in self.mines: conditions['mine'].append(cell)
                if cell in self.moves_made: conditions['made'].append(cell)
            for i in conditions['safe']:
                sent.cells.remove(i)
                self.mark_safe(i)
            for i in conditions['mine']:
                if not i in self.mines:
                    sent.cells.remove(i)
                    self.mark_mine(i)
            for i in conditions['made']:
                if not i in self.moves_made: sent.cells.remove(i)
            if len(sent.cells) == sent.count:
                for cell in sent.cells: conditions['cells_mine'].append(cell)
                for i in conditions['cells_mine']: self.mark_mine(i)
            if sent.count == 0:
                for cell in sent.cells: conditions['cells_safe'].append(cell)
                for i in conditions['cells_safe']: self.mark_safe(i)
            if new_klg:
                if new_klg.cells <= sent.cells:
                    sub = sent.cells.difference(new_klg.cells)
                    new_count = sent.count - new_klg.count
                    if sub: self.knowledge.append(Sentence(sub, new_count))
        
        for i in conditions['empty_sent']:
            self.knowledge.remove(i) 
                      
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if not move in self.moves_made:
                self.position.remove(move)
                return move
        return None
    
    def positions(self):
        for i in range(self.height):
            for j in range(self.width):
                self.position.append((i,j))
                
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        sort = random.randrange(self.width)
        if self.position[sort] in self.position:
            coord = self.position[sort]
            self.position.remove(coord)
        if coord not in self.moves_made and not coord in self.mines:
            return coord
        return None            
