import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import BOLD
from PIL import Image, ImageTk
from data import *
            

class MtnClimberApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        for F in (HomePage, GamePage, LivePage, DeadPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.state('zoomed')
        self.show_frame(HomePage)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

       
class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg = 'white')

        Label(self, text = "MOUNTAIN CLIMBER!", bg = 'white', fg = 'green', font =("Comic Sans MS", 45, BOLD)).pack()

        self.resize_mtn = ImageTk.PhotoImage(Image.open('mtn.png').resize((300, 200)))
        Label(self, image = self.resize_mtn).place(x = 50, y = 100)

        self.resize_mtn2 = ImageTk.PhotoImage(Image.open('mtn2.png').resize((300, 200)))
        Label(self, image = self.resize_mtn2).place(x = 940, y = 100)

        Label(self,height=10, bg='white').pack()

        Button(self, text = 'PLAY!', border=10, font = ("Courier", 30, BOLD), bg = 'grey', fg = 'yellow', width=8, command = lambda: controller.show_frame(GamePage)).pack()
        Label(self, text = 'Tallest Mountains In The World', font = ("Courier", 18, BOLD), fg = 'black', bg = 'white').pack(pady=20)


class GamePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent,bg='white')

        self.img_back = ImageTk.PhotoImage(Image.open('back.png').resize((100, 100)))
        Button(self, image = self.img_back, relief = 'raised', borderwidth = 0, command = lambda: [controller.show_frame(HomePage)] ).place(x=0, y=0)
    
        mountain = StringVar()
        mountain.set("Climb Which Mountain?")
        tool = StringVar()
        tool.set("Bring What Tool?")
        sherpa_food = StringVar()
        sherpa_food.set("Sherpa OR Food?")
        month = StringVar()
        month.set("Climb What Season?")

        mtn_menu = OptionMenu(self, mountain, *mtnData)
        mtn_menu.config(bg='black', fg='white', border=5, font='Sand 15 bold')
        mtn_menu.pack(pady=5)
        tool_menu = OptionMenu(self, tool, *tools)
        tool_menu.config(bg='red', fg='white', border=5, font='Sand 15 bold')
        tool_menu.pack(pady=5)
        sherpa_menu = OptionMenu(self, sherpa_food, "Hire Sherpa", "Bring More Food")
        sherpa_menu.config(bg='green', fg='white', border=5, font='Sand 15 bold')
        sherpa_menu.pack(pady=5)
        month_menu = OptionMenu(self, month, *months)
        month_menu.config(bg='blue', fg='white', border=5, font='Sand 15 bold')
        month_menu.pack(pady=5)

        MountainTable()
                
        def check_fields():
            if mountain.get() == 'Climb Which Mountain?' or tool.get() == 'Bring What Tool?' or sherpa_food.get() == 'Sherpa OR Food?' or month.get() == 'Climb What Season?':
                messagebox.showerror('Error', 'Missing field!')
            else: 
                if live_or_die() == 0:
                    controller.show_frame(DeadPage)
                else:
                    controller.show_frame(LivePage)

        def live_or_die():
            calculation = Calculations(mountain.get(), tool.get(), sherpa_food.get(), month.get()).total_rate()
            if calculation >= .4 and calculation <= .6:
                random_numb = random.randint(0,1)
                if random_numb == 0:
                   return 0
                else:
                    return 1
            elif calculation < .4:
                return 0
            else:
                return 1
        
        def reset():
            mountain.set("Climb Which Mountain?")
            tool.set("Bring What Tool?")
            sherpa_food.set("Sherpa OR Food?")
            month.set("Climb What Season?")

        Button(self, text="CLIMB!", command = lambda: [check_fields(), reset()], font='Helvetica 25 bold italic', border=10, fg='purple', bg='grey', height=1, width=10).pack(pady=25)
        Button(self, text="RESET", command = lambda: reset(), font='Helvetica 10 bold italic', border=7, fg='black', bg='yellow', height=1, width=10).pack()


class LivePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg = 'white')
        
        Label(self, text = "You Lived!", bg = 'white', fg = 'green', font =("Comic Sans MS", 45, BOLD)).pack()
        Button(self, text='Play Again', border=10, font =("Comic Sans MS", 45, BOLD), command = lambda: controller.show_frame(GamePage) ).pack(pady=20)


class DeadPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg = 'red')

        Label(self, text = "You Died!", bg = 'white', fg = 'green', font =("Comic Sans MS", 45, BOLD)).pack()
        Button(self, text='Play Again', border=10, font =("Comic Sans MS", 45, BOLD), command = lambda: controller.show_frame(GamePage)).pack(padx=20)


class MountainTable:
    def __init__(self):
        style = ttk.Style()
        style.configure('Treeview.Heading', foreground = 'red', font = ('Calibri', 13,'bold',UNDERLINE))

        tree = ttk.Treeview(column=("Mountain", "Elevation (ft)", "Total Climbs", "Climb Sucess Rate"), show='headings', height=10)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Mountain")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Elevation (ft)")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Total Climbs")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="Climb Sucess Rate")

        for mountain in mtnData:
            tree.insert('', 'end', text="1", values=(mountain, mtnData[mountain][0], self.total_climbs(mountain), self.sucess_rate(mountain)))
        tree.pack()
    
    def total_climbs(self, mountain):
        return mtnData[mountain][1] + mtnData[mountain][2]
    def sucess_rate(self, mountain):
        return f'{(mtnData[mountain][1] / self.total_climbs(mountain)) * 100:.1f}%'
    

class Calculations:
    def __init__(self, mountain, tool, sherpa_food, month):
        self.mountain = mountain
        self.tool = tool
        self.sherpa_food = sherpa_food
        self.month = month

    def mountain_rate(self):
        return float(MountainTable().sucess_rate(self.mountain).replace('%','')) / 100 
    
    def tool_rate(self):
        if self.tool == 'Ice Axe' or self.tool == 'Crampons':
            return .15
        elif self.tool == 'Goretex Jacket':
            return .05
        elif self.tool == 'Extreme Tent':
            return .2
        else:
            return .3
        
    def sherpa_or_food(self):
        return .4 if self.sherpa_food == "Hire Sherpa" else .1
    
    def month_rate(self):
        if self.month == 'December' or self.month == 'January' or self.month == 'February':
            return .05
        elif self.month == 'November' or self.month == 'March':
            return .1
        elif self.month == 'October' or self.month == 'April':
            return .15
        elif self.month == 'May' or self.month == 'September':
            return .2
        else:
            return .22

    def total_rate(self):
        return self.mountain_rate() + ((self.tool_rate() + self.sherpa_or_food()) * self.month_rate())
    

app = MtnClimberApp()
app.mainloop()





