import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from ui_styles import configure_styles, CATEGORIES, Colors
import numpy as np


class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = Colors.TEXT_SECONDARY
        self.default_fg_color = Colors.TEXT
        
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        self._add_placeholder()

    def _clear_placeholder(self, e=None):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.configure(foreground=self.default_fg_color)

    def _add_placeholder(self, e=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.configure(foreground=self.placeholder_color)

    def get(self):
        value = super().get()
        if value == self.placeholder:
            return ""
        return value


class Transaction:
    """Represents a financial transaction."""
    def __init__(self, amount, category, description="", note="", date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.note = note
        self.date = date if date else datetime.now()


class Budget:
    """Manages a collection of transactions."""
    def __init__(self, data_file="transactions.csv"):
        self.transactions = []
        self.data_file = data_file
        self.load_transactions()

    def load_transactions(self):
        """Loads transactions from CSV file if it exists."""
        if os.path.exists(self.data_file):
            df = pd.read_csv(self.data_file)
            for _, row in df.iterrows():
                date = datetime.strptime(row['Date'], "%Y-%m-%d")
                transaction = Transaction(
                    amount=float(row['Amount']),
                    category=row['Category'],
                    description=row['Description'],
                    note=row['Note'],
                    date=date
                )
                self.transactions.append(transaction)

    def add_transaction(self, transaction):
        """Adds a transaction and saves to CSV."""
        self.transactions.append(transaction)
        self.save_transactions()

    def save_transactions(self):
        """Saves all transactions to CSV file."""
        data = {
            "Date": [t.date.strftime("%Y-%m-%d") for t in self.transactions],
            "Category": [t.category for t in self.transactions],
            "Amount": [t.amount for t in self.transactions],
            "Description": [t.description for t in self.transactions],
            "Note": [t.note for t in self.transactions],
        }
        df = pd.DataFrame(data)
        df.to_csv(self.data_file, index=False)

    def get_summary(self):
        """Summarizes the transactions by category."""
        summary = {}
        for transaction in self.transactions:
            summary[transaction.category] = summary.get(transaction.category, 0) + transaction.amount
        return summary

    def export_to_csv(self):
        """Exports transactions to a user-selected CSV file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Transactions"
        )
        if filename:  # If user didn't cancel the dialog
            data = {
                "Date": [t.date.strftime("%Y-%m-%d") for t in self.transactions],
                "Category": [t.category for t in self.transactions],
                "Amount": [t.amount for t in self.transactions],
                "Description": [t.description for t in self.transactions],
                "Note": [t.note for t in self.transactions],
            }
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            messagebox.showinfo("Success", f"Transactions exported to {filename}")


class FinancialTracker:
    """Main application for managing financial transactions."""
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tracker")
        self.root.geometry("400x700")  # Narrower width, taller height for mobile format
        self.root.configure(bg=Colors.BACKGROUND)
        
        # Configure styles
        self.style = ttk.Style()
        configure_styles(self.style)
        
        self.transactions_file = "transactions.csv"
        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # Reduced padding

        # Header
        ttk.Label(
            main_frame, 
            text="Financial Tracker",
            style="Header.TLabel"
        ).pack(anchor=tk.W, pady=(0, 20))  # Reduced bottom padding

        # Amount with Keypad
        ttk.Label(main_frame, text="Amount", style="Label.TLabel").pack(anchor=tk.W)
        self.amount_entry = PlaceholderEntry(
            main_frame,
            placeholder="Enter amount",
            style="Input.TEntry"
        )
        self.amount_entry.pack(fill=tk.X, pady=(5, 10))

        # Keypad - make it more compact
        keypad_frame = ttk.Frame(main_frame, style="Main.TFrame")
        keypad_frame.pack(pady=5)
        self.create_keypad(keypad_frame)

        # Category
        ttk.Label(main_frame, text="Category", style="Label.TLabel").pack(anchor=tk.W, pady=(10, 0))
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=CATEGORIES,
            state="readonly"
        )
        self.category_combobox.set("Select category")
        self.category_combobox.pack(fill=tk.X, pady=(5, 15))

        # Description
        ttk.Label(main_frame, text="Description", style="Label.TLabel").pack(anchor=tk.W)
        self.description_entry = PlaceholderEntry(
            main_frame,
            placeholder="Enter description",
            style="Input.TEntry"
        )
        self.description_entry.pack(fill=tk.X, pady=(5, 15))

        # Date
        ttk.Label(main_frame, text="Date", style="Label.TLabel").pack(anchor=tk.W)
        self.date_entry = DateEntry(
            main_frame,
            width=30,
            background=Colors.PRIMARY,
            foreground=Colors.BACKGROUND,
            borderwidth=0,
            date_pattern='mm/dd/yyyy'
        )
        self.date_entry.pack(fill=tk.X, pady=(5, 20))

        # Buttons container frame
        buttons_container = ttk.Frame(main_frame, style="Main.TFrame")
        buttons_container.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))

        # Report buttons frame
        report_frame = ttk.Frame(buttons_container, style="Main.TFrame")
        report_frame.pack(fill=tk.X, pady=(0, 10))
        
        # View Report button
        ttk.Button(
            report_frame,
            text="View Report",
            style="Secondary.TButton",
            command=self.show_spending_chart,
            width=15  # Slightly narrower
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Monthly Trends button
        ttk.Button(
            report_frame,
            text="Monthly Trends",
            style="Secondary.TButton",
            command=self.show_monthly_trends_chart,
            width=15  # Slightly narrower
        ).pack(side=tk.RIGHT, padx=(5, 0))

        # Action buttons frame
        action_frame = ttk.Frame(buttons_container, style="Main.TFrame")
        action_frame.pack(fill=tk.X)
        
        # Export CSV button
        ttk.Button(
            action_frame,
            text="Export CSV",
            style="Secondary.TButton",
            command=self.export_transactions,
            width=15  # Slightly narrower
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Add Transaction button
        ttk.Button(
            action_frame,
            text="Add Transaction",
            style="Secondary.TButton",
            command=self.save_transaction,
            width=15  # Slightly narrower
        ).pack(side=tk.RIGHT, padx=(5, 0))

    def create_keypad(self, parent):
        keys = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['0', '.', 'Del']]
        for i, row in enumerate(keys):
            for j, key in enumerate(row):
                btn = ttk.Button(
                    parent,
                    text=key,
                    style="Secondary.TButton",
                    command=lambda k=key: self.on_keypad_press(k),
                    width=3  # Make keypad buttons smaller
                )
                btn.grid(row=i, column=j, padx=1, pady=1)  # Reduced padding

    def on_keypad_press(self, key):
        if key == 'Del':
            current = self.amount_entry.get()
            if current and current != self.amount_entry.placeholder:
                self.amount_entry.delete(len(current) - 1, tk.END)
        else:
            if self.amount_entry.get() == self.amount_entry.placeholder:
                self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(tk.END, key)

    def save_transaction(self):
        try:
            # Get values and validate
            amount = self.amount_entry.get()
            if amount == "Enter amount" or not amount:
                raise ValueError("Please enter an amount")
            amount = float(amount)
            
            category = self.category_var.get()
            if category == "Select category":
                raise ValueError("Please select a category")
            
            description = self.description_entry.get()
            if description == "Enter description":
                description = ""
                
            date = self.date_entry.get_date().strftime("%Y-%m-%d")

            if amount <= 0:
                raise ValueError("Amount must be positive")

            # Create new data
            new_transaction = pd.DataFrame({
                'Date': [date],
                'Amount': [amount],
                'Category': [category],
                'Description': [description]
            })

            # If file exists, append; if not, create new
            if os.path.exists(self.transactions_file):
                new_transaction.to_csv(self.transactions_file, mode='a', header=False, index=False)
            else:
                new_transaction.to_csv(self.transactions_file, index=False)
            
            # Reload transactions
            self.load_transactions()
            
            # Clear entries
            self.clear_entries()
            
            messagebox.showinfo("Success", "Transaction saved successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transaction: {str(e)}")

    def clear_entries(self):
        """Clear all input fields"""
        self.amount_entry.delete(0, tk.END)
        self.amount_entry._add_placeholder()
        
        self.category_combobox.set("Select category")
        
        self.description_entry.delete(0, tk.END)
        self.description_entry._add_placeholder()
        
        # Reset date to current date
        self.date_entry.set_date(datetime.now())

    def load_transactions(self):
        """Load transactions and ensure proper data types"""
        try:
            if os.path.exists(self.transactions_file):
                self.transactions = pd.read_csv(self.transactions_file)
                
                # Convert Date to datetime
                self.transactions['Date'] = pd.to_datetime(self.transactions['Date'])
                
                # Ensure Amount is numeric
                self.transactions['Amount'] = pd.to_numeric(self.transactions['Amount'], errors='coerce')
                
                # Fill NaN values in Description
                self.transactions['Description'] = self.transactions['Description'].fillna('')
                
                # Drop rows with NaN in critical columns
                self.transactions = self.transactions.dropna(subset=['Date', 'Amount', 'Category'])
            else:
                self.transactions = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load transactions: {str(e)}")
            self.transactions = pd.DataFrame(columns=['Date', 'Amount', 'Category', 'Description'])

    def export_transactions(self):
        """Export transactions to a new CSV file"""
        if not os.path.exists(self.transactions_file) or self.transactions.empty:
            messagebox.showerror("Error", "No transactions to export")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Export Transactions"
            )
            if filename:
                self.transactions.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Transactions exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def show_spending_chart(self):
        """Show spending chart with error handling"""
        if self.transactions.empty:
            messagebox.showerror("Error", "No transactions recorded")
            return
            
        try:
            # Calculate category totals
            category_totals = self.transactions.groupby('Category')['Amount'].sum()
            
            if category_totals.empty or category_totals.isna().all():
                messagebox.showerror("Error", "No valid data to plot")
                return
                
            category_totals = category_totals.sort_values(ascending=False)
            
            # Create figure with larger size and better resolution
            plt.close('all')  # Close any existing plots
            plt.figure(figsize=(10, 6), dpi=100)
            ax = plt.gca()
            
            # Create bars with better colors
            bars = ax.bar(
                range(len(category_totals)),
                category_totals.values,
                color='#2563eb',
                alpha=0.7
            )
            
            # Customize the chart
            plt.title("Spending by Category", pad=20, fontsize=14, fontweight='bold')
            plt.xlabel("Categories", labelpad=10, fontsize=12)
            plt.ylabel("Amount (BDT)", labelpad=10, fontsize=12)
            
            # Set x-axis labels
            plt.xticks(
                range(len(category_totals)),
                category_totals.index,
                rotation=45,
                ha='right'
            )
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'BDT {height:,.2f}',
                    ha='center',
                    va='bottom',
                    fontsize=10
                )
            
            # Add grid for better readability
            ax.grid(True, axis='y', linestyle='--', alpha=0.3)
            
            # Adjust layout
            plt.tight_layout()
            
            self.show_chart_window(plt.gcf(), "Spending by Category")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart: {str(e)}")
            plt.close('all')

    def show_monthly_trends_chart(self):
        """Show monthly trends chart with error handling"""
        if self.transactions.empty:
            messagebox.showerror("Error", "No transactions recorded")
            return
            
        try:
            plt.close('all')  # Close any existing plots
            
            # Create figure with better size ratio
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), height_ratios=[1, 1.5])
            fig.suptitle("Monthly Financial Analysis", fontsize=16, fontweight='bold', y=0.95)
            
            # Monthly total spending trend
            monthly_totals = self.transactions.groupby(
                self.transactions['Date'].dt.strftime('%Y-%m')
            )['Amount'].sum()
            
            if monthly_totals.empty or monthly_totals.isna().all():
                messagebox.showerror("Error", "No valid monthly data to plot")
                plt.close('all')
                return
            
            # Plot line chart for monthly totals
            ax1.plot(
                range(len(monthly_totals)),
                monthly_totals.values,
                marker='o',
                linewidth=2,
                color='#2563eb'
            )
            
            # Customize first subplot
            ax1.set_title("Monthly Spending Trend", pad=20, fontsize=12)
            ax1.set_xlabel("Month", labelpad=10)
            ax1.set_ylabel("Total Amount (BDT)", labelpad=10)
            ax1.grid(True, linestyle='--', alpha=0.3)
            
            # Set x-axis labels for first subplot
            ax1.set_xticks(range(len(monthly_totals)))
            ax1.set_xticklabels(monthly_totals.index, rotation=45, ha='right')
            
            # Add value labels on points
            for i, v in enumerate(monthly_totals):
                ax1.text(i, v, f'BDT {v:,.2f}', ha='center', va='bottom')
            
            # Category-wise monthly breakdown
            monthly_category = self.transactions.pivot_table(
                index=self.transactions['Date'].dt.strftime('%Y-%m'),
                columns='Category',
                values='Amount',
                aggfunc='sum',
                fill_value=0
            )
            
            if not monthly_category.empty:
                monthly_category.plot(
                    kind='bar',
                    stacked=True,
                    ax=ax2,
                    width=0.8,
                    alpha=0.7
                )
                
                ax2.set_title("Monthly Category Breakdown", pad=20, fontsize=12)
                ax2.set_xlabel("Month", labelpad=10)
                ax2.set_ylabel("Amount (BDT)", labelpad=10)
                ax2.grid(True, axis='y', linestyle='--', alpha=0.3)
                ax2.legend(title="Categories", bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Adjust layout to prevent text cutoff
            plt.tight_layout()
            
            # Show in new window with specific size
            window = tk.Toplevel(self.root)
            window.title("Monthly Financial Analysis")
            window.geometry("1200x900")  # Larger window size
            
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create chart: {str(e)}")
            plt.close('all')

    def show_chart_window(self, fig, title):
        # Create a new window for the chart
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("1000x800")  # Larger window for better visibility
        
        # Create toolbar frame
        toolbar_frame = ttk.Frame(window)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add export button
        ttk.Button(
            toolbar_frame,
            text="Export Chart",
            style="Secondary.TButton",
            command=lambda: self.export_chart(fig)
        ).pack(side=tk.RIGHT)
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def export_chart(self, fig):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Export Chart"
        )
        if filename:
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Success", "Chart exported successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialTracker(root)
    root.mainloop()
