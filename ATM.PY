import threading
import tkinter as tk
from tkinter import messagebox, simpledialog

# Shared account balance (simulated as shared resource)
account_balance = 1000
users = {}
balance_lock = threading.Lock()

# ATM Functionality
def atm_task(task, amount, log_box, user):
    global account_balance

    if user not in users:
        log_box.insert(tk.END, "User does not exist.\n")
        return

    with balance_lock:
        if task == "Deposit":
            users[user] += amount
            log_box.insert(tk.END, f"{user} deposited {amount}. New balance: {users[user]}\n")

        elif task == "Withdraw":
            if users[user] >= amount:
                users[user] -= amount
                log_box.insert(tk.END, f"{user} withdrew {amount}. New balance: {users[user]}\n")
            else:
                log_box.insert(tk.END, f"{user} has insufficient funds for withdrawal.\n")

        elif task == "Check Balance":
            log_box.insert(tk.END, f"{user}'s balance: {users[user]}\n")

# Thread runner
def run_threads(num_threads, root):
    def open_thread_window(thread_id):
        thread_window = tk.Toplevel(root)
        thread_window.title(f"ATM Thread {thread_id}")

        log_box = tk.Text(thread_window, width=50, height=15)
        log_box.pack(pady=10)

        tk.Label(thread_window, text="Enter User Name:").pack()
        user_entry = tk.Entry(thread_window)
        user_entry.pack(pady=5)

        tk.Label(thread_window, text="Enter Amount:").pack()
        amount_entry = tk.Entry(thread_window)
        amount_entry.pack(pady=5)

        for task in ["Deposit", "Withdraw", "Check Balance"]:
            tk.Button(
                thread_window,
                text=task,
                command=lambda t=task: atm_task(t, float(amount_entry.get()) if t != "Check Balance" else 0, log_box, user_entry.get())
            ).pack(pady=5)

    for i in range(1, num_threads + 1):
        open_thread_window(i)

# GUI implementation
def create_gui():
    def start_simulation():
        try:
            num_threads = int(entry_threads.get())
            if num_threads <= 0:
                raise ValueError("Number of threads must be positive.")

            run_threads(num_threads, root)
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def create_user():
        user_name = simpledialog.askstring("Create User", "Enter user name:")
        if not user_name:
            messagebox.showerror("Error", "User name cannot be empty.")
            return

        initial_balance = simpledialog.askfloat("Create User", "Enter initial balance:")
        if initial_balance is None or initial_balance < 0:
            messagebox.showerror("Error", "Invalid initial balance.")
            return

        if user_name in users:
            messagebox.showerror("Error", "User already exists.")
            return

        users[user_name] = initial_balance
        messagebox.showinfo("Success", f"User {user_name} created with balance {initial_balance}.")

    # Root window
    root = tk.Tk()
    root.title("ATM Simulator")

    # Input for number of threads
    tk.Label(root, text="Enter number of threads (ATMs):").pack(pady=5)
    entry_threads = tk.Entry(root)
    entry_threads.pack(pady=5)

    # Create user button
    tk.Button(root, text="Create User", command=create_user).pack(pady=10)

    # Start simulation button
    tk.Button(root, text="Start Simulation", command=start_simulation).pack(pady=10)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()