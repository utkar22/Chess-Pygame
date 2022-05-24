import pygame
import time
import copy
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()

display_width=640
display_height=640

scale=int(640/8)

surface = pygame.Surface((display_width+200,display_height), pygame.SRCALPHA)

gameDisplay=pygame.display.set_mode((display_width+200,display_height))

#Colors

black=(0,0,0)
white=(255,255,255)

board_dark=(118,150,86)
board_light=(238,238,210)

highlighted_light=(246,246,130)
highlighted_dark=(186,202,68)

light_beige=(169,149,123)
dark_beige=(207,185,151)

light_red=(184, 15, 10)
dark_red=(139, 0, 0)

light_red2=(204, 161, 161)
dark_red2=(115, 52, 52)

text_color=(0, 128, 128)

trans_black=(0, 0, 0, 100)

font1=resource_path("data/freesansbold.ttf")

pawn_shadow=("pawn shadow white","pawn shadow black")


class piece(object):
    def __init__(self,team,role,row,column):
        self.team=team
        self.role=role

        
        self.row=row
        self.column=column
        self.position=(self.row,self.column)
        
        self.times_moved=0

        if self.team=="white":
            self.color=white
        else:
            self.color=black

        self.times_moved=0

    def draw(self):
        if self.role=="Knight":
            self.code="N"
        else:
            self.code=self.role[0]
            
        pygame.draw.circle(gameDisplay, self.color, (self.column*scale+40, self.row*scale+40), 30)
        message_display(self.code,font1,25,self.column*scale+40, self.row*scale+40)

    def available(self, board, unavailable=[]):
        available_boxes=[]
        board=copy.deepcopy(board)

        if self.role=="Pawn":
            if self.team=="white":
                if board[self.row-1][self.column]==None:
                    available_boxes.append((self.row-1,self.column))

                    if self.row==6 and board[self.row-2][self.column]==None:
                        available_boxes.append((self.row-2,self.column))

                if (self.column>0 and (board[self.row-1][self.column-1] in pawn_shadow or
                    (board[self.row-1][self.column-1]!=None and board[self.row-1][self.column-1].team!=self.team))):
                    available_boxes.append((self.row-1,self.column-1))
                if (self.column<7 and (board[self.row-1][self.column+1] in pawn_shadow or
                    (board[self.row-1][self.column+1]!=None and board[self.row-1][self.column+1].team!=self.team))):
                    available_boxes.append((self.row-1,self.column+1))

            else:
                if board[self.row+1][self.column]==None:
                    available_boxes.append((self.row+1,self.column))

                    if self.row==1 and board[self.row+2][self.column]==None:
                        available_boxes.append((self.row+2,self.column))

                if (self.column>0 and (board[self.row+1][self.column-1] in pawn_shadow or
                    (board[self.row+1][self.column-1]!=None and board[self.row+1][self.column-1].team!=self.team))):
                    available_boxes.append((self.row+1,self.column-1))
                if (self.column<7 and (board[self.row+1][self.column+1] in pawn_shadow or
                    (board[self.row+1][self.column+1]!=None and board[self.row+1][self.column+1].team!=self.team))):
                    available_boxes.append((self.row+1,self.column+1))

        else:
            for a in range(0,8):
                for b in range(0,8):
                    if board[a][b] in pawn_shadow:
                        board[a][b]=None


        if self.role=="Knight":
            if self.row>1 and self.column<7 and (board[self.row-2][self.column+1]==None or board[self.row-2][self.column+1].team!=self.team):
                available_boxes.append((self.row-2,self.column+1))
            if self.row>0 and self.column<6 and (board[self.row-1][self.column+2]==None or board[self.row-1][self.column+2].team!=self.team):
                available_boxes.append((self.row-1,self.column+2))
            if self.row<7 and self.column<6 and (board[self.row+1][self.column+2]==None or board[self.row+1][self.column+2].team!=self.team):
                available_boxes.append((self.row+1,self.column+2))
            if self.row<6 and self.column<7 and (board[self.row+2][self.column+1]==None or board[self.row+2][self.column+1].team!=self.team):
                available_boxes.append((self.row+2,self.column+1))

            if self.row>1 and self.column>0 and (board[self.row-2][self.column-1]==None or board[self.row-2][self.column-1].team!=self.team):
                available_boxes.append((self.row-2,self.column-1))
            if self.row>0 and self.column>1 and (board[self.row-1][self.column-2]==None or board[self.row-1][self.column-2].team!=self.team):
                available_boxes.append((self.row-1,self.column-2))
            if self.row<7 and self.column>1 and (board[self.row+1][self.column-2]==None or board[self.row+1][self.column-2].team!=self.team):
                available_boxes.append((self.row+1,self.column-2))
            if self.row<6 and self.column>0 and (board[self.row+2][self.column-1]==None or board[self.row+2][self.column-1].team!=self.team):
                available_boxes.append((self.row+2,self.column-1))


        if self.role=="Rook" or self.role=="Queen":
            for a in range(1,8):
                if self.row+a>7:
                    break
                p=board[self.row+a][self.column]
                if p==None:
                    available_boxes.append((self.row+a,self.column))
                elif p.team!=self.team:
                    available_boxes.append((self.row+a,self.column))
                    break
                else:
                    break

            for a in range(1,8):
                if self.row-a<0:
                    break
                p=board[self.row-a][self.column]
                if p==None:
                    available_boxes.append((self.row-a,self.column))
                elif p.team!=self.team:
                    available_boxes.append((self.row-a,self.column))
                    break
                else:
                    break

            for a in range(1,8):
                if self.column+a>7:
                    break
                p=board[self.row][self.column+a]
                if p==None:
                    available_boxes.append((self.row,self.column+a))
                elif p.team!=self.team:
                    available_boxes.append((self.row,self.column+a))
                    break
                else:
                    break

            for a in range(1,8):
                if self.column-a<0:
                    break
                p=board[self.row][self.column-a]
                if p==None:
                    available_boxes.append((self.row,self.column-a))
                elif p.team!=self.team:
                    available_boxes.append((self.row,self.column-a))
                    break
                else:
                    break


        if self.role=="Bishop" or self.role=="Queen":
            for a in range(1,8):
                if self.row+a>7 or self.column+a>7:
                    break
                p=board[self.row+a][self.column+a]
                if p==None:
                    available_boxes.append((self.row+a,self.column+a))
                elif p.team!=self.team:
                    available_boxes.append((self.row+a,self.column+a))
                    break
                else:
                    break

            for a in range(1,8):
                if self.row+a>7 or self.column-a<0:
                    break
                p=board[self.row+a][self.column-a]
                if p==None:
                    available_boxes.append((self.row+a,self.column-a))
                elif p.team!=self.team:
                    available_boxes.append((self.row+a,self.column-a))
                    break
                else:
                    break

            for a in range(1,8):
                if self.row-a<0 or self.column-a<0:
                    break
                p=board[self.row-a][self.column-a]
                if p==None:
                    available_boxes.append((self.row-a,self.column-a))
                elif p.team!=self.team:
                    available_boxes.append((self.row-a,self.column-a))
                    break
                else:
                    break

            for a in range(1,8):
                if self.row-a<0 or self.column+a>7:
                    break
                p=board[self.row-a][self.column+a]
                if p==None:
                    available_boxes.append((self.row-a,self.column+a))
                elif p.team!=self.team:
                    available_boxes.append((self.row-a,self.column+a))
                    break
                else:
                    break


        if self.role=="King":
            if (self.row>0 and ((self.row-1,self.column) not in unavailable) and 
            (board[self.row-1][self.column]==None or board[self.row-1][self.column].team!=self.team)):
                available_boxes.append((self.row-1,self.column))
             
            if (self.row<7 and ((self.row+1,self.column) not in unavailable) and
             (board[self.row+1][self.column]==None or board[self.row+1][self.column].team!=self.team)):
                available_boxes.append((self.row+1,self.column))
              
            if (self.column>0 and ((self.row,self.column-1) not in unavailable) and 
              (board[self.row][self.column-1]==None or board[self.row][self.column-1].team!=self.team)):
                available_boxes.append((self.row,self.column-1))

                if ((self.row,self.column) not in unavailable and self.times_moved==0 and
                    (self.row,self.column-2) not in unavailable and board[self.row][self.column-1]==None
                    and board[self.row][self.column-2]==None and board[self.row][self.column-3]==None
                    and board[self.row][self.column-4]!=None and board[self.row][self.column-4].times_moved==0):
                    available_boxes.append((self.row,self.column-2))
               
            if (self.column<7 and ((self.row,self.column+1) not in unavailable) and 
               (board[self.row][self.column+1]==None or board[self.row][self.column+1].team!=self.team)):
                available_boxes.append((self.row,self.column+1))

                if ((self.row,self.column) not in unavailable and self.times_moved==0
                    and ((self.row,self.column+2) not in unavailable) and board[self.row][self.column+2]==None
                    and board[self.row][self.column+3]!=None and board[self.row][self.column+3].times_moved==0):
                        available_boxes.append((self.row,self.column+2))

            if (self.row>0 and self.column>0 and ((self.row-1,self.column-1) not in unavailable) and 
            (board[self.row-1][self.column-1]==None or board[self.row-1][self.column-1].team!=self.team)):
                available_boxes.append((self.row-1,self.column-1))

            if (self.row<7 and self.column<7 and ((self.row+1,self.column+1) not in unavailable) and 
            (board[self.row+1][self.column+1]==None or board[self.row+1][self.column+1].team!=self.team)):
                available_boxes.append((self.row+1,self.column+1))

            if (self.row<7 and self.column>0 and ((self.row+1,self.column-1) not in unavailable) and 
            (board[self.row+1][self.column-1]==None or board[self.row+1][self.column-1].team!=self.team)):
                available_boxes.append((self.row+1,self.column-1))

            if (self.row>0 and self.column<7 and ((self.row-1,self.column+1) not in unavailable) and 
            (board[self.row-1][self.column+1]==None or board[self.row-1][self.column+1].team!=self.team)):
                available_boxes.append((self.row-1,self.column+1))
            

        
                
            
            

        return (available_boxes)

    def move(self, board, where, actual=True):

        row,column=where

        if board[row][column]!=None or self.role=="Pawn":
            moves_counter_reset=True
        else:
            moves_counter_reset=False
           


        if self.role=="Pawn":
            if abs(self.row-row)==2:
                if self.team=="white":
                    board[self.row-1][self.column]="pawn shadow white"
                else:
                    board[self.row+1][self.column]="pawn shadow black"

            if board[row][column] in pawn_shadow:
                if self.team=="white":
                    board[row+1][column]=None
                else:
                    board[row-1][column]=None

        elif self.role=="King":
            if column-self.column==2:
                board,bruh=board[self.row][self.column+3].move(board, (self.row,self.column+1), actual)
            elif self.column-column==2:
                board,bruh=board[self.row][self.column-4].move(board, (self.row,self.column-1), actual)


        board[row][column]=board[self.row][self.column]
        board[self.row][self.column]=None
        
            


        if actual:
            self.position=where
            self.row,self.column=self.position

            self.times_moved+=1

            
            

        return (board, moves_counter_reset)

    def promote(self, board):
        new_role=promotion()
        self.role=new_role
                
                
        
        
        
        



def text_objects(text,font,color):
    textSurface=font.render(text, True, color)
    return (textSurface, textSurface.get_rect())

def message_display(text,font,size,x,y,color=text_color):
    largeText=pygame.font.Font(font,size)
    TextSurf,TextRect=text_objects(text, largeText, color)
    TextRect.center=(x,y)
    gameDisplay.blit(TextSurf,TextRect)


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()

    if x<mouse[0]<x+w and y<mouse[1]<y+h:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        
        if click[0]==1 and action!=None:
            if action==True:
                return(True)
            else:
                action()

    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    message_display(msg,font1,20,x+w/2,y+h/2)

    
def promotion():
    is_queen=False
    is_rook=False
    is_knight=False
    is_bishop=False

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        
        is_queen=button("Queen",70,300,100,100,light_beige,dark_beige, True)
        is_rook=button("Rook",210,300,100,100,light_beige,dark_beige, True)
        is_knight=button("Knight",350,300,100,100,light_beige,dark_beige, True)
        is_bishop=button("Bishop",490,300,100,100,light_beige,dark_beige, True)

        if is_queen:
            return("Queen")
        elif is_rook:
            return("Rook")
        elif is_knight:
            return("Knight")
        elif is_bishop:
            return("Bishop")

        pygame.display.update()


                      
def game_end(status,team=""):

    if status=="lose":
        if team=="white":
            msg="Black Wins"
        else:
            msg="White Wins"
    else:
        msg=status
        

    time.sleep(4)
    a=0

    game_end_display=True

    while game_end_display:
        a+=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                a=3000
        
        message_display(msg, font1, 100, display_width/2, display_height/2)
        pygame.display.update()

        if a>2999:
            game_end_display=False
    
    

        
                

        
        
def gameloop():
    run=True

    box_selected=()
    boxes_available=[]
    selected_piece=None

    king_position=()

    resign=False

    

    board=[ [piece("black","Rook",0,0), piece("black","Knight",0,1), piece("black","Bishop",0,2), piece("black","Queen",0,3),
             piece("black","King",0,4), piece("black","Bishop",0,5), piece("black","Knight",0,6), piece("black","Rook",0,7)]
            ,
            [piece("black","Pawn",1,0), piece("black","Pawn",1,1), piece("black","Pawn",1,2), piece("black","Pawn",1,3),
             piece("black","Pawn",1,4), piece("black","Pawn",1,5), piece("black","Pawn",1,6), piece("black","Pawn",1,7)]
            ,
            [None, None, None, None, None, None, None, None]
            ,
            [None, None, None, None, None, None, None, None]
            ,
            [None, None, None, None, None, None, None, None]
            ,
            [None, None, None, None, None, None, None, None]
            ,
            [piece("white","Pawn",6,0), piece("white","Pawn",6,1), piece("white","Pawn",6,2), piece("white","Pawn",6,3),
             piece("white","Pawn",6,4), piece("white","Pawn",6,5), piece("white","Pawn",6,6), piece("white","Pawn",6,7)]
            ,
            [piece("white","Rook",7,0), piece("white","Knight",7,1), piece("white","Bishop",7,2), piece("white","Queen",7,3),
             piece("white","King",7,4), piece("white","Bishop",7,5), piece("white","Knight",7,6), piece("white","Rook",7,7)]

            ]

    team="black"

    click_oldtime=0

    mating_pieces=True
    moves_counter=0

    just_moved=True
             

    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

        if just_moved:
            if team=="white":
                team="black"
            else:
                team="white"

            white_pieces={"King":0, "Queen":0, "Rook":0, "Knight":0, "Bishop":0, "Pawn":0}
            black_pieces={"King":0, "Queen":0, "Rook":0, "Knight":0, "Bishop":0, "Pawn":0}

            cannot_move=[]


            for a in range(0,8):
                for b in range(0,8):
                    board_piece=board[a][b]
                    if board_piece=="pawn shadow "+team:
                        board[a][b]=None
                    elif board_piece!=None and board_piece not in pawn_shadow:
                        if board_piece.role=="Pawn":
                            if (board_piece.team=="white" and board_piece.row==0) or (board_piece.team=="black" and board_piece.row==7):
                                board_piece.promote(board)

                        elif board_piece.role=="King" and board_piece.team==team:
                            king_position=(a,b)




                        if board_piece.team!=team:
                            if board_piece.role=="Pawn":
                                if board_piece.team=="white":
                                    cannot_move.extend([(board_piece.row-1,board_piece.column-1),(board_piece.row-1,board_piece.column+1)])
                                else:
                                    cannot_move.extend([(board_piece.row+1,board_piece.column-1),(board_piece.row+1,board_piece.column+1)])
                            else:
                                cannot_move.extend(board_piece.available(board))


                        if board_piece.team=="white":
                            white_pieces[board_piece.role]+=1
                        elif board_piece.team=="black":
                            black_pieces[board_piece.role]+=1


            is_check=False
            
            if king_position in cannot_move:
                is_check=True

            if (black_pieces["Pawn"]==0 and white_pieces["Pawn"]==0
                and black_pieces["Queen"]==0 and white_pieces["Queen"]==0
                and black_pieces["Rook"]==0 and white_pieces["Rook"]==0
                and black_pieces["Bishop"]<2 and white_pieces["Bishop"]<2
                and (black_pieces["Bishop"]+black_pieces["Knight"]<3)
                and (white_pieces["Bishop"]+white_pieces["Knight"]<3)):
                mating_pieces=False
        

            available_dictionary=dict()

            is_checkmate=True

            for a in range(0,8):
                for b in range(0,8):
                    piece_selected=board[a][b]
                    if piece_selected!=None and piece_selected not in pawn_shadow and piece_selected.team==team:
                        available_dictionary[piece_selected]=[]
                        available_boxes=piece_selected.available(board,cannot_move)
                        for c in available_boxes:
                            board_clone=copy.deepcopy(board)
                            board_clone,bruh=piece_selected.move(board_clone,c,False)

                            king_pos=king_position

                            if piece_selected.role=="King":
                                king_pos=c

                            king_cannot_move=[]
                            for d in range(0,8):
                                for e in range(0,8):
                                    piece_selected2=board_clone[d][e]
                                    if piece_selected2!=None and piece_selected2 not in pawn_shadow and piece_selected2.team!=team:
                                        if piece_selected2.role=="Pawn":
                                            if piece_selected2.team=="white":
                                                king_cannot_move.extend([(piece_selected2.row-1,piece_selected2.column-1),(piece_selected2.row-1,piece_selected2.column+1)])
                                            else:
                                                king_cannot_move.extend([(piece_selected2.row+1,piece_selected2.column-1),(piece_selected2.row+1,piece_selected2.column+1)])
                                        else:
                                            king_cannot_move.extend(piece_selected2.available(board_clone))

                            if king_pos not in king_cannot_move:
                                available_dictionary[piece_selected].append(c)
                                is_checkmate=False

                            board_clone.clear()

            is_stalemate=False

            if is_checkmate and not is_check:
                is_stalemate=True
                is_checkmate=False


        just_moved=False

        
        #Click

        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        click_newtime=pygame.time.get_ticks()


        if click[0]==1 and mouse[0]<display_width and click_newtime-click_oldtime>300:
            box_click_on=(mouse[1]//scale,mouse[0]//scale)
            if box_selected==box_click_on:
                box_selected=()
                boxes_available.clear()
                selected_piece=None
            
            elif board[mouse[1]//scale][mouse[0]//scale]!=None and board[mouse[1]//scale][mouse[0]//scale] not in pawn_shadow:
                if board[mouse[1]//scale][mouse[0]//scale].team==team:
                    box_selected=()
                    boxes_available.clear()
                    selected_piece=None
                    selected_piece=board[mouse[1]//scale][mouse[0]//scale]
                    box_selected=(selected_piece.row,selected_piece.column)
                    boxes_available=copy.deepcopy(available_dictionary[selected_piece])
                    


            if box_click_on in boxes_available:
                board,moves_counter_reset=selected_piece.move(board,box_click_on)
                box_selected=()
                boxes_available.clear()
                selected_piece=None

                if moves_counter_reset:
                    moves_counter=0
                else:
                    moves_counter+=1

                just_moved=True


                
                    
                    
            click_oldtime=click_newtime


            


            

        #Display

        gameDisplay.fill(black)

        surface.fill((0,0,0,0))

        for a in range(0,8):
            for b in range(0,8):
                if (a+b)%2==0:
                    if (a,b)==box_selected:
                        box_color=highlighted_dark
                    elif is_check and (a,b)==king_position:
                        box_color=dark_red2
                    else:
                        box_color=board_dark
                else:
                    if (a,b)==box_selected:
                        box_color=highlighted_light
                    elif is_check and (a,b)==king_position:
                        box_color=light_red2
                    else:
                        box_color=board_light


                if (a,b) in boxes_available:
                    pygame.draw.circle(surface,trans_black,(b*scale+scale//2,a*scale+scale//2),10)
                    

                pygame.draw.rect(gameDisplay, box_color, (b*scale,a*scale,scale,scale))
                

                game_piece=board[a][b]

                if game_piece!=None and game_piece not in pawn_shadow:
                    game_piece.draw()

        if is_checkmate:
            message_display("Checkmate", font1, 30, display_width+100,display_height/2)
        elif is_stalemate:
            message_display("Stalemate", font1, 30, display_width+100,display_height/2)
        else:
            message_display(team[0].capitalize()+team[1:], font1, 50, display_width+100,display_height/2)

        message_display(str(moves_counter//2), font1, 10, 815, 625)


        resign=button("Resign", 690, 135, 100, 50, dark_red, light_red, True)



        gameDisplay.blit(surface, (0,0))

        pygame.display.update()

        if is_stalemate:
            game_end("Stalemate")
            run=False
        elif (not mating_pieces) or moves_counter==100:
            game_end("Draw")
            run=False
        elif is_checkmate or resign:
            game_end("lose",team)
            run=False

    pygame.quit()

gameloop()

