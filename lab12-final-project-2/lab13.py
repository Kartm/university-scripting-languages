import tkinter as tk
import sqlite3
from datetime import date, timedelta

import matplotlib.pyplot as plt
import urllib.request, json

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Application(tk.Frame):
    def __init__(self, master, db_conn: sqlite3.Connection):
        super().__init__(master)
        self.master = master
        self.db_conn = db_conn
        # self.pack()

        self.current_value = tk.StringVar(value=31)

        self.create_widgets()

    def create_widgets(self):


        self.textWidget2 = tk.Text(self.master)
        self.textWidget2.insert(tk.END, "Aggregation")
        self.textWidget2.configure(state='disabled')
        self.textWidget2.grid(row=0, column=1, sticky="nw")

        self.status_bar = StatusBar(self.master)

        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.title('My chart')

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)

        ax1.plot([1, 2, 3])
        ax1.set_title('BTC Price')

        bar1 = FigureCanvasTkAgg(figure1, self.master)
        bar1.get_tk_widget().grid(row=0, column=0, sticky="ne")

        actions_frame = tk.Frame(self.master, borderwidth=1, bd=1, relief=tk.SOLID)
        actions_frame.grid(row=1, columnspan=2, column=0, sticky="we")

        self.fetch_button = tk.Button(actions_frame)
        self.fetch_button["text"] = "Fetch data"
        self.fetch_button["command"] = self.on_fetch_button
        self.fetch_button.grid(padx=(16, 16), pady=(16, 16), sticky="e")

        settings_frame = tk.Frame(actions_frame)

        self.label = tk.Label(settings_frame, text='How many past days of data:')
        self.label.grid(column=0, row=0)

        self.spin_box = tk.Spinbox(
            settings_frame,
            from_=31,
            to=200,
            textvariable=self.current_value,
            wrap=True)
        self.spin_box.grid(column=0, row=1)

        settings_frame.grid(column=0)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def on_fetch_button(self):
        past_days = int(self.current_value.get())

        self.status_bar.variable.set(f"Status: Downloading past {past_days} days data...")

        today = date.today()
        end = today.strftime("%Y-%m-%d")
        start = (today - timedelta(days=past_days)).strftime("%Y-%m-%d")

        url_params = f"?start={start}&end={end}"
        with urllib.request.urlopen(f"http://api.coindesk.com/v1/bpi/historical/close.json{url_params}") as url:
            data = json.loads(url.read().decode())
            self.status_bar.variable.set(f"Status: Downloading finished.")

            cursor = self.db_conn.cursor()

            data_to_insert = [(close_date, data['bpi'][close_date]) for close_date in data['bpi']]
            print(data_to_insert)

            cursor.executemany("""
            INSERT INTO prices VALUES(?, ?);
            """, data_to_insert)

            self.db_conn.commit()



class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=1)
        self.variable = tk.StringVar()
        self.label = tk.Label(self, bd=1, anchor=tk.W,
                              textvariable=self.variable,
                              font=('arial', 12, 'normal'), padx=8)
        self.variable.set('Status: Waiting for user action...')

        self.label.grid()
        self.grid(row=2, columnspan=2, sticky="we")


def run():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices(
                close_date VARCHAR(255) PRIMARY KEY,
                usd_price FLOAT
                );
                """)
    conn.commit()

    gui = tk.Tk()
    gui.geometry("1200x600")

    app = Application(master=gui, db_conn=conn)
    app.master.title("BTC Price Analyzer")

    app.mainloop()


if __name__ == "__main__":
    run()
