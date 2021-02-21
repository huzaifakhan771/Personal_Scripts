# from tkinter import *
# from PIL import ImageTk, Image

# root = Tk()
# root.title('User Questionnaire')
# root.geometry("400x400")

# def close():
# 	# Label(root, text=var1.get()).pack()
# 	status = var2.get()
# 	if status == 1:
# 		root.destroy()
# 	else:
# 		Label(root, text="Check No to close window").pack()


# var1 = IntVar()
# var2 = IntVar()

# c1 = Checkbutton(root, text="Yes", variable=var1)
# c1.pack(pady=(0,100))
# c2 = Checkbutton(root, text="No", variable=var2)
# c2.pack()

# myButton = Button(root, text="Submit", command=close).pack()

# root.mainloop()


from tkinter import *

root = Tk()
root.title("Questionnaire")

qs = ["Did you clear PCR test?", "Did you travel in the past 2 weeks?", "Do you have body aches?",
"Do you have dry cough?", "Do you have any relatives with COVID-19 Symptoms?"]

rows=len(qs)
columns=2

boxes = []
boxVars = []

# Create all IntVars, set to 0

for i in range(rows):
    boxVars.append([])
    for j in range(columns):
        boxVars[i].append(IntVar())
        boxVars[i][j].set(0)

def checkRow(i):
    global boxVars, boxes
    row = boxVars[i]
    deselected = []

    # Loop through row that was changed, check which items were not selected 
    # (so that we know which indeces to disable in the event that 2 have been selected)

    for j in range(len(row)):
        if row[j].get() == 0:
            deselected.append(j)

    # Check if enough buttons have been selected. If so, disable the deselected indeces,
    # Otherwise set all of them to active (in case we have previously disabled them).

    if len(deselected) == (len(row) - 1):
        for j in deselected:
            boxes[i][j].config(state = DISABLED)
    else:
        for item in boxes[i]:
            item.config(state = NORMAL)


def submitfunc():
	output_yes = [out[0].get() for out in boxVars]
	output_no = [out[1].get() for out in boxVars]
	for i in range(len(output_yes)):
		if output_yes[i] == 0 and output_no[i] == 0:
			all_questions = Label(root, text='Please answer all the questions').grid(row=12,column=0)
			return -1

	print("Yes", output_yes)
	print("No", output_no)

	global status
	status = 'safe'

	if output_yes[0] == 0:
		status = 'Not Safe'
	if output_yes[1] == 1:
		status = 'Not Safe'	
	if output_yes[2] == 1:
		status = 'Not Safe'
	if output_yes[3] == 1:
		status = 'Not Safe'
	if output_yes[4] == 1:
		status = 'Not Safe'

	status_label = Label(root, text=status).grid(row=12,column=0)

	root.destroy()

for x, q in enumerate(qs):
    boxes.append([])
    Label(root, text= 'yes').grid(row=0,column=0+1)
    Label(root, text= 'no').grid(row=0,column=1+1)
    Label(root, text= q).grid(row=x+1,column=0)
    # Label(root, text= "Test %s"%(x+1)).grid(row=x+1,column=1)
    boxes[x].append(Checkbutton(root, variable = boxVars[x][0], command = lambda x = x: checkRow(x)))
    boxes[x].append(Checkbutton(root, variable = boxVars[x][1], command = lambda x = x: checkRow(x)))
    boxes[x][0].grid(row=x+1, column=0+1)
    boxes[x][1].grid(row=x+1, column=1+1)


submit = Button(root, text = "submit", command = submitfunc, width = 10)
submit.grid(row = 12, column = 11)

mainloop()


print(status)