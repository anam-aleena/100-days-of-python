"""
Day 1: Personal Finance Tracker
A simple CLI app to track income and expenses with file persistence.
"""

import json
import os
from datetime import datetime

DATA_FILE = "finances.json"

class FinanceTracker:
    def __init__(self):
        self.transactions = []
        self.load_data()
    
    def load_data(self):
        """Load transactions from JSON file if it exists"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    self.transactions = json.load(f)
                print(f"✅ Loaded {len(self.transactions)} transactions from file.")
            except Exception as e:
                print(f"❌ Error loading data: {e}")
                self.transactions = []
        else:
            print("📁 No existing data file found. Starting fresh.")
    
    def save_data(self):
        """Save transactions to JSON file"""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.transactions, f, indent=2)
            print("💾 Data saved successfully!")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def add_transaction(self):
        """Add a new transaction (income or expense)"""
        print("\n➕ Add New Transaction")
        
        # Get transaction details
        description = input("Description: ").strip()
        
        while True:
            try:
                amount = float(input("Amount: $"))
                break
            except ValueError:
                print("Please enter a valid number.")
        
        print("\nType:")
        print("1. Income (+)")
        print("2. Expense (-)")
        
        while True:
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                transaction_type = "income"
                break
            elif choice == '2':
                transaction_type = "expense"
                amount = -amount  # Make expense negative
                break
            else:
                print("Invalid choice. Try again.")
        
        # Create transaction dictionary
        transaction = {
            "id": len(self.transactions) + 1,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description,
            "amount": amount,
            "type": transaction_type
        }
        
        self.transactions.append(transaction)
        print(f"✅ Transaction added successfully!")
        
        # Auto-save
        self.save_data()
    
    def show_transactions(self):
        """Display all transactions in a formatted table"""
        if not self.transactions:
            print("\n📭 No transactions found.")
            return
        
        print("\n" + "="*60)
        print(f"{'ID':<4} {'Date':<20} {'Description':<25} {'Amount':>10}")
        print("="*60)
        
        for t in self.transactions:
            # Format amount with color (green for income, red for expense)
            amount = f"${t['amount']:.2f}"
            if t['amount'] >= 0:
                amount = f"\033[92m{amount}\033[0m"  # Green
            else:
                amount = f"\033[91m{amount}\033[0m"  # Red
            
            print(f"{t['id']:<4} {t['date'][:19]:<20} {t['description'][:23]:<25} {amount:>10}")
        
        print("="*60)
    
    def show_summary(self):
        """Show financial summary"""
        if not self.transactions:
            print("\n📊 No transactions to summarize.")
            return
        
        total_income = sum(t['amount'] for t in self.transactions if t['amount'] > 0)
        total_expenses = abs(sum(t['amount'] for t in self.transactions if t['amount'] < 0))
        balance = total_income - total_expenses
        
        print("\n" + "="*40)
        print("📊 FINANCIAL SUMMARY")
        print("="*40)
        print(f"Total Income:    ${total_income:.2f}")
        print(f"Total Expenses:  ${total_expenses:.2f}")
        print(f"Balance:         ${balance:.2f}")
        print("="*40)
        
        # Financial health indicator
        if balance > 0:
            print("💰 Financial Status: Positive Balance")
        elif balance == 0:
            print("⚖️  Financial Status: Break Even")
        else:
            print("⚠️  Financial Status: Negative Balance")
    
    def export_to_csv(self):
        """Export transactions to CSV file"""
        if not self.transactions:
            print("No transactions to export.")
            return
        
        try:
            filename = f"finances_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'w') as f:
                f.write("ID,Date,Description,Amount,Type\n")
                for t in self.transactions:
                    f.write(f"{t['id']},{t['date']},{t['description']},{t['amount']},{t['type']}\n")
            print(f"📤 Data exported to '{filename}'")
        except Exception as e:
            print(f"❌ Export failed: {e}")

def main():
    """Main program loop"""
    tracker = FinanceTracker()
    
    while True:
        print("\n" + "="*50)
        print("💰 PERSONAL FINANCE TRACKER")
        print("="*50)
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Financial Summary")
        print("4. Export to CSV")
        print("5. Save Data")
        print("6. Exit")
        print("="*50)
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            tracker.add_transaction()
        elif choice == '2':
            tracker.show_transactions()
        elif choice == '3':
            tracker.show_summary()
        elif choice == '4':
            tracker.export_to_csv()
        elif choice == '5':
            tracker.save_data()
        elif choice == '6':
            tracker.save_data()
            print("\n👋 Thank you for using Finance Tracker!")
            print("Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    # ASCII Art Banner
    print("""
    ╔══════════════════════════════════════════╗
    ║     PERSONAL FINANCE TRACKER v1.0        ║
    ║        #100DaysOfPython - Day 1          ║
    ╚══════════════════════════════════════════╝
    """)
    main()