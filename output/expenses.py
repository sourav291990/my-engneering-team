import datetime
from typing import List, Dict, Tuple, Optional


class Expense:
    """
    Represents a single expense entry.
    """

    def __init__(self, amount: float, category: str, date: datetime.date, description: str = "") -> None:
        """
        Initializes a new Expense object.

        Args:
            amount (float): The amount of the expense.
            category (str): The category of the expense (e.g., "Food", "Transportation", "Entertainment").
            date (datetime.date): The date of the expense.
            description (str, optional): A brief description of the expense. Defaults to "".
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number.")
        if not isinstance(category, str):
            raise TypeError("Category must be a string.")
        if not isinstance(date, datetime.date):
            raise TypeError("Date must be a datetime.date object.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def __repr__(self) -> str:
        """
        Returns a string representation of the Expense object.
        """
        return f"Expense(amount={self.amount}, category='{self.category}', date={self.date.isoformat()}, description='{self.description}')"


class UserAccount:
    """
    Represents a user's account with their initial balance.
    """

    def __init__(self, initial_balance: float) -> None:
        """
        Initializes a new UserAccount object.

        Args:
            initial_balance (float): The initial balance of the user's account.
        """
        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Initial balance must be a number.")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")

        self.balance = initial_balance

    def update_balance(self, expense_amount: float) -> None:
        """
        Updates the user's balance after an expense.

        Args:
            expense_amount (float): The amount of the expense to deduct from the balance.
        """
        self.balance -= expense_amount

    def get_balance(self) -> float:
        """
        Returns the current balance of the user's account.

        Returns:
            float: The current balance.
        """
        return self.balance


class ExpenseManager:
    """
    Manages expenses for a user, including adding, updating, deleting, and viewing expenses.
    """

    def __init__(self, user_account: UserAccount) -> None:
        """
        Initializes a new ExpenseManager object.

        Args:
            user_account (UserAccount): The UserAccount object associated with this expense manager.
        """
        self.expenses: List[Expense] = []
        self.user_account = user_account

    def add_expense(self, amount: float, category: str, date: datetime.date, description: str = "") -> None:
        """
        Adds a new expense to the expense list.

        Args:
            amount (float): The amount of the expense.
            category (str): The category of the expense.
            date (datetime.date): The date of the expense.
            description (str, optional): A description of the expense. Defaults to "".

        Raises:
            ValueError: If the expense amount exceeds the available balance.
        """
        if amount > self.user_account.get_balance():
            raise ValueError("Expense amount exceeds available balance.")

        expense = Expense(amount, category, date, description)
        self.expenses.append(expense)
        self.user_account.update_balance(amount)

    def update_expense(self, index: int, amount: float, category: str, date: datetime.date, description: str = "") -> None:
        """
        Updates an existing expense in the expense list.

        Args:
            index (int): The index of the expense to update.
            amount (float): The new amount of the expense.
            category (str): The new category of the expense.
            date (datetime.date): The new date of the expense.
            description (str, optional): The new description of the expense. Defaults to "".

        Raises:
            IndexError: If the index is out of range.
            ValueError: If the expense amount exceeds the available balance after the update.
        """
        if not 0 <= index < len(self.expenses):
            raise IndexError("Invalid expense index.")

        original_expense = self.expenses[index]
        balance_increase = original_expense.amount
        available_balance = self.user_account.get_balance() + balance_increase

        if amount > available_balance:
             raise ValueError("Expense amount exceeds available balance after update.")

        self.user_account.update_balance(balance_increase)  # Revert the original expense from balance
        expense = Expense(amount, category, date, description)
        self.expenses[index] = expense
        self.user_account.update_balance(-amount)  # Deduct the new expense amount

    def delete_expense(self, index: int) -> None:
        """
        Deletes an expense from the expense list.

        Args:
            index (int): The index of the expense to delete.

        Raises:
            IndexError: If the index is out of range.
        """
        if not 0 <= index < len(self.expenses):
            raise IndexError("Invalid expense index.")

        expense = self.expenses[index]
        self.user_account.update_balance(expense.amount)  # Restore balance
        del self.expenses[index]

    def get_expenses_by_period(self, start_date: datetime.date, end_date: datetime.date) -> List[Expense]:
        """
        Returns a list of expenses within a given period.

        Args:
            start_date (datetime.date): The start date of the period.
            end_date (datetime.date): The end date of the period.

        Returns:
            List[Expense]: A list of Expense objects within the specified period.
        """
        return [expense for expense in self.expenses if start_date <= expense.date <= end_date]

    def calculate_total_expenses(self, start_date: datetime.date, end_date: datetime.date) -> float:
        """
        Calculates the total expenses within a given period.

        Args:
            start_date (datetime.date): The start date of the period.
            end_date (datetime.date): The end date of the period.

        Returns:
            float: The total expenses within the specified period.
        """
        expenses_in_period = self.get_expenses_by_period(start_date, end_date)
        return sum(expense.amount for expense in expenses_in_period)

    def get_remaining_balance(self) -> float:
        """
        Returns the remaining balance of the user's account.

        Returns:
            float: The remaining balance.
        """
        return self.user_account.get_balance()

    def get_expenses_by_category(self, start_date: datetime.date, end_date: datetime.date) -> Dict[str, float]:
        """
        Categorizes expenses and provides a breakdown of spending by category within a given period.

        Args:
            start_date (datetime.date): The start date of the period.
            end_date (datetime.date): The end date of the period.

        Returns:
            Dict[str, float]: A dictionary where keys are expense categories and values are the total expenses for that category.
        """
        expenses_in_period = self.get_expenses_by_period(start_date, end_date)
        category_totals: Dict[str, float] = {}
        for expense in expenses_in_period:
            category = expense.category
            amount = expense.amount
            category_totals[category] = category_totals.get(category, 0) + amount
        return category_totals

    def generate_report(self, period: str) -> Dict[str, Dict[str, float]]:
        """
        Generates a report summarizing expenses over weekly, monthly, or yearly periods.

        Args:
            period (str): The period for the report ("weekly", "monthly", or "yearly").

        Returns:
            Dict[str, Dict[str, float]]: A dictionary where keys are time periods (e.g., "Week 1", "January", "2023") and
            values are dictionaries containing the total expenses and category breakdowns for that period.
        """
        today = datetime.date.today()
        if period == "weekly":
            start_date = today - datetime.timedelta(days=today.weekday())
            end_date = start_date + datetime.timedelta(days=6)
            report_data = {
                "Weekly Report": {
                    "total_expenses": self.calculate_total_expenses(start_date, end_date),
                    "category_breakdown": self.get_expenses_by_category(start_date, end_date),
                }
            }
        elif period == "monthly":
            year = today.year
            month = today.month
            start_date = datetime.date(year, month, 1)
            next_month = month + 1 if month < 12 else 1
            next_year = year + 1 if month == 12 else year
            end_date = datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)

            report_data = {
                "Monthly Report": {
                    "total_expenses": self.calculate_total_expenses(start_date, end_date),
                    "category_breakdown": self.get_expenses_by_category(start_date, end_date),
                }
            }
        elif period == "yearly":
            year = today.year
            start_date = datetime.date(year, 1, 1)
            end_date = datetime.date(year, 12, 31)
            report_data = {
                "Yearly Report": {
                    "total_expenses": self.calculate_total_expenses(start_date, end_date),
                    "category_breakdown": self.get_expenses_by_category(start_date, end_date),
                }
            }
        else:
            raise ValueError("Invalid period.  Must be 'weekly', 'monthly', or 'yearly'.")

        return report_data

    def get_all_expenses(self) -> List[Expense]:
        """
        Returns all the expenses recorded.

        Returns:
            List[Expense]: A list of all Expense objects.
        """
        return self.expenses