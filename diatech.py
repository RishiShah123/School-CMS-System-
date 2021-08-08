import sys
import sqlite3
from datetime import datetime
from dearpygui.core import *
from dearpygui.simple import *
import pandas as pd

def close(x):
    delete_item(x)

def exit_main_window (sender, data):
    stop_dearpygui
    sys.exit()
   

# get selected data from cell
def tablePrinter(sender, data):
    coordList = get_table_selections("Table Supervisor")
    row = 0
    for coordinates in coordList:
        row = coordinates[0]
    
    with window("Supervisor Interface"):
        set_value("Supervisor ID", get_table_item("Table Supervisor", row, 0))
        set_value("Supervisor Name", get_table_item("Table Supervisor", row, 1))
        set_value("Supervisor Type", get_table_item("Table Supervisor", row, 2))
        set_value("Supervisor Email", get_table_item("Table Supervisor", row, 3))
   
def clear_sup_interface(sender, data):
     with window("Supervisor ID"):
        set_value("Supervisor Name", "")
        set_value("Supervisor Name", "")
        set_value("Supervisor Type", "Teacher")
        set_value("Supervisor Email", "")
        clear_table("Table Supervisor")
        items = sup_display_data("select * from Supervisors;")
        for item in items:
            add_row("Table Supervisor", [item[0], item[1], item[2],item[3]])

# Display data from sqllite to the dearpygui table
def sup_display_data(str_select):
    conn = sqlite3.connect('diatech.db')
    c =conn.cursor()
    c.execute(str_select)
    items = c.fetchall()
    return items
    conn.commit()
    conn.close()
    
# insert data in the table        
def sup_add_data(str_insert):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    
    with window("Supervisor Interface"):
        if (get_value("Supervisor Name")==""):
            add_text("Please fill in the name")
        elif (get_value("Supervisor Email")==""):
            add_text("Please fill in the email")
        else:
            c.execute(str_insert)
            conn.commit()
            set_value("Supervisor Name", "")
            set_value("Supervisor Type", "Teacher")
            set_value("Supervisor Email", "")
            clear_table("Table Supervisor")
            items = sup_display_data("select * from Supervisors;")
            for item in items:
                 add_row("Table Supervisor", [item[0], item[1], item[2],item[3]])
    conn.close()

    # insert data in the table        
def sup_update_data(str_update):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_update)
    conn.commit()
    # clear contents of the supervisor form
    with window("Supervisor Interface"):
        if (get_value("Supervisor Name")==""):
            add_text("Please fill in the name")
        elif (get_value("Supervisor Email")==""):
            add_text("Please fill in the email")
        else:
            add_text("Data successfully updated")
            set_value("Supervisor Name", "")
            set_value("Supervisor Type", "Teacher")
            set_value("Supervisor Email", "")
            clear_table("Table Supervisor")
            items = sup_display_data("select * from Supervisors;")
            for item in items:
                add_row("Table Supervisor", [item[0], item[1], item[2],item[3]])
    conn.close()
    
# Delete data in the table        
def sup_del_data(str_delete):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_delete)
    conn.commit()
    # clear contents of the supervisor form
    with window("Supervisor Interface"):
        if (get_value("Supervisor Name")==""):
            add_text("Please fill in the name")
        elif (get_value("Supervisor Email")==""):
            add_text("Please fill in the email")
        else:
           
            set_value("Supervisor Name", "")
            set_value("Supervisor Type", "Teacher")
            set_value("Supervisor Email", "")
            clear_table("Table Supervisor")
            items = sup_display_data("select * from Supervisors;")
            for item in items:
                 add_row("Table Supervisor", [item[0], item[1], item[2],item[3]])
    conn.close()

#window object settings
set_main_window_size(1366,768)
set_main_window_pos(0, 0)
set_global_font_scale(1)
set_theme("Dark  ")
set_style_window_padding(30,30)

def sup_Interface():    
    with window("Supervisor Interface", width=1000, height=575, no_resize = True, no_move = False, no_close=True):
        #add_drawing("suplogo", width=48, height=48) #create some space for the image
        #draw_image("suplogo", "D:\Python Projects\supicon.png", [0,0], [48,48])
        add_text("This Section is to Add/Edit/Delete Supervisors", color=[215,122,13])
        conn = sqlite3.connect('diatech.db')
        c = conn.cursor()
        add_separator()
        set_window_pos("Supervisor Interface", 200, 60)
        add_input_text("Supervisor ID", width=1)
        #Hide ID field
        hide_item("Supervisor ID")
        add_spacing(count=5)
        add_input_text("Supervisor Name", width=415)
        add_spacing(count=5)
        suptype = ["Teacher", "Club Member", "Assistant", "Admin"]
        add_combo("Supervisor Type", items=suptype, default_value="Club member", width=415)
        add_spacing(count=5)
        add_input_text("Supervisor Email", width=415)
        add_spacing(count=5)
        add_button("Add", callback=lambda: sup_add_data("Insert into Supervisors(Supervisor_Name, Supervisor_Specialization, Supervisor_Email) values('" + get_value("Supervisor Name") + "','" + get_value("Supervisor Type") + "','" + get_value("Supervisor Email") + "');"))
        with popup("Add", "Add Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added succesfully!", wrap=-1)
            add_button("Add Done", callback=lambda: close_popup("Add Message"))
        add_same_line()
        add_button("Update", callback=lambda: sup_edit_data("update Supervisors SET Supervisor_Name= '" + get_value("Supervisor Name") + "', Supervisor_Specialization= '" + get_value("Supervisor Type") + "', Supervisor_Email= '" + get_value("Supervisor Email") + "' where Supervisor_ID=" + get_value("Supervisor ID") + ";"))
        with popup("Update", "Update Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added Updated!", wrap=-1)
            add_button("Update Done", callback=lambda: close_popup("Update Message"))
        add_same_line()
        add_button("Delete", callback=lambda: sup_del_data("Delete from Supervisors where Supervisor_ID = "  + get_value("Supervisor ID")))
        with popup("Delete", "Delete Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added Deleted!", wrap=-1)
            add_button("Delete Done", callback=lambda: close_popup("Delete Message"))
        add_same_line()
        add_button("Clear", callback= clear_sup_interface)
        with popup("Clear", "Clear Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added Cleared!", wrap=-1)
            add_button("Clear Done", callback=lambda: close_popup("Clear Message"))
        add_same_line()
        add_button("Close", callback= lambda: close("Supervisor Interface"))
        add_spacing(count=5)
        add_table("Table Supervisor", ["ID", "Name", "type", "Email"],callback=tablePrinter)
        items = sup_display_data("select * from Supervisors;")
        for item in items:
            add_row("Table Supervisor", [item[0], item[1], item[2],item[3]])






def volprinter(sender, data):
    coordList = get_table_selections("Table Volunteer")
    row = 0
    for coordinates in coordList:
        row = coordinates[0]
    with window("Volunteer Interface"):
        set_value("Volunteer ID", get_table_item("Table Volunteer", row, 0))
        set_value("Volunteer Name", get_table_item("Table Volunteer", row, 1))
        set_value("Volunteer Year", get_table_item("Table Volunteer", row, 2))
        set_value("Volunteer Email", get_table_item("Table Volunteer", row, 3))
   
def vol_clear(sender, data):
     with window("Volunteer Interface"):
        set_value("Volunteer ID", "")
        set_value("Volunteer Name", "")
        set_value("Volunteer Year", "10")
        set_value("Volunteer Email", "")
        clear_table("Table Volunteer")
        items = vol_display("select * from Volunteers;")
        for item in items:
            add_row("Table Volunteer", [item[0], item[1], item[2],item[3]])

# Display data from sqllite to the dearpygui table
def vol_display(str_select):
    conn = sqlite3.connect('diatech.db')
    c =conn.cursor()
    c.execute(str_select)
    items = c.fetchall()
    return items
    conn.commit()
    conn.close()
    
# insert data in the table        
def vol_add(str_insert):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    with window("Volunteer Interface"):
        if (get_value("Volunteer Name")==""):
            add_text("Please fill in the name")
        elif (get_value("Volunteer Email")==""):
            add_text("Please fill in the email")
        else:
            c.execute(str_insert)
            conn.commit()
          
            set_value("Volunteer ID", "")
            set_value("Volunteer Name", "")
            set_value("Volunteer Year", "10")
            set_value("Volunteer Email", "")
            clear_table("Table Volunteer")
            x = 1
            items = vol_display("select * from Volunteers;")
            for item in items:
                add_row("Table Volunteer", [item[0], item[1], item[2],item[3]])
    conn.close()

    # insert data in the table        
def vol_edit(str_update):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_update)
    conn.commit()
    # clear contents of the supervisor form
    with window("Volunteer Interface"):
        if (get_value("Volunteer Name")==""):
            add_text("Please fill in the name")
        elif (get_value("Volunteer Email")==""):
            add_text("Please fill in the email")
        else:
        
            set_value("Volunteer ID", "")
            set_value("Volunteer Name", "")
            set_value("Volunteer Year", "10")
            set_value("Volunteer Email", "")
            clear_table("Table Volunteer")
            x = 1
            items = vol_display("select * from Volunteers;")
            for item in items:
                add_row("Table Volunteer", [item[0], item[1], item[2],item[3]])
    conn.close()
   
# Delete data in the table        
def vol_del(str_delete):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_delete)
    conn.commit()
    # clear contents of the supervisor form
    with window("Volunteer Interface"):
        if (get_value("Volunteer Name")==""):
            add_text("Please fill in the name")
        elif (get_value("Volunteer Email")==""):
            add_text("Please fill in the email")
        else:
            
            set_value("Volunteer ID", "")
            set_value("Volunteer Name", "")
            set_value("Volunteer Year", "11")
            set_value("Volunteer Email", "")
            clear_table("Table Volunteer")
           
            items = vol_display("select * from Volunteers;")
            for item in items:
                add_row("Table Volunteer", [item[0], item[1], item[2],item[3]])
    conn.close()

#window object settings
set_main_window_size(1366,768)
set_main_window_pos(0, 0)
set_global_font_scale(1)
set_theme("Dark  ")
set_style_window_padding(30,30)

def vol_Interface():    
    with window("Volunteer Interface", width=1000, height=575, no_resize = True, no_move = False, no_close=True):
        conn = sqlite3.connect('diatech.db')
        c = conn.cursor()
        add_text("This Section is to Add/Edit/Delete Volunteers", color=[215,122,13])
        add_separator()
        set_window_pos("Volunteer Interface", 200, 60)
        add_input_text("Volunteer ID", width=1)
        hide_item("Volunteer ID")
        add_spacing(count=5)
        add_input_text("Volunteer Name", width=415)
        add_spacing(count=5)
        volyear = ["10", "11", "12"]
        add_combo("Volunteer Year", items=volyear, default_value="11", width=415)
        add_spacing(count=5)
        add_input_text("Volunteer Email", width=415)
        add_spacing(count=5)
        add_button("Add", callback=lambda: vol_add("Insert into Volunteers(Volunteer_Name, Volunteer_Year, Volunteer_Email) values('" + get_value("Volunteer Name")+ "','" + get_value("Volunteer Year") + "','" + get_value("Volunteer Email") + "');"))
        with popup("Add", "Add Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added succesfully!", wrap=-1)
            add_button("Add Done", callback=lambda: close_popup("Add Message"))
        add_same_line()
        add_button("Update", callback=lambda: vol_edit("update Volunteers SET Volunteer_Name= '" + get_value("Volunteer Name") + "', Volunteer_Year= '" + get_value("Volunteer Year") + "', Volunteer_Email='" + get_value("Volunteer Email") + "' where Volunteer_ID=" + get_value("Volunteer ID") + ";"))
        with popup("Update", "Update Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data updated succesfully!", wrap=-1)
            add_button("Update Done", callback=lambda: close_popup("Update Message"))
        add_same_line()
        add_button("Delete", callback=lambda: vol_del("Delete from Volunteers where Volunteer_ID = "  + get_value("Volunteer ID")))
        with popup("Delete", "Delete Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data deleted succesfully!", wrap=-1)
            add_button("Delete Done", callback=lambda: close_popup("Delete Message"))
        add_same_line()
        add_button("Clear", callback= vol_clear)
        with popup("Clear", "Clear Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data cleared succesfully!", wrap=-1)
            add_button("Clear Done", callback=lambda: close_popup("Clear Message"))
        add_same_line()
        add_button("Close", callback=lambda: close("Volunteer Interface"))
        add_spacing(count=5)
        add_table("Table Volunteer", ["ID", "Name", "year", "Email"],callback=volprinter)
        items = vol_display("select * from Volunteers;")
        for item in items:
            add_row("Table Volunteer", [item[0], item[1], item[2],item[3]])


def actprinter(sender, data):
    coordList = get_table_selections("Table Activity")
    row = 0
    for coordinates in coordList:
        row = coordinates[0]
    with window("Activity Interface"):
        set_value("Activity ID", get_table_item("Table Activity", row, 0))
        set_value("Activity Name", get_table_item("Table Activity", row, 1))
        set_value("Activity Supervisor", get_table_item("Table Activity", row, 2))
        set_value("Activity Location", get_table_item("Table Activity", row, 3))
        set_value("Activity Time", get_table_item("Table Activity", row, 4))
   
def clear_act(sender, data):
     with window("Activity Interface"):
        set_value("Activity ID", "")
        set_value("Activity Name", "")
        set_value("Activity Supervisor", "")
        set_value("Activity Location", "PE hall")
        set_value("Activity Time", "Lunch")
        clear_table("Table Activity")
        items = display_act("select * from Activity;")
        for item in items:
            add_row("Table Activity", [item[0], item[1], item[2],item[3],item[4]])

# Display data from sqllite to the dearpygui table
def display_act(str_select):
    conn = sqlite3.connect('diatech.db')
    c =conn.cursor()
    c.execute(str_select)
    items = c.fetchall()
    return items
    conn.commit()
    conn.close()
    
# insert data in the table        
def add_act(str_insert):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
   
    with window("Activity Interface"):
        if (get_value("Activity Name")==""):
            add_text("Please fill in the name")
        else:
            c.execute(str_insert)
            conn.commit()
            set_value("Activity ID", "")
            set_value("Activity Name", "")
            set_value("Activity Location", "PE hall")
            set_value("Activity Time", "Lunch")
            clear_table("Table Activity")
            items = display_act("select * from Activity;")
            for item in items:
                add_row("Table Activity", [item[0], item[1], item[2],item[3],item[4]])
    conn.close()

    # insert data in the table        
def edit_act(str_update):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_update)
    conn.commit()
    # clear contents of the supervisor form
    with window("Activity Interface"):
        if (get_value("Activity Name")==""):
                    add_text("Please fill in the name")
        else:
            add_text("Data updated")
            set_value("Activity ID", "")
            set_value("Activity Name", "")
            set_value("Activity Supervisor", "")
            set_value("Activity Location", "PE hall")
            set_value("Activity Time", "Lunch")
            clear_table("Table Activity")
            items = display_act("select * from Activity;")
            for item in items:
                add_row("Table Activity", [item[0], item[1], item[2],item[3], item[4]])
    conn.close()
   
# Delete data in the table        
def del_act(str_delete):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_delete)
    conn.commit()
    # clear contents of the supervisor form
    with window("Activity Interface"):
        if (get_value("Activity Name")==""):
            add_text("Please fill in the name")
        else:
            set_value("Activity ID", "")
            set_value("Activity Name", "")
            set_value("Activity Supervisor", "")
            set_value("Activity Location", "PE hall")
            set_value("Activity Time", "Lunch")
            clear_table("Table Activity")
            items = display_act("select * from Activity;")
            for item in items:
                add_row("Table Activity", [item[0], item[1], item[2],item[3],item[4]])
    conn.close()

    #window object settings
set_main_window_size(1366,768)
set_main_window_pos(0, 0)
set_global_font_scale(1)
set_theme("Dark  ")
set_style_window_padding(30,30)



def a_id():
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    h = c.fetchall()
    query = "SELECT * FROM Activity"
    l = c.execute(query)
    h = []
    for y in l:
        h.append(y)
    u = len(h) + 1
    return str(u)

def sidconvert(sup):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    name = get_value("Activity Supervisor")

    query = "SELECT Supervisor_ID FROM Supervisors WHERE Supervisor_Name = '%s'" %(name) 
    t = c.execute(str(query))
    a=0 
    for h in t:
        l1 = len(h)
        y = str(h[0])
        k = int(y)
        if (k==l1):
            sup.pop()
        else:
            a = k-1
        sup.pop(a)
        configure_item("Activity Supervisor", items=sup)
        return y

    
    

        

def act_Interface():    
    with window("Activity Interface", width=1000, height=575, no_resize = True, no_move = False, no_close=True):
        #add_drawing("suplogo", width=48, height=48) #create some space for the image
        #draw_image("suplogo", "D:\Python Projects\supicon.png", [0,0], [48,48])
        conn = sqlite3.connect('diatech.db')
        c = conn.cursor()
        add_text("This Section is to Add/Edit/Delete Activities", color=[215,122,13])
        add_separator()
        set_window_pos("Activity Interface", 200, 60)
        add_input_text("Activity ID", width=1)
        #Hide ID field
        hide_item("Activity ID")
        add_spacing(count=5)
        add_input_text("Activity Name", width=415)
        add_spacing(count=5)
        actlocation = ["Pe Hall" , "Presentation Hall" , "Lab" , "Quad" , "Hall Entrance", "field" ]
        acttime = ["Lunch" , "All day" , "day before"]
        
        query = c.execute("select Supervisors.Supervisor_Name from Supervisors;")
        k = []
        for i in query:
            j = str(i)
            r = j[2:-3]
            k.append(r)
        
        add_combo("Activity Supervisor", items=k, default_value="", width= 415)
        add_spacing(count=5)     
        
        
        add_combo("Activity Location", items=actlocation, default_value="PE Hall", width=415)
        add_spacing(count=5)
        add_combo("Activity Time", items=acttime, default_value="Lunch", width=415)
        add_spacing(count=5)
        add_button("Add", callback=lambda: add_act("Insert into Activity(Activity_ID, Activity_Name, Activity_Location, Activity_Time, Activity_Supervisor) values('" + a_id() + "','" + get_value("Activity Name")+ "','" + get_value("Activity Location") + "','" +  get_value("Activity Time") + "','" + sidconvert(k) + "');"))
        with popup("Add", "Add Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added succesfully!", wrap=-1)
            add_button("Add Done", callback=lambda: close_popup("Add Message"))
        add_same_line()
        
        add_button("Update", callback=lambda: edit_act("update Activity SET Activity_Name= '" + get_value("Activity Name") + "', Activity_Supervisor= '"  + "', Activity Location='" + get_value("Activity Location") + "', Activity Time='" + get_value("Activity Time") + "' where Activity_ID=" + get_value("Activity ID") + ";"))
        with popup("Update", "Update Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data updated succesfully!", wrap=-1)
            add_button("Update Done", callback=lambda: close_popup("Update Message"))
        add_same_line()
        add_button("Delete", callback=lambda: del_act("Delete from Activity where Activity_ID = "  + get_value("Activity ID")))
        with popup("Delete", "Delete Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data deleted succesfully!", wrap=-1)
            add_button("Delete Done", callback=lambda: close_popup("Delete Message"))
        add_same_line()
        add_button("Clear", callback= clear_act)
        with popup("Clear", "Clear Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data cleared succesfully!", wrap=-1)
            add_button("Clear Done", callback=lambda: close_popup("Clear Message"))
        add_same_line()
        add_button("Close", callback= lambda: close("Activity Interface"))
        add_spacing(count=5)
        add_table("Table Activity", ["ID", "Name", "Supervisor", "Location", "Time"],callback=actprinter)
        items = display_act("select * from Activity;")
        for item in items:
            add_row("Table Activity", [item[0], item[1], item[2],item[3], item[4]])
        conn.close()

# get selected data from cell
def assprinter(sender, data):
    coordList = get_table_selections("Table Assignment")
    row = 0
    for coordinates in coordList:
        row = coordinates[0]
    
    with window("Volunteer Interface"):
        set_value("Assignment ID", get_table_item("Table Assignment", row, 0))
        set_value("Activity Name", get_table_item("Table Assignment", row, 1))
        set_value("Volunteer Name", get_table_item("Table Assignment", row, 2))
     
   
def ass_clear(sender, data):
     with window("Volunteer Interface"):
        set_value("Assignment ID","")
        set_value("Activity Name", "")
        set_value("Volunteer Name","")
        clear_table("Table Assignment")
        items = ass_display("select * from Assignment;")
        for item in items:
            add_row("Table Assignment", [item[0], item[1], item[2]])
# Display data from sqllite to the dearpygui table
def ass_display(str_select):
    conn = sqlite3.connect('diatech.db')
    c =conn.cursor()
    c.execute(str_select)
    items = c.fetchall()
    return items
    conn.commit()
    conn.close()
    
# insert data in the table        
def ass_add_data(str_insert):
    x = 0;
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    
    with window("Assignment Interface"):
        query = "select Volunteer_Name from Assignment where Activity_Name = '%s'" %(get_value("Activity Name"))
        v = c.execute(query)
        vname = []

        t = 0;
        for u in v:
            j = str(u)
            vname.append(j[2:-3])
            t = t+1
        if (t>=5):
            add_text("No more volunteers needed ")
        else:
            c.execute(str_insert)
            conn.commit()
            set_value("Assignment ID","")
            set_value("Activity Name", "")
            set_value("Volunteer Name","")
            clear_table("Table Assignment")
            items = ass_display("select * from Assignment;")
            for item in items:
                add_row("Table Assignment", [item[0], item[1], item[2]])
    conn.close()

    # insert data in the table        
def ass_edit(str_update):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_update)
    conn.commit()
    # clear contents of the supervisor form
    with window("Assignment Interface"):
        c.execute(str_insert)
        conn.commit()
        set_value("Assignment ID","")
        set_value("Activity Name", "")
        set_value("Volunteer Name","")
        clear_table("Table Assignment")
        items = ass_display("select * from Assignment;")
        for item in items:
            add_row("Table Assignment", [item[0], item[1], item[2]])
    conn.close()
   
# Delete data in the table        
def ass_del(str_delete):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute(str_delete)
    conn.commit()
    # clear contents of the supervisor form
    with window("Assignment Interface"):
        c.execute(str_insert)
        conn.commit()
        set_value("Assignment ID","")
        set_value("Activity Name", "")
        set_value("Volunteer Name","")
        clear_table("Table Assignment")
        items = ass_display("select * from Assignment;")
        for item in items:
            add_row("Table Assignment", [item[0], item[1], item[2]])
    conn.close()

#window object settings
set_main_window_size(1366,768)
set_main_window_pos(0, 0)
set_global_font_scale(1)
set_theme("Dark  ")
set_style_window_padding(30,30)

def ass_Interface():    
    with window("Assignment Interface", width=1000, height=575, no_resize = True, no_move = False, no_close=True):
        #add_drawing("suplogo", width=48, height=48) #create some space for the image
        #draw_image("suplogo", "D:\Python Projects\supicon.png", [0,0], [48,48])
        add_text("This Section is to Add/Edit/Delete Assignments", color=[215,122,13])
        add_separator()
        set_window_pos("Assignment Interface", 200, 60)
        add_input_text("Assignment ID", width=1)
        #Hide ID field
        hide_item("Assignment ID")
        add_spacing(count=5)
        conn = sqlite3.connect('diatech.db')
        c = conn.cursor()
        query1 = c.execute("select Activity_Name from Activity;")
        list1 = []
        for i in query1:
                x = str(i)
                k = x[2:-3]
                list1.append(k)
        add_spacing(count=5)
        add_combo("Activity Name", items= list1, default_value="", width= 415)
        query2 = c.execute("select Volunteer_Name from Volunteers;")
        list2 = []
        for p in query2:
            x = str(p)
            r = x[2:-3]
            list2.append(r)
        add_spacing(count=5)
       
        add_combo("Volunteer Name", items=list2, default_value="", width=415)
        add_spacing(count=5)
        add_button("Add", callback=lambda: ass_add_data("Insert into Assignment(Activity_Name, Volunteer_Name) values('" + get_value("Activity Name")+ "','" + get_value("Volunteer Name") + "');"))
        with popup("Add", "Add Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data added succesfully!", wrap=-1)
            add_button("Add Done", callback=lambda: close_popup("Add Message"))
        add_same_line()
        add_button("Update", callback=lambda: ass_edit("update Assignment SET Activity_Name= '" + get_value("Activity Name") + "', Volunteer_Name= '" + get_value("Volunteer Name") + "' where Assignment_ID=" + get_value("Assignment ID") + ";"))
        with popup("Update", "Update Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data updated succesfully!", wrap=-1)
            add_button("Update Done", callback=lambda: close_popup("Update Message"))
        add_same_line()
        add_button("Delete", callback=lambda: ass_del("Delete from Assignment where Assignment_ID = "  + get_value("Assignment ID")))
        with popup("Delete", "Delete Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data deleted succesfully!", wrap=-1)
            add_button("Delete Done", callback=lambda: close_popup("Delete Message"))
        add_same_line()
        add_button("Clear", callback= ass_clear) 
        with popup("Clear", "Clear Message", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Data cleared succesfully!", wrap=-1)
            add_button("Clear Done", callback=lambda: close_popup("Clear Message"))
        add_same_line()
        add_button("Close", callback= lambda: close("Assignment Interface"))
        add_spacing(count=5)
        add_table("Table Assignment", ["ID", "Activity Name", "Volunteer Name"],callback=assprinter)
        items = ass_display("select * from Assignment;")
        for item in items:
            add_row("Table Assignment", [item[0], item[1], item[2]])
def list_items_report_one():
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    query = c.execute("select Activity_Name from Activity;")
    l = []
    for i in query:
        r = str(i)
        o = r[2:-3]
        l.append(o)
    return l
def list_items_report_two():
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    query = c.execute("select Volunteer_Name from Volunteers;")
    y = []
    for i in query:
        t = str(i)
        p = t[2:-3]
        y.append(p)
    return y
def list_items_report_three():
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    query = c.execute("select Activity_Time from Activity;")
    a = []
    o = 1
    for i in query:
        p = str(i)
        k = p[2:-3]
        a.append(k)
        o = o + 1
        if (o==4):
            break
    return a
def report_one_generator(a):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    query = "select Volunteer_Name from Assignment where Activity_Name = '%s'" %(a)

    v = c.execute(query)
    x = []
    e = []
    for i in v:
        j = str(i)
        x.append(j[2:-3])
        print(j)
    for p in x:
        querytwo = "select Volunteer_ID from Volunteers where Volunteer_Name = '%s'" %(p)
        t = c.execute(querytwo)
        for q in t:
            e.append(q)
    data = {'ID':e,
        'Name':x}
    df = pd.DataFrame(data, columns  = ['ID', 'Name'])
    return df.to_excel('report1.xlsx')
    conn.close()

def report_two_generator(b):
    print(b)
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    query = "select Activity_Name from Assignment where Volunteer_Name = '%s'" %(b)
    h = c.execute(query)
    aname = []
    aid = []
    asup = []
    alocation = []
    atime = []
    for i in h:
        j = str(i)
        aname.append(j[2:-3])
        print(j)
    for p in aname:
        query = "select Activity_ID from Activity where Activity_Name = '%s'" %(p)
        f = c.execute(query)
        for q in f:
            aid.append(q)
    for x in aname:
        query = "select Activity_Supervisor from Activity where Activity_Name = '%s'" %(x)
        u = c.execute(query)
        for q in u:
            asup.append(q)
    for n in aname:
        query = "select Activity_Location from Activity where Activity_Name = '%s'" %(n)
        j = c.execute(query)
        for q in j:
            alocation.append(q)
    for b in aname:
        query = "select Activity_Time from Activity where Activity_Name = '%s'" %(b)
        v = c.execute(query)
        for q in v:
            atime.append(q)
    data = {'ID':aid,
        'Name':aname,
        'Supervisor': asup,
        'Location': alocation,
        'Time': atime}
    df = pd.DataFrame(data, columns  = ['ID', 'Name','Supervisor', 'Location', 'Time'])
    return df.to_excel('report2.xlsx')
    conn.close()
def report_three_generator(a):
    print(a)
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    query = "select Activity_Name from Activity where Activity_Time = '%s'" %(a)
    p = c.execute(query)
    volname = []
    actname = []
    for i in p:
        l = str(i)
        actname.append(l[2:-3])
        print(l)
    for p in actname:
        sqltwo = "select Volunteer_Name from Assignment where Activity_Name = '%s'" %(p)
        t = c.execute(sqltwo)
        for q in t:
            volname.append(q)
    data = {'Activity Name':actname,
        'Volunteer Name':volname}
    df = pd.DataFrame(data, columns  = ['Activity Name', 'Volunteer Name'])
    return df.to_excel('report3.xlsx')
    conn.close()


def allcases():    
    with window("Report Interface", width=1000, height=575, no_resize = True, no_move = False, no_close=True):
        #add_drawing("suplogo", width=48, height=48) #create some space for the image
        #draw_image("suplogo", "D:\Python Projects\supicon.png", [0,0], [48,48])
        add_text("This Section is to create report based on what you want", color=[215,122,13])
        add_separator()
        set_window_pos("Reports Interface", 200, 60)
        add_combo("R1 - Activity", items=list_items_report_one(), default_value="", width=415)
        add_spacing(count=5)
        add_combo("R2 - Volunteer", items=list_items_report_two(), default_value="", width=415)
        add_spacing(count=5)
        add_combo("R3 - Time", items=list_items_report_three(), default_value="", width=415)
        add_spacing(count=5)
        add_button("Report_one", callback=lambda: report_one_generator(get_value("R1 - Activity")))
        with popup("Report_one", "Report1", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Your excel file is being made", wrap=-1)
            add_button("Done", callback=lambda: close_popup("Report1"))
        add_same_line()
        add_button("Report_Two", callback=lambda: report_two_generator(get_value("R2 - Volunteer")))
        with popup("Report_Two", "report2", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Your second report is being made", wrap=-1)
            add_button("Done", callback=lambda: close_popup("report2"))
        add_same_line()
        add_button("Report_Three", callback=lambda: report_three_generator(get_value("R3 - Time")))
        with popup("Report_Three", "Report3", modal=True, mousebutton=mvMouseButton_Left):
            add_text("Your excel file is being made", wrap=-1)
            add_button("Done", callback=lambda: close_popup("Report3"))

        add_same_line()
        add_button("Close", callback= lambda: close("Report Interface"))
def acttovol(a):
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    sqlone = "select Volunteer_Name from Assignment where Activity_Name = '%s'" %(a)
    v = c.execute(sqlone)
    vname = []
    for i in v:
        j = str(i)
        vname.append(j[2:-3])
    with window("Volunteer Roll Call 2", width=800, height=400, no_resize = True, no_move = False, no_close=True):
        
        add_text("This Section is for Volunteer Roll Call", color=[232,163,33])
        add_separator()
        set_window_pos("Volunteer Roll call 2", 200, 60)
        conn = sqlite3.connect('diatech.db')
        c = conn.cursor()
        add_spacing(count=5)
        add_combo("Volunteers", items= vname, width= 415)
        add_button("Present", callback= lambda: present(get_value("Volunteers")))
        add_same_line()
        add_button("Absent", callback= lambda: abesent(get_value("Volunteers")))
        add_same_line()
        
def attendence ():
    with window("Roll Call", width=1000, height=575, no_resize = True, no_move = False, no_close=True):
        add_text("Roll Call", color=[232,163,33])
        add_separator()
        set_window_pos("Roll call", 200, 60)
        conn = sqlite3.connect('diatech.db')
        c = conn.cursor()
        query = c.execute("select Activity_Name from Activity;")
        l = []
        for i in query:
                j = str(i)
                k = j[2:-3]
                l.append(k)
        add_spacing(count=5)
        add_combo("Activities", items= l, width= 415)
        add_button("Next", callback= lambda: acttovol(get_value("Activities")))
        add_same_line()



def present(a):
    print(a)
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute("UPDATE Volunteers SET Volunteer_Present = 'Present' WHERE Volunteer_Name = '%s'" %(a))

def abesent(a):
    print(a)
    conn = sqlite3.connect('diatech.db')
    c = conn.cursor()
    c.execute("UPDATE Volunteers SET Volunteer_Present = 'Absent' WHERE Volunteer_Name = '%s'" %(a))



#Main DiaTech Interface (Start Screen)        
with window("Diatech Interface", width=1340, height=680,no_resize = False, no_move = False, no_close=True):
    set_window_pos("Diatech Interface", 0, 0)
    conn = sqlite3.connect('diatech.db')
    c =conn.cursor()
    #c.execute("select * from supervisor")
    conn.commit()
    now = datetime.now()
    dt_string = now.strftime("%d %B %Y %H:%M:%S")
    add_text("Welcome! You are sucessfully connected to Di@Tech Database ~ " + str(dt_string), color=[143, 216, 218])        
    conn.close()
    #image logo
    #add_drawing("logo", width=1300, height=550) #create some space for the image
    #draw_image("logo", "a.JPG", [0,0], [1300,550])

    with menu_bar("Main Menu Bar"): 
        with menu("File"):
            add_menu_item("Exit", callback=exit_main_window)

        with menu("Data Entry"):                             # simple
            add_menu_item("Supervisor", callback=sup_Interface)            
            add_menu_item("Volunteer", callback=vol_Interface)
            add_menu_item("Activity", callback=act_Interface)
            add_menu_item("Assign volunteers", callback = ass_Interface)
        
        with menu("Report"):                             # simple
            add_menu_item("All", callback=allcases)

        with menu("Extensions"):
            add_menu_item("Roll call", callback=attendence )

start_dearpygui()

