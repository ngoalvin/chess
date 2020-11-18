class Chess:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.history = {}
        self.move_counter = 1
    
    def add_piece(self, piece):
        x = piece.get_x()
        y = piece.get_y()
        self.board[x][y] = piece
    
    def get_board(self):
        return self.board
    
    def not_game_over(self):
        #checks if there are stil 2 kings on board
        king_count = 0
        for x in self.board:
            for y in x:
                if type(y) is King:
                    king_count += 1
        return king_count == 2
    def add_move(self):
        if self.move_counter not in self.history:
            self.history.update({self.move_counter:self.board})
            self.move_counter += 1
            
    def replay_turn(self, turn):
        print (dic[turn])
            
        
    
    def pprint(self):
        for i in range(8):
            for j in range(8):
                if not self.board[i][j]:
                    print("-", end=" ")
                else:
                    print(self.board[i][j].piece, end=" ")
            print()
                                     
class Piece:
    def __init__ (self, colour:str, x:int, y:int, piece_type:str):
        self.colour = colour.upper()
        self.piece_type = piece_type
        self.x = x
        self.y = y
        
        if self.check_colour(self.colour) == True:
            self.piece = self.colour + self.piece_type        
    
    def check_colour(self, colour:str):
        #checks if colour is valid
        if self.colour != 'W' and self.colour != 'B':
            raise ColourError("Colour must be 'W' or 'B'")
        return True
        
    def move(self, new_x:int, new_y:int, board):
        #checking if move is valid
        if (new_x != self.x or new_y != self.y) and self.move_is_valid(new_x, new_y, board):
            board[self.x][self.y] = None #changing current location to None
            board[new_x][new_y] = self #changing new location to object
            self.x = new_x #updating new location
            self.y = new_y
        else:
            return False
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def is_start_position(self):
        #checks if the piece is in the start position
        return self.start_x == self.x and self.start_y == self.y
    
    def is_ally(self, new_x:int, new_y:int, board):
        #check if a piece is an ally
        if board[new_x][new_y]:
            return board[self.x][self.y].colour == board[new_x][new_y].colour
        return False
    
    def can_kill(self, new_x, new_y, board):
        #checks if you can take a piece
        return not self.is_ally(new_x, new_y, board)
    
    def all_moves(self, board):
        lst = []
        for x in range(8):
            for y in range(8):
                if self.move_is_valid(x, y, board):
                    lst.append([x,y])
        return lst      
    
                    
    def check(self,board):
        moves = self.all_moves(board)
        for move in moves:
            if board[move[0]][move[1]] is not None:
                if 'KING' in board[move[0]][move[1]].piece:
                    if self.can_kill(move[0], move[1]):
                        return True
        return False
                
                        
                             
class King(Piece):
    def __init__(self, colour:str, x:int, y:int):
        super().__init__(colour, x, y, 'KING')
        self.start_x = x
        self.start_y = y         
        
    def move_is_valid(self, new_x:int, new_y:int, board):
        if (abs(new_x - self.x) < 2 and abs(new_y - self.y) < 2): #checks if you are moving 1 unit from any direction
            if board[new_x][new_y] is not None: #checks if location has a piece on it
                return can_kill(new_x, new_y, board) 
            return True 
        return False

class Rook(Piece):
    def __init__(self, colour:str, x:int, y:int):
        super().__init__(colour, x, y, 'ROOK')
        self.start_x = x
        self.start_y = y
        
    def move_is_valid(self, new_x:int, new_y:int, board):
        is_moving_left = new_x - self.x < 0 #checks if piece is moving left
        is_moving_down = new_y - self.y < 0 #checks if piece is moving down
        step_x = -1 if is_moving_left else 1
        step_y = -1 if is_moving_down else 1
        x = self.x
        y = self.y
        if not (0 <= new_x < 8) and (0 <= new_y < 8):
            return False#checks if valid x , y
        if (self.x == new_x and self.y != new_y):#checks if moving vertical
            while x == new_x and y != new_y: 
                y += step_y
                if board[x][y] is not None:#checks if theres a piece blocking in between locations
                    return False
            if board[new_x][new_y] is not None:#checks if the position has a piece
                return can_kill(new_x, new_y, board)#checks if you can take the piece
            return True
        if (self.x != new_x and self.y == new_y):
            while x != new_x and y == new_y: 
                x += step_x
                if board[x][y] is not None:
                    return False
            if board[new_x][new_y] is not None:
                return can_kill(new_x, new_y, board)
            return True

class Queen(Piece):
    def __init__(self, colour:str, x:int, y:int):
        super().__init__(colour, x, y, 'QUEEN')
        self.start_x = x
        self.start_y = y       
        
    def move_is_valid(self, new_x:int, new_y:int, board):
        is_moving_left = new_x - self.x < 0
        is_moving_down = new_y - self.y < 0   
        step_x = -1 if is_moving_left else 1
        step_y = -1 if is_moving_down else 1
        x = self.x
        y = self.y
        if not (0 <= new_x < 8) and (0 <= new_y < 8):
            return False
        if (abs(self.x - new_x)) == abs(self.y - new_y):#check if its a diagonal move
            while x != (new_x - step_x) and y != (new_y - step_y):
                x += step_x
                y += step_y
                if board[x][y] is not None:
                    return False
            if board[new_x][new_y] is not None:
                return self.can_kill(new_x, new_y, board)
            return True
        if (self.x == new_x and self.y != new_y):
            while y != (new_y - step_y):
                y += step_y
                if board[x][y] is not None:
                    return False
            if board[new_x][new_y] is not None:
                return self.can_kill(new_x, new_y, board)
            return True
        if (self.x != new_x and self.y == new_y):
            while x != (new_x - step_x):
                x += step_x
                if board[x][y] is not None:
                    return False
            if board[new_x][new_y] is not None:
                return self.can_kill(new_x, new_y, board)
            return True
          
    
class Knight(Piece):
    def __init__(self, colour:str, x:int, y:int):
        super().__init__(colour, x, y, 'KNIGHT')
        self.start_x = x
        self.start_y = y   
        
    def move_is_valid(self, new_x:int, new_y:int, board):
        if not ((0 <= new_x < 8) and (0 <= new_y < 8)):
            return False
        if abs(self.x - new_x) == 1 and abs(self.y - new_y) == 2:
            if board[new_x][new_y] is not None:
                return self.can_kill(new_x, new_y, board) 
            return True
        if abs(self.x - new_x) == 2 and abs (self.y - new_y) == 1:
            if board[new_x][new_y] is not None:
                return self.can_kill(new_x, new_y, board) 
            return True
        

class Bishop(Piece):
    def __init__(self, colour:str, x:int, y:int):
        super().__init__(colour, x, y, 'BISHOP') 
        self.start_x = x
        self.start_y = y       
        
    def move_is_valid(self, new_x:int, new_y:int, board): 
        is_moving_left = new_x - self.x < 0
        is_moving_down = new_y - self.y < 0
        step_x = -1 if is_moving_left else 1
        step_y = -1 if is_moving_down else 1
        x = self.x
        y = self.y        
        while x != (new_x - step_x) and y != (new_y - step_y)and (0 <= new_x < 8) and (0 <= new_y < 8):
            x += step_x
            y += step_y
            if board[x][y] is not None:
                return False          
        if (abs(self.x - new_x)) == abs(self.y - new_y):
            if board[new_x][new_y] is not None:
                return self.can_kill(new_x, new_y, board) 
            return True
        return False

class Pawn(Piece):
    def __init__(self, colour:str, x:int, y:int):
        super().__init__(colour, x, y, 'PAWN')
        self.start_x = x
        self.start_y = y         
        
    def move_is_valid(self, new_x:int, new_y:int,board):
        is_moving_left = new_x - self.x < 0
        is_moving_down = new_y - self.y < 0
        step_y = -1 if is_moving_down else 1
        x = self.x
        y = self.y
        if not (0 <= new_x < 8) and (0 <= new_y < 8):
            return False
        while x == new_x and y != (new_y - step_y):
            y += step_y
            if board[x][y] is not None:
                return False
            
        if self.is_start_position(): #checks if pawn hasnt move
            if board[self.x][self.y].colour == 'W':#checks if its white or black                  
                if abs(self.y - new_y) <= 2 and self.x == new_x and not is_moving_down:#if it is white make sure its not moving down
                    return True
                if abs(self.y - new_y) < 2 and ((self.x + 1) == new_x or (self.x - 1) == new_x):
                    if board[new_x][new_y]:
                        return self.can_kill(new_x, new_y, board)
                        
            else:
                if abs(self.y - new_y) <= 2 and self.x == new_x and is_moving_down:#if it is black make sure its moving down
                    return True
                if abs(self.y- new_y) < 2 and ((self.x + 1) == new_x or (self.x - 1) == new_x):
                    if board[new_x][new_y]:
                        return self.can_kill(new_x, new_y, board)
        
        
        if board[self.x][self.y].colour == 'W':               
            if abs(self.y - new_y) < 2 and self.x == new_x and not is_moving_down:
                return True
            if abs(self.y- new_y) < 2 and ((self.x + 1) == new_x or (self.x - 1) == new_x):
                if board[new_x][new_y]:
                    return self.can_kill(new_x, new_y, board)
        else:
            if abs(self.y - new_y) < 2 and self.x == new_x and is_moving_down:
                return True
            if abs(self.y- new_y) < 2 and ((self.x + 1) == new_x or (self.x - 1) == new_x):
                if board[new_x][new_y]:
                    return self.can_kill(new_x, new_y, board)
        return False

def main():
        
    NUM_PAWNS = 8
    chess = Chess()
    white_piece = []
    black_piece = []
    p1_turn = True
    p2_turn = True
    
    chess.add_piece(Rook('W', 0, 0))
    chess.add_piece(Knight('W', 1, 0))
    chess.add_piece(Bishop('W', 2, 0))
    chess.add_piece(Queen('W', 3, 0))
    chess.add_piece(King('W', 4, 0))
    chess.add_piece(Bishop('W', 5, 0))
    chess.add_piece(Knight('W', 6, 0))
    chess.add_piece(Rook('W', 7, 0))
    
    chess.add_piece(Rook('B', 0, 7))
    chess.add_piece(Knight('B', 1, 7))
    chess.add_piece(Bishop('B', 2, 7))
    chess.add_piece(Queen('B', 3, 7))
    chess.add_piece(King('B', 4, 7))
    chess.add_piece(Bishop('B', 5, 7))
    chess.add_piece(Knight('B', 6, 7))
    chess.add_piece(Rook('B', 7, 7))
        
        
    for i in range(NUM_PAWNS):
        chess.add_piece(Pawn('W', i , 1))
    
    for i in range(NUM_PAWNS):
        chess.add_piece(Pawn('B', i , 6))
    
    chess.pprint()
    
                
            
     
    while chess.not_game_over():
        while p1_turn:
            print('P1 turn')
            print('Please enter X location of piece you want to move')
            try:
                p1_x_piece = int(input())
            except:
                print('PLEASE USE AN INT')
                continue
            print('Please enter Y location of piece you want to move')
            try:
                p1_y_piece = int(input())
            except:
                print('PLEASE US AN INT')
                continue
            
            if chess.board[p1_x_piece][p1_y_piece] != None and chess.board[p1_x_piece][p1_y_piece].colour == 'W':
                available_moves = chess.board[p1_x_piece][p1_y_piece].all_moves(chess.board)
                print(available_moves)                
                print('Please enter X location of where to move')
                try:
                    p1_x_move = int(input())
                except:
                    print('PLEASE USE AN INT')
                    continue
                print('Please enter Y location of where to move')
                try:
                    p1_y_move = int(input())
                except:
                    print('PLEASE USE AN INT')
                    continue                    
                if chess.board[p1_x_piece][p1_y_piece].move(p1_x_move, p1_y_move, chess.board) == False:
                    print('Invalid move try again')
                    chess.pprint()
                else:
                    chess.add_move()
                    if chess.board[p1_x_move][p1_y_move].check(chess.board):
                        print('P2 King is in check')
                    p1_turn = False
                    p2_turn = True
                    chess.pprint()
                    
        while p2_turn:
            print('P2 turn')
            print('Please enter X location of piece you want to move')
            try:
                p2_x_piece = int(input())
            except:
                print('PLEASE USE AN INT')
                continue
            print('Please enter Y location of piece you want to move')
            try:
                p2_y_piece = int(input())
            except:
                print('PLEASE US AN INT')
                continue
            if chess.board[p2_x_piece][p2_y_piece] != None and chess.board[p2_x_piece][p2_y_piece].colour == 'B':
                available_moves = chess.board[p2_x_piece][p2_y_piece].all_moves(chess.board)
                print(available_moves)                                
                print('Please enter X location of where to move')
                try:
                    p2_x_move = int(input())
                except:
                    print('PLEASE USE AN INT')
                    continue
                print('Please enter Y location of where to move')
                try:
                    p2_y_move = int(input())
                except:
                    print('PLEASE USE AN INT')
                    continue    
                if chess.board[p2_x_piece][p2_y_piece].move(p2_x_move, p2_y_move, chess.board) == False:
                    print('Invalid move try again')
                    chess.pprint()
                else:
                    chess.add_move()
                    if chess.board[p2_x_move][p2_y_move].check(chess.board):
                        print('P1 King is in check')                    
                    p1_turn = True
                    p2_turn = False               
               
        chess.pprint()  
    print('game over')
        
    
        
        
    
    
    
    
               
            
        
    
    
        

    

                
