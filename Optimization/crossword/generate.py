import sys

from crossword import *
from copy import deepcopy
from random import sample, choice, randrange


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #V Object Variable
        var = []
        for v in self.domains:
            y = []
            var.append(v)
            for x in self.domains[v]:
                if len(x) != v.length:
                    y.append(x)
            for i in y:
                self.domains[v].remove(i)
        
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        control = False
        coordinate = None
        if x != y:
            coordinate = self.crossword.overlaps[x,y]
        a = dict()
        if coordinate:
            valueX = self.domains[x]
            valueY = self.domains[y]
            for v1 in valueX:
                a[v1] = 0
                for v2 in valueY:
                    if v1[coordinate[0]] != v2[coordinate[1]]:
                        a[v1] += 1
            for i in a:
                if a[i] == len(self.domains[y]):
                    self.domains[x].remove(i)
                    control = True
        return control

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        lista = [x for x in self.domains]
        
        while len(lista) != 0:
            x = lista[0]
            y = lista[1] if len(lista) > 1 else lista[0]
            lista.remove(x)
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    lista.append(z)
                    lista.append(x)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.domains):
            return True
        else:
            return False
            
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        dist = []
        for var in assignment:
            for var2 in assignment:
                if var != var2:
                    if assignment[var] != assignment[var2]:
                        dist.append(True)
                    else:
                        dist.append(False)
                        
            if len(assignment[var]) == var.length:
                dist.append(True)
            else:
                dist.append(False)
        if all(dist):
            return True
        else:
            return False
            
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        heristic = dict()
        for variable in self.domains:
            if variable != var:
                if self.crossword.overlaps[var, variable]:
                    coord = self.crossword.overlaps[var, variable]
                    for word in self.domains[var]:
                        heristic[word] = 0
                        for w in self.domains[variable]:
                            if w[coord[1]] != word[coord[0]]:
                                heristic[word] += 1
                            if w == word:
                                heristic[word] += 1

                                
        key = [(k, heristic[k]) for k in heristic]
        key.sort(key= lambda tuple: tuple[1]) 
        
        return [x[0] for x in key]
                        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        keys = [(var,len(self.domains[var])) for var in self.domains if not var in assignment]
        keys.sort(key=lambda tuple: tuple[1])
        for k in keys:
            for i in keys:
                if k != i:
                    if k[1] == i[1]:
                        nk = len(self.crossword.neighbors(k[0]))   
                        ni = len(self.crossword.neighbors(i[0]))
                        if nk > ni:
                            return k[0]
                        elif ni > nk:
                            return i[0]
                        else:
                            return choice([k[0],i[0]])
                           
        return keys[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        aux = []
        
        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
    
                assignment[var] = value
                result = self.backtrack(assignment)
                if result:
                    return result
            aux.append(value)
        [assignment.pop(v) for v in aux if v in assignment]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()
    
    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
