import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import plotly.express as px
import csv

# --- Matplotlib Styling ---
plt.style.use('ggplot')

class GamingScoreAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Gaming Score Data Analyzer")
        self.root.geometry("1300x850")
        self.root.configure(bg='#2c3e50')

        # --- Data Attributes ---
        self.players = []
        self.scores = np.array([])
        self.total_scores = np.array([])
        self.headers = []

        # --- Setup ---
        self._apply_styles()
        self.setup_gui()

    # ---------------- STYLING -----------------
    def _apply_styles(self):
        """Applies Ttk styles for a modern, consistent look."""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook Style (Tabs)
        style.configure('TNotebook', background='#2c3e50', borderwidth=0)
        style.configure('TNotebook.Tab', background='#34495e', foreground='white', padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#1abc9c'), ('active', '#4a6b82')], foreground=[('selected', 'black')])

        # Frame Style
        style.configure('TFrame', background='#2c3e50')

    # ---------------- GUI SETUP -----------------
    def setup_gui(self):
        # --- Header ---
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text="🎯 GAMING SCORE DATA ANALYZER",
                 font=('Arial', 22, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(5, 0))
        tk.Label(header_frame, text="Performance Evaluation and Visualization System",
                 font=('Arial', 12), fg='#bdc3c7', bg='#34495e').pack()

        # --- Control Frame ---
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(fill='x', padx=10, pady=10)
        btn_style = {'font': ('Arial', 10, 'bold'), 'bg': '#3498db', 'fg': 'white', 'padx': 15, 'pady': 8, 'relief': 'flat', 'activebackground': '#2980b9'}

        tk.Button(control_frame, text="📁 Load CSV", command=self.load_csv, **btn_style).pack(side='left', padx=5)
        tk.Button(control_frame, text="📈 Show Analysis", command=lambda: self.notebook.select(self.analysis_frame), **btn_style).pack(side='left', padx=5)
        tk.Button(control_frame, text="🏆 Leaderboard", command=self.show_leaderboard, **btn_style).pack(side='left', padx=5)

        tk.Button(control_frame, text="🔥 Seaborn Heatmap (Window)", command=self.show_seaborn, **btn_style).pack(side='left', padx=5)
        # Button for Plotly
        tk.Button(control_frame, text="🌈 Plotly Graphs (Browser)", command=self.show_plotly, **btn_style).pack(side='left', padx=5)


        # --- Notebook Tabs ---
        self.notebook = ttk.Notebook(self.root, style='TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.dashboard_frame = tk.Frame(self.notebook, bg='#2c3e50')
        self.analysis_frame = tk.Frame(self.notebook, bg='#2c3e50')
        self.add_score_frame = tk.Frame(self.notebook, bg='#2c3e50')

        self.notebook.add(self.dashboard_frame, text="📊 Dashboard")
        self.notebook.add(self.analysis_frame, text="📈 Analysis Charts")
        self.notebook.add(self.add_score_frame, text="➕ Add Scores")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self.create_add_score_section()
        self.load_sample_data()

    def _on_tab_change(self, event):
        """Triggers chart rendering when switching to the Analysis tab."""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "📈 Analysis Charts":
            self.show_analysis()

    # ---------------- ADD SCORE SECTION -----------------
    def create_add_score_section(self):
        tk.Label(self.add_score_frame, text="➕ Add or Update Player Scores",
                 font=('Arial', 18, 'bold'), fg='#f1c40f', bg='#2c3e50').pack(pady=20)

        form = tk.Frame(self.add_score_frame, bg='#34495e')
        form.pack(pady=20, padx=20)

        tk.Label(form, text="Player Name:", bg='#34495e', fg='white', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.player_name = tk.Entry(form, font=('Arial', 12))
        self.player_name.grid(row=0, column=1, padx=10, pady=10)

        self.score_entries = []
        for i in range(5):
            tk.Label(form, text=f"Game {i+1} Score:", bg='#34495e', fg='white', font=('Arial', 12)).grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
            e = tk.Entry(form, font=('Arial', 12))
            e.grid(row=i+1, column=1, padx=10, pady=10)
            self.score_entries.append(e)

        tk.Button(self.add_score_frame, text="💾 Add / Update Score", bg="#27ae60", fg="white",
                  font=('Arial', 12, 'bold'), command=self.add_score, relief='flat', activebackground='#2ecc71').pack(pady=20)


    # ---------------- DATA HANDLING & CALCULATIONS -----------------
    def load_sample_data(self):
        """Creates and processes a sample CSV for initial data loading."""
        sample_data = [
            ["Player", "Game1", "Game2", "Game3", "Game4", "Game5"],
            ["Player1", 85, 90, 78, 92, 88],
            ["Player2", 92, 88, 95, 85, 90],
            ["Player3", 78, 85, 80, 88, 82],
            ["Player4", 88, 92, 85, 90, 87]
        ]
        with open("sample_scores.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        self.process_data("sample_scores.csv")

    def load_csv(self):
        """Opens a file dialog to load user CSV."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.process_data(file_path)
            messagebox.showinfo("Success", "CSV Loaded Successfully!")
            self.update_dashboard()

    def process_data(self, file_path):
        """Reads CSV data and updates internal arrays."""
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            self.headers = next(reader)
            data = list(reader)

        self.players = [row[0] for row in data]
        try:
             self.scores = np.array([[int(x) for x in row[1:]] for row in data])
        except ValueError as e:
            messagebox.showerror("Data Error", f"Error converting scores to numbers: {e}. Check your CSV data.")
            self.scores = np.array([])
            self.players = []
            self.headers = []
            return

        self.calculate_stats()
        self.update_dashboard()

    def calculate_stats(self):
        """Calculates total scores, averages, ranks, etc."""
        if self.scores.size == 0:
            self.total_scores = self.average_scores = self.highest_scores = self.lowest_scores = np.array([])
            self.ranked_players = self.ranked_scores = np.array([])
            return

        self.total_scores = np.sum(self.scores, axis=1)
        self.average_scores = np.mean(self.scores, axis=1)
        self.highest_scores = np.max(self.scores, axis=1)
        self.lowest_scores = np.min(self.scores, axis=1)
        self.rank_indices = np.argsort(-self.total_scores)
        self.ranked_players = np.array(self.players)[self.rank_indices]
        self.ranked_scores = self.total_scores[self.rank_indices]

    def add_score(self):
        """Handles adding new players or updating existing scores."""
        player = self.player_name.get().strip()
        if not player:
            messagebox.showwarning("Warning", "Enter player name.")
            return

        try:
            new_scores = [int(e.get()) for e in self.score_entries]
        except ValueError:
            messagebox.showerror("Error", "Error: Enter valid numeric scores.")
            return

        if player in self.players:
            idx = self.players.index(player)
            if len(new_scores) == self.scores.shape[1]:
                 self.scores[idx] = new_scores
            else:
                 messagebox.showerror("Error", "Score count must match existing games.")
                 return
        else:
            self.players.append(player)
            if self.scores.size == 0:
                self.scores = np.array([new_scores])
            else:
                self.scores = np.vstack([self.scores, new_scores])

        self.calculate_stats()
        self.update_dashboard()
        self.player_name.delete(0, tk.END)
        for entry in self.score_entries:
            entry.delete(0, tk.END)

        messagebox.showinfo("Success", f"Scores updated for {player}!")

    # ---------------- DASHBOARD & LEADERBOARD -----------------
    def update_dashboard(self):
        """Updates the summary panel with key statistics."""
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()

        tk.Label(self.dashboard_frame, text="🏠 Dashboard Summary",
                 font=('Arial', 18, 'bold'), fg='#1abc9c', bg='#2c3e50').pack(pady=20)

        if len(self.players) == 0:
            tk.Label(self.dashboard_frame, text="No data loaded yet!", font=('Arial', 12),
                     fg='white', bg='#2c3e50').pack()
            return

        text = f"""
Total Players: {len(self.players)}
Average Score (Overall): {np.mean(self.average_scores):.2f}
Highest Score Overall: {np.max(self.highest_scores)}
Lowest Score Overall: {np.min(self.lowest_scores)}
Top Player: {self.ranked_players[0]} ({self.ranked_scores[0]} pts)
        """
        tk.Label(self.dashboard_frame, text=text, font=('Consolas', 14),
                 fg='#ecf0f1', bg='#2c3e50', justify='left', relief='solid', bd=1, padx=20, pady=10).pack(pady=10)

    def show_leaderboard(self):
        """Displays the ranked list of players in a message box."""
        if len(self.players) == 0:
            messagebox.showwarning("Warning", "Load or add data first!")
            return

        message = "🏆 Leaderboard:\n\n"
        for i, (p, s) in enumerate(zip(self.ranked_players, self.ranked_scores), 1):
            message += f"{i}. {p} — {s} pts\n"
        messagebox.showinfo("Leaderboard", message)

    # ---------------- MATPLOTLIB CHARTS -----------------
    def _create_matplotlib_chart(self, master, fig, title, row, col):
        """Helper to embed a single matplotlib figure into a grid."""
        frame = tk.Frame(master, bg='#34495e', bd=2, relief='groove')
        frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        tk.Label(frame, text=title, font=('Arial', 14, 'bold'), fg='#f1c40f', bg='#34495e').pack(pady=5)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)

        plt.close(fig)

    def show_analysis(self):
        """Generates and displays 4 Matplotlib charts in the Analysis tab grid."""
        if self.scores.size == 0 or len(self.players) == 0:
            for widget in self.analysis_frame.winfo_children():
                widget.destroy()
            tk.Label(self.analysis_frame, text="⚠️ Load or add data first to view charts.", font=('Arial', 14),
                     fg='#e74c3c', bg='#2c3e50').pack(pady=50)
            return

        for widget in self.analysis_frame.winfo_children():
            widget.destroy()

        self.analysis_frame.grid_columnconfigure((0, 1), weight=1)
        self.analysis_frame.grid_rowconfigure((0, 1), weight=1)

        # --- Chart 1: Bar Chart (Total Scores) ---
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.bar(self.players, self.total_scores, color='#3498db')
        ax1.set_title("Total Scores by Player", fontsize=10)
        ax1.set_ylabel("Total Score", fontsize=9)
        self._create_matplotlib_chart(self.analysis_frame, fig1, "Total Score Ranking", 0, 0)

        # --- Chart 2: Line Chart (Score Trends) ---
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        for i, player in enumerate(self.players):
            ax2.plot(range(1, self.scores.shape[1] + 1), self.scores[i], marker='o', label=player)
        ax2.set_title("Score Trends by Game", fontsize=10)
        ax2.set_xlabel("Game Number", fontsize=9)
        ax2.set_ylabel("Score", fontsize=9)
        ax2.legend(fontsize=7, loc='upper right')
        self._create_matplotlib_chart(self.analysis_frame, fig2, "Performance Trend Over Games", 0, 1)

        # --- Chart 3: Pie Chart (Contribution) ---
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        mask = self.total_scores > 0
        valid_scores = self.total_scores[mask]
        valid_players = np.array(self.players)[mask]

        if valid_scores.size > 0:
            ax3.pie(valid_scores, labels=valid_players, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax3.set_title("Score Contribution by Player", fontsize=10)
        self._create_matplotlib_chart(self.analysis_frame, fig3, "Total Contribution Share", 1, 0)

        # --- Chart 4: Box Plot (Score variability) ---
        # This is the Matplotlib box plot that remains
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        data_to_plot = [self.scores[:, i] for i in range(self.scores.shape[1])]
        ax4.boxplot(data_to_plot, patch_artist=True, labels=self.headers[1:])
        ax4.set_title("Score Distribution per Game (Box Plot)", fontsize=10)
        ax4.set_ylabel("Score Range", fontsize=9)
        self._create_matplotlib_chart(self.analysis_frame, fig4, "Game Score Variability", 1, 1)


    # ---------------- SEABORN HEATMAP -----------------
    def show_seaborn(self):
        """Creates and displays a Seaborn heatmap in a standard Matplotlib window."""
        if self.scores.size == 0:
            messagebox.showwarning("Warning", "Load or add data first!")
            return

        plt.figure(figsize=(7, 5))

        sns.heatmap(self.scores, annot=True, fmt='d', cmap='coolwarm', linewidths=.5, linecolor='black',
                    xticklabels=self.headers[1:], yticklabels=self.players)

        plt.title("🔥 Player Performance per Game (Heatmap)", fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show() # Use plt.show() to open in a standard, separate window

    # ---------------- PLOTLY GRAPHS (Bar, Scatter, 3D Scatter) -----------------
    def show_plotly(self):
        """Creates 3 Plotly charts (Bar, Scatter, 3D Scatter) and displays them interactively in a web browser."""
        if self.scores.size == 0 or len(self.players) == 0:
            messagebox.showwarning("Warning", "Load or add data first!")
            return

        game_labels = self.headers[1:] if self.headers else [f"Game{i+1}" for i in range(self.scores.shape[1])]

        # Prepare data in 'long' format using pure Python lists of dictionaries
        melted_data = []
        for i, player in enumerate(self.players):
             for j, game in enumerate(game_labels):
                 if j < self.scores.shape[1]:
                    melted_data.append({
                        "Player": player,
                        "Game": game,
                        "Game Index": j + 1, # Used for a 3rd dimension axis
                        "Score": int(self.scores[i][j]),
                        "Total Score": int(self.total_scores[i])
                    })

        # Get unique player/total score pairs for the bar chart
        unique_scores = []
        seen_players = set()
        for d in melted_data:
            if d['Player'] not in seen_players:
                unique_scores.append(d)
                seen_players.add(d['Player'])


        # --- 1. Plotly Bar Chart (Total Scores) ---
        fig1 = px.bar(
            unique_scores,
            x='Player',
            y='Total Score',
            title='1. Player Total Scores (Interactive Bar Chart)',
            color='Total Score',
            template='plotly_white'
        )
        fig1.update_traces(textposition='outside')

        # --- 2. Plotly 2D Scatter Plot (Score vs Game) ---
        fig2 = px.scatter(
            melted_data,
            x="Game",
            y="Score",
            color="Player",
            size="Score",
            title='2. Individual Score Trends Across Games (2D Scatter)',
            template='plotly_dark'
        )

        # --- 3. Plotly 3D Scatter Plot (Total Score vs Game Index vs Score) ---
        # This graph allows rotating and exploring the data in 3 dimensions
        fig3 = px.scatter_3d(
            melted_data,
            x="Total Score",
            y="Score",
            z="Game Index",
            color="Player",
            size="Score",
            title="3. 3D Player Performance: Total Score, Individual Score, and Game Index",
            template='plotly_dark'
        )
        fig3.update_layout(scene = dict(
                            xaxis_title='Player Total Score',
                            yaxis_title='Individual Game Score',
                            zaxis_title='Game Index (1-5)'))


        # Display all three figures (opens three separate tabs/windows)
        fig1.show()
        fig2.show()
        fig3.show()


# --- Run Application ---
if __name__ == "__main__":
    import webbrowser # Necessary for fig.show() to work

    root = tk.Tk()
    app = GamingScoreAnalyzer(root)
    root.mainloop()