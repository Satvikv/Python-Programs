import tkinter

root = tkinter.Tk()

var = tkinter.StringVar()


label = tkinter.Message(root,aspect=200,textvariable=var,pady=50)
var.set("hey!")
childLabel=tkinter.Entry(label)
childLabel.pack(side="bottom")
label.pack()
root.mainloop()	
