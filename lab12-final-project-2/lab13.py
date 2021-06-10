import json
import sqlite3
import tkinter as tk
import urllib.request
from datetime import date, timedelta, datetime

import matplotlib.pyplot as plt
from matplotlib import dates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def confirmation_dialog_result(cursor: sqlite3.Cursor):
    cursor.execute("""
        SELECT count(*) FROM sqlite_master WHERE type='table' AND name='prices';
    """)

    cache_exists = cursor.fetchall()[0][0] == 1

    if cache_exists:
        answer = tk.messagebox.askyesno(
            message="This will override the cache. Continue?")

        if not answer:
            return False

    return True


class Application(tk.Frame):
    def __init__(self, master, db_conn: sqlite3.Connection):
        super().__init__(master)
        self.master = master
        self.db_conn = db_conn
        # self.pack()

        self.current_value = tk.StringVar(value=31)

        self.create_widgets()

    def create_widgets(self):
        self.stats = Stats(self.master)
        self.stats.grid(row=0, column=1, sticky=tk.NSEW)

        self.status_bar = StatusBar(self.master)

        self.plot = Plot(self.master)
        self.plot.grid(row=0, column=0, sticky=tk.NSEW)

        actions_frame = tk.Frame(self.master, borderwidth=1, bd=1, relief=tk.SOLID)
        actions_frame.grid(row=1, columnspan=2, column=0, sticky="we")

        self.fetch_button = tk.Button(actions_frame)
        self.fetch_button["text"] = "Fetch data"
        self.fetch_button["command"] = self.on_fetch_button

        self.clear_button = tk.Button(actions_frame)
        self.clear_button["text"] = "Clear cache"
        self.clear_button["command"] = self.on_clear_button

        settings_frame = tk.Frame(actions_frame)

        self.label = tk.Label(settings_frame, text='How many past days of data:')
        self.label.grid(column=0, row=0, sticky='w')

        self.spin_box = tk.Spinbox(
            settings_frame,
            from_=31,
            to=200,
            textvariable=self.current_value,
            wrap=True)
        self.spin_box.grid(column=0, row=1)

        self.fetch_button.grid(column=1, row=0, padx=(16, 16), pady=(16, 16), sticky="e")
        self.clear_button.grid(column=1, row=1, padx=(16, 16), pady=(16, 16), sticky="e")
        settings_frame.grid(column=0, row=0, rowspan=2, sticky="NESW")

        self.master.grid_columnconfigure(0, weight=1, uniform="group1")
        self.master.grid_columnconfigure(1, weight=1, uniform="group1")
        self.master.grid_rowconfigure(0, weight=1)

    def on_fetch_button(self):
        past_days = int(self.current_value.get())

        self.status_bar.variable.set(f"Status: Downloading past {past_days} days data...")

        cursor = self.db_conn.cursor()

        try:
            self.download_data(cursor, past_days)

            self.status_bar.variable.set(f"Status: Downloaded {past_days} past days.")

            self.plot.refresh(cursor)
            self.stats.refresh(cursor)
        except urllib.error.URLError as e:
            self.status_bar.variable.set(f"Status: Error.")
            tk.messagebox.showinfo(title="Error downloading data:", message=e)


    def on_clear_button(self):
        self.status_bar.variable.set(f"Status: Cleared the cache.")

        cursor = self.db_conn.cursor()
        cursor.execute("""
            DROP table IF EXISTS prices;
        """)

    def download_data(self, cursor: sqlite3.Cursor, past_days: int):
        today = date.today()
        end = today.strftime("%Y-%m-%d")
        start = (today - timedelta(days=past_days)).strftime("%Y-%m-%d")

        url_params = f"?start={start}&end={end}"

        if not confirmation_dialog_result(cursor):
            return


        with urllib.request.urlopen(f"http://api.coindesk.com/v1/bpi/historical/close.json{url_params}") as url:
            data = json.loads(url.read().decode())

            data_to_insert = [(close_date, data['bpi'][close_date]) for close_date in data['bpi']]

            cursor.execute("""
                DROP table IF EXISTS prices;
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prices(
                close_date VARCHAR(255) PRIMARY KEY,
                usd_price FLOAT
                );
            """)

            cursor.executemany("""
                INSERT INTO prices VALUES(?, ?);
            """, data_to_insert)

            self.db_conn.commit()


class Plot(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.fig = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)

        self.ax1.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m'))
        self.fig.autofmt_xdate()

        plt.gcf().autofmt_xdate()

        self.ax1.set_title('BTC Price')
        self.ax1.set_ylabel('Price in $')

        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.get_tk_widget().grid(row=0, column=0)

    def refresh(self, cursor: sqlite3.Cursor):
        cursor.execute("""
            SELECT
                close_date,
                usd_price
            FROM
                prices
        """)

        rows = cursor.fetchall()

        x_plot = [datetime.strptime(x[0], '%Y-%m-%d') for x in rows]
        y_plot = [x[1] for x in rows]

        self.ax1.plot(x_plot, y_plot)
        self.canvas.draw()


class Stats(tk.Frame):
    _header_text = "Basic statistics"

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.variable = tk.StringVar()
        self.label = tk.Label(self,
                              anchor="e", justify=tk.LEFT,
                              textvariable=self.variable,
                              font=('arial', 12, 'normal'), padx=8)
        self.label.grid()
        self.variable.set(f'{self._header_text}:\nn/a')

    def refresh(self, cursor: sqlite3.Cursor):
        cursor.execute("""
            SELECT
                round(min(usd_price), 2) lowest_price,
                round(max(usd_price), 2) highest_price,
                round(avg(usd_price), 2) avg_price
            FROM
                prices
        """)

        rows = cursor.fetchall()

        price_min = rows[0][0]
        price_max = rows[0][1]
        price_avg = rows[0][2]
        self.variable.set(f"{self._header_text}:"
                          f"\nLowest price: {price_min}$"
                          f"\nHighest price: {price_max}$"
                          f"\nAverage price: {price_avg}$")


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

    gui = tk.Tk()
    gui.geometry("1200x600")

    app = Application(master=gui, db_conn=conn)
    app.master.title("BTC Price Analyzer")

    app.mainloop()


if __name__ == "__main__":
    run()
