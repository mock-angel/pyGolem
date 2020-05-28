

class PathFinder():
    def __init__(self):
        pass
    
    def init_Matrix(self, matrix_size):
        x, y = matrix_size
        
        matrix = []
        for i in range(y):
            matrix_row = []
            for j in range(x):
                matrix_row.append(0)
            
            matrix.append(matrix_row)
        self.driver_matrix = matrix
        
    def print(self):
        for r in self.driver_matrix:
            print_text = ""
            for cell in r:
                print_text += "  " + str(cell)
                
            print(print_text)
    
    def print_final(self):
        for c in self.driven_matrix:
            print_text = ""
            for r in c:
                print_text += "  " + str(r)
                
            print(print_text)
            
    def add_obstacle_point(self, point, value = 1):
        self.driver_matrix[point[1]][point[0]] = value
    
#     def add_obstacle_point(self, point1, point2, value = 1):
#        for i in range(point1[1] - point2[0]):
#            for ()
    def start(self, pos_start):
        self.start_cell = pos_start
        
    def end(self, pos_end):
        self.end_cell = pos_end
    
    def solve(self):
        self.create_nodes()
    
    def create_nodes(self):
        for 
    
if __name__ == "__main__":
    pf = PathFinder()
    pf.init_Matrix((10,10))
    pf.add_obstacle_point((1, 1))
    pf.add_obstacle_point((1, 2))
    pf.add_obstacle_point((1, 3))
    pf.add_obstacle_point((1, 4))
    pf.add_obstacle_point((1, 5))
    pf.add_obstacle_point((3, 1))
    pf.add_obstacle_point((3, 2))
    pf.add_obstacle_point((3, 3))
    pf.add_obstacle_point((3, 4))
    pf.add_obstacle_point((3, 5))
    pf.start((2, 0))
    pf.end((2, 6))
    pf.solve()
    pf.print()
