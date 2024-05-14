from classes.docwriter import DocWriter 
import excelData as ex
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

import os

def makeDocumentFromRoute(source, destination, alternatives = 1):
    src = source.get()
    dst = destination.get()
    alts = 1
    try:
        alts = int(alternatives)
    except ValueError:
        messagebox.showwarning("Warning", "Valid number of alternatives not specified, showing shortest route available.")
    writer = DocWriter(src + " to " + dst + " draft procedure data:")
    #route is found here:
    routes = components[src].routesTo(components[dst], alts)
    #change this to use a selected route from the options instead!
    for route in routes:
        for i in range(1,len(route)-2):
            route[i].setPosition(route)
        writer.buildDocument(route,pits)
    filename = src +"_to_"+ dst + ".docx"
    writer.save(filename)
    os.system(f'start {filename}')

def src_filter(*args):
    query = src_entry.get().lower() 
    src_dropdown['menu'].delete(0, tk.END)
    for node in nodes:
        # if query in node.lower() and (components[node].in_tank or select_from_all):
        if query in node.lower():
            src_dropdown['menu'].add_command(label=node, command=tk._setit(source, node))

def dst_filter(*args):
    query = dst_entry.get().lower() 
    dst_dropdown['menu'].delete(0, tk.END)
    for node in nodes:
        # if query in node.lower() and (components[node].in_tank or select_from_all):
        if query in node.lower():
            dst_dropdown['menu'].add_command(label=node, command=tk._setit(destination, node))

def main():
    window = tk.Tk()
    window.title("Waste Transfer Procedure Data Tool")
    filename = '//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/1 Transfers/1C - Procedure Review Tools/MasterProcedureData.xlsx'
    global components
    global pits 
    try: 
        components, pits =  ex.ImportComponents(filename)
    except Exception as e:
        filewarning ="Unable to find file at:\n\n" + filename + "\n\n Please browse for Excel data file"
        messagebox.showwarning("Warning", filewarning)
        filename = filedialog.askopenfilename(defaultextension="xlsx" ,title = "Select Procedure Data Excel file")
        components, pits =  ex.ImportComponents(filename)

    def toggle_boolean(*args):
        if select_from_all:
            nodes = components.keys()
            for node in nodes:
                # dst_dropdown['menu'].delete(0, tk.END)
                src_dropdown['menu'].add_command(label=node, command=tk._setit(source, node))
                dst_dropdown['menu'].add_command(label=node, command=tk._setit(destination, node))
        else:
            src_filter()
            dst_filter()

    items_to_tank = set()
    for item in components.keys():
        if components[item].in_tank:
            items_to_tank.add(item)
    
    global nodes 
    nodes = items_to_tank

    label0 = tk.Label(window, text="Select transfer origin:")
    label0.grid(row=0, column= 0, pady = 2, padx=10,sticky = "w")

    global source
    source = tk.StringVar(window)
    global src_dropdown
    src_dropdown = tk.OptionMenu(window, source, *nodes)
    src_dropdown.grid(row=0, column= 2, pady=2)
    global src_entry
    src_entry = tk.Entry(window)
    src_entry.grid(row=0, column= 1, pady=5, padx=4)

    label1 = tk.Label(window, text="Select transfer destination:")
    label1.grid(row=2, column= 0, pady = 2, padx=10, sticky = "w")

    global destination
    destination = tk.StringVar(window)
    global dst_dropdown
    dst_dropdown = tk.OptionMenu(window, destination, *nodes)
    dst_dropdown.grid(row=2, column= 2, pady=2)
    global dst_entry
    dst_entry = tk.Entry(window)
    dst_entry.grid(row=2, column= 1, pady=5, padx=4)

    global select_from_all
    select_from_all = tk.BooleanVar()
    select_from_all.set(False)

    checkbox = tk.Checkbutton(window, text="Include Valves", variable=select_from_all, command = toggle_boolean)
    checkbox.grid(row=0, column=4)

    label2 = tk.Label(window, text="Number of route alternatives:")
    label2.grid(row=4, column= 0, pady = 5, padx=10, sticky = "w")

    global alternatives 
    alternatives = tk.Entry(window)
    alternatives.grid(row=4, column= 1, columnspan=1, pady=2)

    label3 = tk.Label(window, text= "Using data from: "+ filename, wraplength=600)
    label3.grid(row = 5, columnspan=9, rowspan=3, padx=10, pady=20,sticky = "n")

    src_entry.bind("<KeyRelease>", src_filter)
    dst_entry.bind("<KeyRelease>", dst_filter)

    printButton = tk.Button(window, text="Find Routes", command=lambda: makeDocumentFromRoute(source, destination, alternatives.get()))
    printButton.grid(row=4, column= 2, pady=5)
    window.mainloop()

if __name__== '__main__':   
    main()

# TO DO: FIGURE OUT DVI, FIGURE OUT SPLITS NECESSARY??