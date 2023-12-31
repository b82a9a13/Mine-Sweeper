# 9 = Mine
# 0 = Empty
# 1-8 = Number of adject mines
#Import dependancies
import tkinter as tk
import math
from random import randint
from tkinter import messagebox
from tkinter import Label
from tkinter import filedialog
from PIL import Image, ImageTk

#Define required root variable and size variables
root = tk.Tk()
mines = 20
grid = 20
winHeight = 600
winWidth = 800
height = 600
width = 600
secheight = height/grid
secwidth = width/grid
scoreInt = 0
highScoreInt = 0

#Set the application title and size. Disable resizing
root.title("Mine Sweeper")
root.geometry(f"{winWidth}x{winHeight}")
root.resizable(False,False)

#Main Menu
#Define start button, exit button and upload button, then place them
startBtn = tk.Button(root, text='Start Game', command=lambda:start_game(), height=2, width=11)
uploadBtn = tk.Button(root, text='Upload Images', command=lambda:upload_images(), height=2, width=11)
exitBtn = tk.Button(root, text='Exit', command=lambda:exit_program(), height=2, width=11)
def create_menu():
    startBtn.place(x=(winWidth/2)-40,y=(winHeight/2)-100)
    uploadBtn.place(x=(winWidth/2)-40, y=(winHeight/2)-50)
    exitBtn.place(x=(winWidth/2)-40, y=(winHeight/2))
create_menu()

#Game Menu
#Define canvas and button varaibles
canvas = tk.Canvas(root, width=width, height=height, bg="green")
endBtn = tk.Button(root, text='End Game', command=lambda:end_game(), height=2, width=10)
restartBtn = tk.Button(root, text='Restart Game', command=lambda:restart_game(), height=2, width=10)
#Define gmae labels
highScore = Label(root, text='High Score: '+str(highScoreInt))
score = Label(root, text='Score: '+str(scoreInt))
#Define values array which will contain the game data
gameStat = False
values = []
squares = []
for x in range(grid):
    tmp = []
    for y in range(grid):
        tmp.append(0)
    values.append(tmp)

#Upload Menu
#Define the heading text
uploadText = Label(root, text='Select a image for each number or empty square or mine')
#Define the buttons
numBtns = [
    [
        tk.Button(root, text='1', command=lambda:open_image(1)),
        tk.Button(root, text='2', command=lambda:open_image(2)),
        tk.Button(root, text='3', command=lambda:open_image(3)),
        tk.Button(root, text='4', command=lambda:open_image(4))
    ],
    [
        tk.Button(root, text='5', command=lambda:open_image(5)),
        tk.Button(root, text='6', command=lambda:open_image(6)),
        tk.Button(root, text='7', command=lambda:open_image(7)),
        tk.Button(root, text='8', command=lambda:open_image(8))
    ]
]
txtBtns = [
    tk.Button(root, text='Empty Square', command=lambda:open_image(0)),
    tk.Button(root, text='Mine', command=lambda:open_image(9))
]
#Define the back button
backBtn = tk.Button(root, text='Go Back', command=lambda:upload_back())
#Array is used to store the images
imgs = [None, None, None, None, None, None, None, None, None, None]
#Array is used to store the labels
labels = [None, None, None, None, None, None, None, None, None, None]
#Varaible used to display a image error message
uploadError = Label(root, text='Invalid image size, it must be 100px by 100px', fg='red')

#Function is called to close the program
def exit_program():
    root.destroy()

#Function is called to remove main menu buttons
def exit_menu():
    startBtn.place_forget()
    uploadBtn.place_forget()
    exitBtn.place_forget()

#Function is called to end the game and return to the main menu
def end_game():
    canvas.pack_forget()
    canvas.delete('all')
    endBtn.place_forget()
    restartBtn.place_forget()
    highScore.place_forget()
    score.place_forget()
    create_menu()

#Function is called to start the game
def start_game():
    global values
    global squares
    global gameStat
    global scoreInt
    #Set game varaibles to the default values
    gameStat = True
    exit_menu()
    scoreInt = 0
    score.config(text='Score: '+str(scoreInt))
    values = []
    squares = []
    for x in range(grid):
        tmp = []
        for y in range(grid):
            tmp.append(0)
        values.append(tmp)
    #Draw defualt canvas 
    def draw_canvas():
        global canvas
        fill = "lightgrey"
        for x in range(grid):
            canvas.create_line(secwidth*x, height, secwidth*x, 0, fill=fill)
            canvas.create_line(0, secheight*x, width, secheight*x, fill=fill)
    draw_canvas()

    #add mines and values to array
    for x in range(mines):
        #Add a mine to a empty space
        yy = randint(0, grid-1)
        xx = randint(0, grid-1)
        while values[xx][yy] == 9:
            yy = randint(0, grid-1)
            xx = randint(0, grid-1)
        values[xx][yy] = 9
    
    #Loop through values array to add the values
    for xx in range(grid):
        for yy in range(grid):
            if values[xx][yy] == 9:
                #Add 1 to a adjacent square that is adject to the mine
                if xx != 0 and xx != grid-1 and yy != 0 and yy != grid-1:
                    values[xx-1][yy] = values[xx-1][yy] + 1 if values[xx-1][yy] != 9 else 9
                    values[xx+1][yy] = values[xx+1][yy] + 1 if values[xx+1][yy] != 9 else 9
                    values[xx][yy+1] = values[xx][yy+1] + 1 if values[xx][yy+1] != 9 else 9
                    values[xx][yy-1] = values[xx][yy-1] + 1 if values[xx][yy-1] != 9 else 9
                    values[xx-1][yy-1] = values[xx-1][yy-1] + 1 if values[xx-1][yy-1] != 9 else 9
                    values[xx-1][yy+1] = values[xx-1][yy+1] + 1 if values[xx-1][yy+1] != 9 else 9
                    values[xx+1][yy-1] = values[xx+1][yy-1] + 1 if values[xx+1][yy-1] != 9 else 9
                    values[xx+1][yy+1] = values[xx+1][yy+1] + 1 if values[xx+1][yy+1] != 9 else 9
                elif xx == 0 and yy > 0 and yy < grid-1:
                    values[xx][yy+1] = values[xx][yy+1] + 1 if values[xx][yy+1] != 9 else 9
                    values[xx][yy-1] = values[xx][yy-1] + 1 if values[xx][yy-1] != 9 else 9
                    values[xx+1][yy] = values[xx+1][yy] + 1 if values[xx+1][yy] != 9 else 9
                    values[xx+1][yy-1] = values[xx+1][yy-1] + 1 if values[xx+1][yy-1] != 9 else 9
                    values[xx+1][yy+1] = values[xx+1][yy+1] + 1 if values[xx+1][yy+1] != 9 else 9
                elif xx > 0 and xx < grid-1 and yy == 0:
                    values[xx+1][yy] = values[xx+1][yy] + 1 if values[xx+1][yy] != 9 else 9
                    values[xx-1][yy] = values[xx-1][yy] + 1 if values[xx-1][yy] != 9 else 9
                    values[xx][yy+1] = values[xx][yy+1] + 1 if values[xx][yy+1] != 9 else 9
                    values[xx+1][yy+1] = values[xx+1][yy+1] + 1 if values[xx+1][yy+1] != 9 else 9
                    values[xx-1][yy-1] = values[xx-1][yy-1] + 1 if values[xx-1][yy-1] != 9 else 9
                elif xx > 0 and xx < grid-1 and yy == grid-1:
                    values[xx][yy-1] = values[xx][yy-1] + 1 if values[xx][yy-1] != 9 else 9
                    values[xx+1][yy] = values[xx+1][yy] + 1 if values[xx+1][yy] != 9 else 9
                    values[xx-1][yy] = values[xx-1][yy] + 1 if values[xx-1][yy] != 9 else 9
                    values[xx+1][yy-1] = values[xx+1][yy-1] + 1 if values[xx+1][yy-1] != 9 else 9
                    values[xx-1][yy-1] = values[xx-1][yy-1] + 1 if values[xx-1][yy-1] != 9 else 9
                elif xx == grid-1 and yy > 0 and yy < grid-1:
                    values[xx-1][yy] = values[xx-1][yy] + 1 if values[xx-1][yy] != 9 else 9
                    values[xx][yy+1] = values[xx][yy+1] + 1 if values[xx][yy+1] != 9 else 9
                    values[xx][yy-1] = values[xx][yy-1] + 1 if values[xx][yy-1] != 9 else 9
                    values[xx-1][yy+1] = values[xx-1][yy+1] + 1 if values[xx-1][yy+1] != 9 else 9
                    values[xx-1][yy-1] = values[xx-1][yy-1] + 1 if values[xx-1][yy-1] != 9 else 9
                elif xx == grid-1 and yy == grid-1:
                    values[xx][yy-1] = values[xx][yy-1] + 1 if values[xx][yy-1] != 9 else 9
                    values[xx-1][yy] = values[xx-1][yy] + 1 if values[xx-1][yy] != 9 else 9
                    values[xx-1][yy-1] = values[xx-1][yy-1] + 1 if values[xx-1][yy-1] != 9 else 9
                elif xx == 0 and yy == grid-1:
                    values[xx][yy-1] = values[xx][yy-1] + 1 if values[xx][yy-1] != 9 else 9
                    values[xx+1][yy] = values[xx+1][yy] + 1 if values[xx+1][yy] != 9 else 9
                    values[xx+1][yy-1] = values[xx+1][yy-1] + 1 if values[xx+1][yy-1] != 9 else 9
                elif xx == grid-1 and yy == 0:
                    values[xx][yy+1] = values[xx][yy+1] + 1 if values[xx][yy+1] != 9 else 9
                    values[xx-1][yy] = values[xx-1][yy] + 1 if values[xx-1][yy] != 9 else 9
                    values[xx-1][yy+1] = values[xx-1][yy+1] + 1 if values[xx-1][yy+1] != 9 else 9
                elif xx == 0 and yy == 0:
                    values[xx+1][yy] = values[xx+1][yy] + 1 if values[xx+1][yy] != 9 else 9
                    values[xx][yy+1] = values[xx][yy+1] + 1 if values[xx][yy+1] != 9 else 9
                    values[xx+1][yy+1] = values[xx+1][yy+1] + 1 if values[xx+1][yy+1] != 9 else 9
    
    #Draw mines and values, and add a square to the squares array
    for x in range(grid):
        tmp = []
        for y in range(grid):
            xPos = secwidth/2
            yPos = secheight/2
            if x == 0 and y != 0:
                yPos = (secheight*y)+(secheight/2)
            elif y == 0 and x != 0:
                xPos = (secwidth*x)+(secwidth/2)
            elif x != 0 and y != 0:
                xPos = (secwidth*x)+(secwidth/2)
                yPos = (secwidth*y)+(secwidth/2)
            if has_image(values[x][y]):
                canvas.create_image(xPos, yPos, image=imgs[values[x][y]])
            elif values[x][y] != 0:
                if values[x][y] == 9:
                    canvas.create_text(xPos, yPos, text='M', fill='red', font=('Arial 10 bold'))
                else:
                    colour = 'blue'
                    if values[x][y] == 1:
                        colour = 'purple'
                    if values[x][y] == 2:
                        colour = 'yellow'
                    if values[x][y] == 3:
                        colour = 'orange'
                    canvas.create_text(xPos, yPos, text=values[x][y], fill=colour, font=('Arial 10 bold'))
            tmp.append(canvas.create_rectangle(xPos-(secwidth/2), yPos-(secheight/2), xPos+(secwidth/2), yPos+(secheight/2), fill='darkgreen'))
        squares.append(tmp)
    #Draw buttons
    xPos = width+50
    restartBtn.place(x=xPos, y=500)
    endBtn.place(x=xPos, y=550)
    #Draw score text
    highScore.place(x=xPos, y=0)
    score.place(x=xPos, y=25)
    #Pack canvas
    canvas.pack(side='left')
    #Function is called when the canvas is clicked
    def on_canvas_click(event):
        global scoreInt
        global highScoreInt
        global gameStat
        #Get the x and y postion on the click
        x = event.x
        y = event.y
        #Set game stat to fals if a bomb is clicked
        xPos = math.floor(x/secwidth)
        yPos = math.floor(y/secheight)
        current = values[xPos][yPos]
        if current == 9:
            canvas.delete(squares[xPos][yPos])
            gameStat = False
        #Output game over if game stat is false
        if gameStat == False:
            messagebox.showinfo('Dialog Box', 'Game Over!')
        else:
            #Check if the square click is present on the canvas
            if canvas.find_withtag(squares[xPos][yPos]):
                canvas.delete(squares[xPos][yPos])
                scoreInt += 1
                if current == 0:
                    #runs when a empty square is clicked, clears surrounding squares if they aren't a mine
                    if xPos != 0 and xPos != grid-1 and yPos != 0 and yPos != grid-1:
                        if values[xPos+1][yPos] != 9 and canvas.find_withtag(squares[xPos+1][yPos]):
                            canvas.delete(squares[xPos+1][yPos])
                            scoreInt += 1
                        if values[xPos-1][yPos] != 9 and canvas.find_withtag(squares[xPos-1][yPos]):
                            canvas.delete(squares[xPos-1][yPos])
                            scoreInt += 1
                        if values[xPos][yPos+1] != 9 and canvas.find_withtag(squares[xPos][yPos+1]):
                            canvas.delete(squares[xPos][yPos+1])
                            scoreInt += 1
                        if values[xPos][yPos-1] != 9 and canvas.find_withtag(squares[xPos][yPos-1]):
                            canvas.delete(squares[xPos][yPos-1])
                            scoreInt += 1
                        if values[xPos+1][yPos-1] != 9 and canvas.find_withtag(squares[xPos+1][yPos-1]):
                            canvas.delete(squares[xPos+1][yPos-1])
                            scoreInt += 1
                        if values[xPos+1][yPos+1] != 9 and canvas.find_withtag(squares[xPos+1][yPos+1]):
                            canvas.delete(squares[xPos+1][yPos+1])
                            scoreInt += 1
                        if values[xPos-1][yPos-1] != 9 and canvas.find_withtag(squares[xPos-1][yPos-1]):
                            canvas.delete(squares[xPos-1][yPos-1])
                            scoreInt += 1
                        if values[xPos-1][yPos+1] != 9 and canvas.find_withtag(squares[xPos-1][yPos+1]):
                            canvas.delete(squares[xPos-1][yPos+1])
                            scoreInt += 1
                    elif xPos != 0 and xPos != grid-1 and yPos == 0:
                        if values[xPos][yPos+1] != 9 and canvas.find_withtag(squares[xPos][yPos+1]):
                            canvas.delete(squares[xPos][yPos+1])
                            scoreInt += 1
                        if values[xPos+1][yPos] != 9 and canvas.find_withtag(squares[xPos+1][yPos]):
                            canvas.delete(squares[xPos+1][yPos])
                            scoreInt += 1
                        if values[xPos+1][yPos+1] != 9 and canvas.find_withtag(squares[xPos+1][yPos+1]):
                            canvas.delete(squares[xPos+1][yPos+1])
                            scoreInt += 1
                        if values[xPos-1][yPos] != 9 and canvas.find_withtag(squares[xPos-1][yPos]):
                            canvas.delete(squares[xPos-1][yPos])
                            scoreInt += 1
                        if values[xPos-1][yPos+1] != 9 and canvas.find_withtag(squares[xPos-1][yPos+1]):
                            canvas.delete(squares[xPos-1][yPos+1])
                            scoreInt += 1
                    elif xPos != 0 and xPos != grid-1 and yPos == grid-1:
                        if values[xPos][yPos-1] != 9 and canvas.find_withtag(squares[xPos][yPos-1]):
                            canvas.delete(squares[xPos][yPos-1])
                            scoreInt += 1
                        if values[xPos-1][yPos] != 9 and canvas.find_withtag(squares[xPos-1][yPos]):
                            canvas.delete(squares[xPos-1][yPos])
                            scoreInt += 1
                        if values[xPos-1][yPos-1] != 9 and canvas.find_withtag(squares[xPos-1][yPos-1]):
                            canvas.delete(squares[xPos-1][yPos-1])
                            scoreInt += 1
                        if values[xPos+1][yPos] != 9 and canvas.find_withtag(squares[xPos+1][yPos]):
                            canvas.delete(squares[xPos+1][yPos])
                            scoreInt += 1
                        if values[xPos+1][yPos-1] != 9 and canvas.find_withtag(squares[xPos+1][yPos-1]):
                            canvas.delete(squares[xPos+1][yPos-1])
                            scoreInt += 1
                    elif xPos == 0 and yPos != 0 and yPos != grid-1:
                        if values[xPos+1][yPos] != 9 and canvas.find_withtag(squares[xPos+1][yPos]):
                            canvas.delete(squares[xPos+1][yPos])
                            scoreInt += 1
                        if values[xPos][yPos-1] != 9 and canvas.find_withtag(squares[xPos][yPos-1]):
                            canvas.delete(squares[xPos][yPos-1])
                            scoreInt += 1
                        if values[xPos][yPos+1] != 9 and canvas.find_withtag(squares[xPos][yPos+1]):
                            canvas.delete(squares[xPos][yPos+1])
                            scoreInt += 1
                        if values[xPos+1][yPos-1] != 9 and canvas.find_withtag(squares[xPos+1][yPos-1]):
                            canvas.delete(squares[xPos+1][yPos-1])
                            scoreInt += 1
                        if values[xPos+1][yPos+1] != 9 and canvas.find_withtag(squares[xPos+1][yPos+1]):
                            canvas.delete(squares[xPos+1][yPos+1])
                            scoreInt += 1
                    elif xPos == grid-1 and yPos != 0 and yPos != grid-1:
                        if values[xPos-1][yPos] != 9 and canvas.find_withtag(squares[xPos-1][yPos]):
                            canvas.delete(squares[xPos-1][yPos])
                            scoreInt += 1
                        if values[xPos][yPos+1] != 9 and canvas.find_withtag(squares[xPos][yPos+1]):
                            canvas.delete(squares[xPos][yPos+1])
                            scoreInt += 1
                        if values[xPos][yPos-1] != 9 and canvas.find_withtag(squares[xPos][yPos-1]):
                            canvas.delete(squares[xPos][yPos-1])
                            scoreInt += 1
                        if values[xPos-1][yPos+1] != 9 and canvas.find_withtag(squares[xPos-1][yPos+1]):
                            canvas.delete(squares[xPos-1][yPos+1])
                            scoreInt += 1
                        if values[xPos-1][yPos-1] != 9 and canvas.find_withtag(squares[xPos-1][yPos-1]):
                            canvas.delete(squares[xPos-1][yPos-1])
                            scoreInt += 1
                    elif xPos == 0 and yPos == 0:
                        if values[xPos][yPos+1] != 9 and canvas.find_withtag(squares[xPos][yPos+1]):
                            canvas.delete(squares[xPos][yPos+1])
                            scoreInt += 1
                        if values[xPos+1][yPos] != 9 and canvas.find_withtag(squares[xPos+1][yPos]):
                            canvas.delete(squares[xPos+1][yPos])
                            scoreInt += 1
                        if values[xPos+1][yPos+1] != 9 and canvas.find_withtag(squares[xPos+1][yPos+1]):
                            canvas.delete(squares[xPos+1][yPos+1])
                            scoreInt += 1
                    elif xPos == grid-1 and yPos == grid-1:
                        if values[xPos][yPos-1] != 9 and canvas.find_withtag(squares[xPos][yPos-1]):
                            canvas.delete(squares[xPos][yPos-1])
                            scoreInt += 1
                        if values[xPos-1][yPos] != 9 and canvas.find_withtag(squares[xPos-1][yPos]):
                            canvas.delete(squares[xPos-1][yPos])
                            scoreInt += 1
                        if values[xPos-1][yPos-1] != 9 and canvas.find_withtag(squares[xPos-1][yPos-1]):
                            canvas.delete(squares[xPos-1][yPos-1])
                            scoreInt += 1
                    elif xPos == 0 and yPos == grid-1:
                        if values[xPos][yPos-1] != 9 and canvas.find_withtag(squares[xPos][yPos-1]):
                            canvas.delete(squares[xPos][yPos-1])
                            scoreInt += 1
                        if values[xPos+1][yPos] != 9 and canvas.find_withtag(squares[xPos+1][yPos]):
                            canvas.delete(squares[xPos+1][yPos])
                            scoreInt += 1
                        if values[xPos+1][yPos-1] != 9 and canvas.find_withtag(squares[xPos+1][yPos-1]):
                            canvas.delete(squares[xPos+1][yPos-1])
                            scoreInt += 1
                    elif xPos == grid-1 and yPos == 0:
                        if values[xPos][yPos+1] != 9 and canvas.find_withtag(squares[xPos][yPos+1]):
                            canvas.delete(squares[xPos][yPos+1])
                            scoreInt += 1
                        if values[xPos-1][yPos] != 9 and canvas.find_withtag(squares[xPos-1][yPos]):
                            canvas.delete(squares[xPos-1][yPos])
                            scoreInt += 1
                        if values[xPos-1][yPos+1] != 9 and canvas.find_withtag(squares[xPos-1][yPos+1]):
                            canvas.delete(squares[xPos-1][yPos+1])
                            scoreInt += 1
        #Check if the high score is less than the current score, if so the high score label
        if scoreInt > highScoreInt:
            highScoreInt = scoreInt
            highScore.config(text='High Score: '+str(highScoreInt))
        #Update the score label
        score.config(text='Score: '+str(scoreInt))
    #Bind a click event        
    canvas.bind("<Button-1>", on_canvas_click)

#Function is called to restart the game
def restart_game():
    global gameStat
    global scoreInt
    gameStat = True
    scoreInt = 0
    score.config(text='Score: '+str(scoreInt))
    canvas.pack_forget()
    canvas.delete('all')
    start_game()

#Function is called to open the upload images page
def upload_images():
    exit_menu()
    uploadText.pack(side='top')
    backBtn.pack(side='bottom')
    xp = 0
    for x in numBtns:
        yp = 0
        for y in x:
            y.place(x=((winWidth/2)-40)+(20*yp),y=75+(xp*30))
            yp += 1
        xp += 1
    xp = 0
    for x in txtBtns:
        x.place(x=((winWidth/2)-60)+(85*xp),y=135)
        xp += 1
    pos = 0
    for x in labels:
        if x != None:
            xPos = winWidth/2 - 300
            yPos = winHeight/3
            if pos > 0 and pos < 9:
                if pos > 4:
                    xPos += 100 * (pos-4)
                    yPos += 105
                else:
                    xPos += 100 * pos
            else:
                yPos += 210
                xPos = winWidth/2 - 100
                if pos == 9:
                    xPos += 100
            labels[pos].place(x=xPos, y=yPos)
        pos += 1

#Function is called to return to the main menu from the uploag images page
def upload_back():
    uploadText.pack_forget()
    backBtn.pack_forget()
    for x in numBtns:
        for y in x:
            y.place_forget()
    for x in txtBtns:
        x.place_forget()
    for x in labels:
        if x != None:
            x.place_forget()
    create_menu()

#Function is called when a image button is clicked
def open_image(pos):
    global imgs
    uploadError.pack_forget()
    #Get file and define the allowed file types
    filePath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.ppm *.pgm")])
    if filePath:
        with open(filePath, "rb") as image_file:
            #Create a variable with the image
            im = Image.open(filePath)
            #Check the size of the image is 100x100
            width, height = im.size
            if width != 100 and height != 100:
                #Output error message
                uploadError.pack(side="top")
            else:
                #Define the x and y position dependant on the position provided
                xPos = winWidth/2 - 300
                yPos = winHeight/3
                if pos > 0 and pos < 9:
                    if pos > 4:
                        xPos += 100 * (pos-4)
                        yPos += 105
                    else:
                        xPos += 100 * pos
                else:
                    yPos += 210
                    xPos = winWidth/2 - 100
                    if pos == 9:
                        xPos += 100
                #Create image variable within an array
                im = im.resize((int(secwidth)-1, int(secheight)-1))
                imgs[pos] = ImageTk.PhotoImage(im)
                if labels[pos] != None:
                    labels[pos].place_forget()
                #Add image to label and pack to the UI
                labels[pos] = Label(root, image=imgs[pos])
                labels[pos].place(x=xPos, y=yPos)

#Function is called to check if a image exists for a specific position in an array
def has_image(pos):
    return imgs[pos] is not None

root.mainloop()