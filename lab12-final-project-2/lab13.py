import tkinter as tk
import sqlite3


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.current_value = tk.StringVar(value=31)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text='How many past days of data:')
        self.label.pack()

        self.spin_box = tk.Spinbox(
            self.master,
            from_=31,
            to=200,
            textvariable=self.current_value,
            wrap=True)
        self.spin_box.pack()

        self.fetch_button = tk.Button(self.master)
        self.fetch_button["text"] = "Fetch data"
        self.fetch_button["command"] = self.on_fetch_button
        self.fetch_button.pack()

        self.status_bar = StatusBar(self.master)
        self.status_bar.pack()

    def on_fetch_button(self):
        print(f"download {self.current_value.get()}")


class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.variable = tk.StringVar()
        self.label = tk.Label(self, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                              textvariable=self.variable,
                              font=('arial', 16, 'normal'))
        self.variable.set('Status Bar')
        self.label.pack(fill=tk.X, side=tk.BOTTOM)
        self.pack()


def initialize_db(cursor: sqlite3.Cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_index(
        close_date VARCHAR(255) PRIMARY KEY,
        usd_price FLOAT
        );
        """)

def run():
    gui = tk.Tk()
    gui.geometry("1200x600")

    app = Application(master=gui)
    app.master.title("BTC Price Analyzer")

    app.status_bar.variable.set("xd")

    app.mainloop()

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    initialize_db(cursor)

    conn.commit()


if __name__ == "__main__":
    run()
