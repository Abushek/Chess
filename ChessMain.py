#GameState File
import pygame as p
from Engine import ChessEngine
width=height=512
dimension=8
sqr_size=height//dimension
images={}

def loadImages():
    pieces=['wP','wR','wN','wB','wQ','wK','bP','bB','bN','bR','bQ','bK']
    for piece in pieces:
        images[piece]=p.transform.scale(p.image.load("Pieces/"+piece+".png"),(sqr_size,sqr_size))
#Main Driver
def main():
    p.init()
    screen=p.display.set_mode((width,height))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngine.GameState()
    print(gs.board)
main()