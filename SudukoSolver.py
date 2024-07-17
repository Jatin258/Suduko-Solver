from tkinter import *
import sys
sys.setrecursionlimit(1000000)

root = Tk()
root.title("Sudoku Solver")
root.geometry("324x550")

label = Label(root,text="Fill in the numbers and click solve").grid(row=0,column=1,columnspan=10)

errLabel = Label(root,text="",fg="red")
errLabel.grid(row=15,column=1,columnspan=10,pady=5)

solvedLabel = Label(root,text="",fg="green")
solvedLabel.grid(row=15,column=1,columnspan=10,pady=5)

cells = {}

def ValidateNumber(P) :
    out = (P.isdigit() or P =="") and len(P) < 2 
    return out

reg = root.register(ValidateNumber)

def draw3x3Grid(row,column,bgcolor) :
    for i in range(3) :
        for j in range(3) :
            e = Entry(root , width=5 , bg=bgcolor , justify="center" , validate="key" , validatecommand=(reg,"%P"))
            e.grid(row=row+i+1,column=column+j+1,sticky="nsew",padx=1,pady=1,ipady=5)
            cells[(row+i+1,column+j+1)] = e;

def draw9x9Grid():
    color="#ADFD8D"
    for rowNo in range(1,10,3) :
        for colNo in range(0,9,3) :
            draw3x3Grid(rowNo,colNo,color)
            if(color == "#ADFD8D") :
                color = "#ffffd0"
            else :
                color = "#ADFD8D"

def clearValues() :
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11) :
        for col in range(1,10) :
            cell = cells[(row,col)]
            cell.delete(0,"end")

def getValues() :
    board = []
    errLabel.configure(text="")
    solvedLabel.configure(text="")
    for row in range(2,11) :
        rows = []
        for col in range(1,10) :
            val = cells[(row,col)].get()
            if val == "" :
                rows.append(0);
            else :
                rows.append(int(val))
        board.append(rows)
    updatevalues(board)

N = 9
def isSafe(sudoku , row , col ,num):
    for i in range(9) :
        if sudoku[row][i] == num :
            return False
    
    for i in range(9) :
        if sudoku[i][col] == num :
            return False
        
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3) :
        for j in range(3) :
            if sudoku[startRow+i][startCol+j] == num :
                return False
    return True

def solveSuduko(sudoku,emp,curr):
    if curr==len(emp):
        return True
    for i in range(1,10):
        if isSafe(sudoku,emp[curr][0],emp[curr][1],i):
            sudoku[emp[curr][0]][emp[curr][1]]=i
            if solveSuduko(sudoku,emp,curr+1):
                return True
            else:
                sudoku[emp[curr][0]][emp[curr][1]]=0

def solver(sudoku) :
    emp=[]
    for i in range(N):
        for j in range(N):
            if sudoku[i][j]==0:
                emp.append([i,j]);
    
    if (solveSuduko(sudoku,emp,0)):
        return sudoku
    else:
        return "no"


btn1 = Button(root,command=getValues,text="Solve",width=10)
btn1.grid(row=20,column=1,columnspan=5,pady=20)

btn2 = Button(root,command=clearValues,text="Clear",width=10)
btn2.grid(row=20,column=5,columnspan=5,pady=20)

def updatevalues(s) :
    sol = solver(s)
    if sol != "no" :
        for rows in range(2,11) :
            for col in range(1,10) :
                cells[(rows,col)].delete(0,"end")
                cells[(rows,col)].insert(0,sol[rows-2][col-1])
            solvedLabel.configure(text="Sudoko solved!")
    else :
        errLabel.configure(text="No solution exists for this suduko")



draw9x9Grid()
root.mainloop()