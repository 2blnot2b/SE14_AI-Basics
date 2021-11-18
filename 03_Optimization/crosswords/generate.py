import sys
import time
from crossword import *
from collections import deque

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

        img.save(f"outputs/{filename}")

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

        # Iterating over all variables and their potential words
        for var, words in self.domains.items():
            words_to_remove = set()
            for word in words:

                # If variable can't hold the length of the word, then remove it!
                if len(word) != var.length:

                    # Removing here means adding the word 1 by 1 to the set called words_to_remove, before removing them all at once
                    words_to_remove.add(word)

            # Subtracting all words that aren't suitable from variable's domain
            self.domains[var] = words.difference(words_to_remove)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Assign false to revised to check any consistency
        revised = False

        # Finding overlaps between two nodes in the shared grid
        overlap = self.crossword.overlaps[x, y]  

        if overlap:
            v1, v2 = overlap

            # Storing all x domains to remove
            x_doms_to_remove = set()
            for x_i in self.domains[x]:
                overlaps = False

                # Evaluating any overlaps between x variables and y variables
                for y_j in self.domains[y]:
                    if x_i != y_j and x_i[v1] == y_j[v2]:
                        overlaps = True
                        break

                # Whenever no overlaps between x and y variables, add those to the x domains to be removed
                if not overlaps:
                    x_doms_to_remove.add(x_i)
            
            # If there are variables saved in x domains, remove it!
            if x_doms_to_remove:
                self.domains[x] = self.domains[x].difference(x_doms_to_remove)

                 # Making sure that the revision made after those x variables are removed
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # if given arcs is none, initialize a queue with all edges (arcs)
        if arcs is None:
            arcs = deque()
            for v1 in self.crossword.variables:
                for v2 in self.crossword.neighbors(v1):
                    arcs.appendleft((v1, v2))

        # If arcs is not None, convert it to deque!
        else:
            arcs = deque(arcs)

        while arcs:
            x, y = arcs.pop()
            
            # Revising every combination of nodes in the edge positions (arcs) 
            if self.revise(x, y):
                if len(self.domains[x]) == 0:

                    # If there are no variables for x, then arc consistency is not possible
                    return False

                # Preparing the queue by adding the edges between x neighbours (excluding y) and x
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.appendleft((z, x))

        # All smooth? Return True
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in self.crossword.variables:

            # No variable assignedt == No words assigned, return False
            if var not in assignment.keys():
                return False

            # Variable assigned == Word assigned, if but the words are not in the available list, return False
            if assignment[var] not in self.crossword.words:
                return False

        # All smooth? Return True
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Evaluating the length of the assigned word is of the proper length for the variable
        for var_x, word_x in assignment.items():
            if var_x.length != len(word_x):
                return False

            for var_y, word_y in assignment.items():
                if var_x != var_y:

                    # Checking if the word is unique since it can't be used in any other variable
                    if word_x == word_y:
                        return False

                    # PReparation to check for overlapping characters in the variable
                    overlap = self.crossword.overlaps[var_x, var_y]

                    # If any overlap, make sure no conflict in the characters
                    if overlap:
                        i, j = overlap

                        # Different characters means inconsistency == conflicts!
                        if word_x[i] != word_y[j]:  
                            return False

        # All smooth? Return True
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Assigning all neighbours for the given variable
        neighbors = self.crossword.neighbors(var)
        
        # Iterating over all assignments to check if some neighbouring variables are already assigned to a word
        for each_assignment in assignment:

            # If variable is in neighbours and in assignment, the variable already has a value and is not considered a neighbour
            if each_assignment in neighbors:

                # So we remove it from the neighbourhood!
                neighbors.remove(each_assignment)

        # The result will be sorted according to Least-Constraining Values (heuristics)
        result = []

        for variable in self.domains[var]:

            # Counting the domains that will be exluded from neighboring variables
            to_exclude = 0  

            for neighbor in neighbors:
                for variable_2 in self.domains[neighbor]:
                    overlap = self.crossword.overlaps[var, neighbor]

                    # Any overlapping means that the domain will be excluded from the variable
                    if overlap:
                        i, j = overlap
                        if variable[i] != variable_2[j]:
                            to_exclude += 1

            # Storing the variable with the number of the exluded domains
            result.append([variable, to_exclude])

        # Sorting all variables by the number of excluded domains they will eliminate
        result.sort(key=lambda x: x[1])

        # Returning only the list of variables
        return [i[0] for i in result]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # List consists of potential variables to be considered using minimum remaining value heuristic and degree heuristic:
        # Minimum remaining values (MRV): choose the variable with the fewest possible values
        potential_vars = []

        # Iterating over all variables
        for var in self.crossword.variables:
            if var not in assignment: 

                # Adding any unassigned variable to the list with the number of domains (minimum remaining values)
                # and number of neighbors (degree heuristic)
                potential_vars.append([var, len(self.domains[var]), len(self.crossword.neighbors(var))])

        # Ordering potential variables by the number of available domains (ascending) and number of neighbours (descending)
        if potential_vars:
            potential_vars.sort(key=lambda x: (x[1], -x[2]))
            return potential_vars[0][0]

        # No potential variables? Return None!
        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Start counting the time complexity for Back Tracking algorithm
        start = time.time()

        # Checking if all words have been assigned to variables
        if self.assignment_complete(assignment):
            return assignment

        # Selecting unassigned variable from the assignment for its domain
        var = self.select_unassigned_variable(assignment)

        # Iterating over all values in the domain
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val

            # Checking if assignment still consistent (the words are unique and the overlaps consits of the same characters)
            if self.consistent(assignment):

                # Preparation for recursive execution of "Backtracking Search" algorithm
                result = self.backtrack(assignment)

                # Recursive is done to to check the consistency of further values from the chosen assignment
                # If the assignment is taken by the result, then the variable works and everything is consistent!
                if result:

                    # Output describes one of the performance criterias of Back Tracking algorithm; Time complexity
                    end = time.time()
                    print(f"\n<<< Back Tracking Search Time Complexity 'O(2^N)': {round(end - start, 13)} >>>\n")

                    return result

                # If instead None is assigned to the result, then remove the variable from assignment since it doesn't give any solution!
                assignment.pop(var, None)

        # Output describes one of the performance criterias of Back Tracking algorithm; Time complexity
        end = time.time()
        print(f"\n<<< Back Tracking Search Time Complexity 'O(2^N)': {round(end - start, 13)} >>>\n")

        # Returning None means that the chosen variable can't be assigned into the assignment
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
