import numpy as np

class spatialGame():
    """This class produces an array representing the different variables in the spatial game"""

    def __init__(self, canvas_width, canvas_height, cell_size, dist, variables, matrix, invade, neighbourhood, boundary, dynamicval):
        self.width = int(canvas_width/int(cell_size)) #assings all the object variables
        self.height = int(canvas_height/int(cell_size))
        self.cell_size = int(cell_size)
        self.variables = variables
        self.matrix = matrix
        self.neighbourhood = neighbourhood
        self.boundary = boundary
        self.a = float(matrix[0][0])
        self.b = float(matrix[0][1])
        self.c = float(matrix[1][0])
        self.d = float(matrix[1][1])
        self.invade = invade
        self.payoffGrid=[]
        self.cells=[]
        self.stratA = 0
        self.stratB = 0
        self.stratC = 0
        self.dynamicval = dynamicval
        if variables == 2: #Creates and populates the array when there are 2 possible strategies
            if self.invade == 0: #if not an invade game
                start = np.random.choice([1,2],(self.width,self.height),p=dist) #uses numpy arrays to randomly generate a grid
                for row in range(0,self.height): #translates the grid from an array into a list of lists
                    self.cells.append([])
                    for col in range(0,self.width):
                        self.cells[row].append(start[row][col])
                self.e = 0
                self.f = 0
                self.g = 0
                self.h = 0
                self.i = 0
            elif self.invade ==1: #if it is an invade game
                for x in range(self.height): #creates a grid filled with behaviour strategy A
                    self.cells.append([])
                    for y in range(self.width):
                        self.cells[x].append(1)
                self.cells[int(self.width/2)][int(self.height/2)]=2 #inserts a cell with behaviour strategy B at the center of the grid
                self.e = 0
                self.f = 0
                self.g = 0
                self.h = 0
                self.i = 0
        elif variables == 3: #Creates and populates the array when there are 3 possible strategies
            self.e = float(matrix[0][2])
            self.f = float(matrix[1][2])
            self.g = float(matrix[2][0])
            self.h = float(matrix[2][1])
            self.i = float(matrix[2][2])
            start = np.random.choice([1,2,3],(self.width,self.height),p=dist) #uses numpy arrays to randomly generate a grid
            for row in range(0,self.height): #translates the grid from an array into a list of lists
                self.cells.append([])
                for col in range(0,self.width):
                    self.cells[row].append(start[row][col])

    def run_rules(self): #This function returns a new array after running the specified set of rules on the population
        temp = [] #creates a temporary grid to store the values of the array #NEEDS CHANGING TO ARRAY
        payoff_grid = self.create_grid(self.cells,self.a,self.b,self.c,self.d,self.e,self.f,self.g,self.h,self.i)
        if self.boundary == 1:
            payoffGrid = self.fixed(payoff_grid)
            indexGrid = self.fixed(self.cells)
        elif self.boundary ==2:
            payoffGrid = self.reflective(payoff_grid)
            indexGrid = self.reflective(self.cells)
        else:
            payoffGrid = self.periodic(payoff_grid)
            indexGrid = self.periodic(self.cells)
        for x in range(len(payoffGrid)-2):
            temp.append([])
            for y in range(len(payoffGrid[x])-2):
                if self.neighbourhood == 2: #Attains payoff values for the cells in Von nuemann neighbourhood
                    neighbour_grid = [payoffGrid[x][y+1],
                                      payoffGrid[x+1][y],
                                      payoffGrid[x+1][y+1],
                                      payoffGrid[x+1][y+2],
                                      payoffGrid[x+2][y+1]]
                    ind = neighbour_grid.index(max(neighbour_grid)) #calculates the index of the cell with the heighest payoff
                    x_val = [x,x+1,x+1,x+1,x+2]
                    y_val = [y+1,y,y+1,y+2,y+1]
                    ix = x_val[ind] #transaltes the index from the neighour grid onto the index of the actual cell
                    iy = y_val[ind]
                elif self.neighbourhood == 1: #Attains values for the cells in Moore Neighbourhood
                    neighbour_grid = [payoffGrid[x][y],
                                      payoffGrid[x][y+1],
                                      payoffGrid[x][y+2],
                                      payoffGrid[x+1][y],
                                      payoffGrid[x+1][y+1],
                                      payoffGrid[x+1][y+2],
                                      payoffGrid[x+2][y],
                                      payoffGrid[x+2][y+1],
                                      payoffGrid[x+2][y+2]]
                    ind = neighbour_grid.index(max(neighbour_grid))  #calculates the index of the cell with the heighest payoff
                    x_val = [x,x,x,x+1,x+1,x+1,x+2,x+2,x+2]
                    y_val = [y,y+1,y+2,y,y+1,y+2,y,y+1,y+2]
                    ix = x_val[ind] #transaltes the index from the neighour grid onto the index of the actual cell
                    iy = y_val[ind]
                temp[x].append(indexGrid[ix][iy]) #appends the temporary grid with the strategy that had the highest payoff
        if self.dynamicval ==1:
            self.cells = self.dynamic(temp) #sets the temporary grid equal to our actual grid and calls the dynamic function
        elif self.dynamicval ==0:
            self.cells = temp

    def create_grid(self,cells, a, b, c, d, e, f, g, h, i):
        self.stratA = 0
        self.stratB = 0
        self.stratC = 0
        payoffGrid = [] #creates a grid to store the values
        if self.boundary ==1:
            cellkey = self.fixed(cells)
        elif self.boundary ==2:
            cellkey = self.reflective(cells)
        if self.boundary == 3:
            cellkey = self.periodic(cells) #extends the grid so it satisfies boundary conditions
        for x in range(self.height):
            payoffGrid.append([])
            for y in range(self.width):
                if self.neighbourhood == 2: #Attains values for the focal cells in Von nuemann neighbourhood
                    neighbour_grid = [cellkey[x][y+1],
                                      cellkey[x+1][y],
                                      cellkey[x+1][y+2],
                                      cellkey[x+2][y+1]]
                elif self.neighbourhood == 1:
                    neighbour_grid = [cellkey[x][y], #Attains values in the focal cells Moore neighbourhood
                                      cellkey[x][y+1],
                                      cellkey[x][y+2],
                                      cellkey[x+1][y],
                                      cellkey[x+1][y+2],
                                      cellkey[x+2][y],
                                      cellkey[x+2][y+1],
                                      cellkey[x+2][y+2]]
                if (self.cells[x][y] == 1) or (self.cells[x][y] == 4):  #Considers the case where the focal cell is strategy A
                    A = neighbour_grid.count(1) + neighbour_grid.count(4) #Counts the number of each strategy in it's Moore Neighbourhood
                    B = neighbour_grid.count(2) + neighbour_grid.count(5)
                    C = neighbour_grid.count(3) + neighbour_grid.count(6)
                    payoff = a*A + b*B + e*C
                    self.stratA=self.stratA+1
                    payoffGrid[x].append(payoff)
                elif (self.cells[x][y] == 2) or (self.cells[x][y] == 5):#Considers the case where the focal cell is strategy B
                    A = neighbour_grid.count(1) + neighbour_grid.count(4) #Counts the number of each strategy in it's Moore Neighbourhood
                    B = neighbour_grid.count(2) + neighbour_grid.count(5)
                    C = neighbour_grid.count(3) + neighbour_grid.count(6)
                    payoff = c*A + d*B + f*C
                    self.stratB=self.stratB+1
                    payoffGrid[x].append(payoff)
                elif (self.cells[x][y] == 3) or (self.cells[x][y] ==6):#Considers the case where the focal cell is strategy C
                    A = neighbour_grid.count(1) + neighbour_grid.count(4) #Counts the number of each strategy in it's Moore Neighbourhood
                    B = neighbour_grid.count(2) + neighbour_grid.count(5)
                    C = neighbour_grid.count(3) + neighbour_grid.count(6)
                    payoff = g*A + h*B + i*C
                    self.stratC=self.stratC+1
                    payoffGrid[x].append(payoff)
        return payoffGrid #returns a grid with updated payoff strategies

    def dynamic(self, lst): #This function allows the array to be viewed dynamically when being viewed without animation
        for x in range(len(lst)):
            for y in range(len(lst[0])):
                if (lst[x][y] == 2 or lst[x][y] == 5) and (self.cells[x][y] == 2 or self.cells[x][y] == 5):
                    lst[x][y] = 2 #represents a strategy A that was a strategy A in the previous gen
                elif (lst[x][y] == 1 or lst[x][y] == 4) and (self.cells[x][y] == 1 or self.cells[x][y] == 4):
                    lst[x][y] = 1 #represents a strategy B that was a strategy B in the previous gen
                elif (lst[x][y] == 2 or lst[x][y] == 5) and (self.cells[x][y] != 2 or self.cells[x][y] != 5):
                    lst[x][y] = 5 #represents a strategy B that wasn't a strategy B in the previous gen
                elif (lst[x][y] == 1 or lst[x][y] == 4) and (self.cells[x][y] != 1 or self.cells[x][y] != 4):
                    lst[x][y] = 4 #represents a strategy A that wasn't a strategy A in the previous gen
                elif (lst[x][y] == 3 or lst[x][y] == 6) and (self.cells[x][y] == 3 or self.cells[x][y] == 6):
                    lst[x][y] = 3 #represents a strategy C that was a strategy C in the previous gen
                elif (lst[x][y] == 3 or lst[x][y] == 6) and (self.cells[x][y] != 3 or self.cells[x][y] != 6):
                    lst[x][y] = 6 #represents a strategy C that wasn't a strategy C in the previous gen
        return lst

    def periodic(self,cells): #This extends the grid with periodic boundary conditions
        first_col = []
        last_col = []
        cellperiodic = []
        for x in range(len(cells)): #creates a new grid identical to cells
            cellperiodic.append([])
            for y in range(len(cells[x])):
                cellperiodic[x].append(cells[x][y])
        cellperiodic.insert(0,cellperiodic[-1]) #inserts the last row at the start of the list
        cellperiodic.append(cellperiodic[1]) #appends the first row to the end of the list
        for x in range(len(cellperiodic)):
            first_col.append(cellperiodic[x][0]) #calculates the values in the first column
        for y in range(len(cellperiodic)):
            last_col.append(cellperiodic[y][-1]) #calculates the value in the last column
        for i in range(len(first_col)-2):
            cellperiodic[i].append(first_col[i]) #appends the first column entry to the last column
        for j in range(len(last_col)-2):
            cellperiodic[j].insert(0,last_col[j]) #inserts the last column before the first column
        return cellperiodic

    def fixed(self,cells): #This extends the grid with fixed boundary conditions
        first_col = []
        last_col = []
        cellfixed = []
        for x in range(len(cells)): #creates a new grid identical to cells
            cellfixed.append([])
            for y in range(len(cells[x])):
                cellfixed[x].append(cells[x][y])
        for x in range(len(cells[0])):
            first_col.append(1)
            last_col.append(1)
        cellfixed.insert(0,first_col) #inserts the last row at the start of the list
        cellfixed.append(last_col)
        for i in range(len(cellfixed)):
            cellfixed[i].append(1) #appends the first column entry to the last column
        for j in range(len(cellfixed)):
            cellfixed[j].insert(0,1) #inserts the last column before the first column
        return cellfixed

    def reflective(self,cells): #This extends the grid with periodic boundary conditions
        first_col = []
        last_col = []
        cellreflective = []
        for x in range(len(cells)): #creates a new grid identical to cells
            cellreflective.append([])
            for y in range(len(cells[x])):
                cellreflective[x].append(cells[x][y])
        cellreflective.insert(0,cellreflective[0]) #inserts the last row at the start of the list
        cellreflective.append(cellreflective[-1])#appends the first row to the end of the list
        for g in range(len(cellreflective)):
            first_col.append(cellreflective[g][0]) #calculates the values in the first column
        for h in range(len(cellreflective)):
            last_col.append(cellreflective[h][-1]) #calculates the value in the last column
        cellfix = []
        for x in range(len(cellreflective)): #creates a new grid identical to cells
            cellfix.append([])
            for y in range(len(cellreflective[x])):
                cellfix[x].append(cellreflective[x][y])
        for i in range(len(first_col)):
            cellfix[i].insert(0,first_col[i])
        for j in range(len(last_col)):
            cellfix[j].append(last_col[j])
        return cellfix
