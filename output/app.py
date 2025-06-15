import gradio as gr
import datetime
from expenses import ExpenseManager, UserAccount, Expense

# Initialize the expense manager with a default balance
user_account = UserAccount(0)
expense_manager = ExpenseManager(user_account)


def set_initial_balance(initial_balance):
    global user_account, expense_manager
    try:
        initial_balance = float(initial_balance)
        user_account = UserAccount(initial_balance)
        expense_manager = ExpenseManager(user_account)
        return f"Initial balance set to: {initial_balance}"
    except ValueError:
        return "Invalid input. Please enter a number."

def add_expense(amount, category, date, description):
    global expense_manager
    try:
        amount = float(amount)
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        expense_manager.add_expense(amount, category, date, description)
        return "Expense added successfully."
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {e}"

def update_expense(index, amount, category, date, description):
    global expense_manager
    try:
        index = int(index)
        amount = float(amount)
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        expense_manager.update_expense(index, amount, category, date, description)
        return "Expense updated successfully."
    except ValueError as e:
        return str(e)
    except IndexError:
        return "Invalid expense index."
    except Exception as e:
        return f"An error occurred: {e}"

def delete_expense(index):
    global expense_manager
    try:
        index = int(index)
        expense_manager.delete_expense(index)
        return "Expense deleted successfully."
    except ValueError:
        return "Invalid index. Please enter a number."
    except IndexError:
        return "Invalid expense index."
    except Exception as e:
        return f"An error occurred: {e}"

def view_expenses(start_date, end_date):
    global expense_manager
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        expenses = expense_manager.get_expenses_by_period(start_date, end_date)
        output = ""
        for expense in expenses:
            output += f"{expense}\n"
        if not output:
            output = "No expenses found in the specified period."
        return output
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {e}"

def generate_report(period):
    global expense_manager
    try:
        report = expense_manager.generate_report(period)
        return str(report)
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {e}"
    
def get_balance():
     global expense_manager
     return str(expense_manager.get_remaining_balance())

with gr.Blocks() as demo:
    gr.Markdown("# Simple Expense Manager")

    with gr.Tab("Initial Balance"):
        initial_balance_input = gr.Number(label="Initial Balance")
        set_balance_button = gr.Button("Set Balance")
        balance_output = gr.Textbox(label="Output")
        set_balance_button.click(set_initial_balance, inputs=initial_balance_input, outputs=balance_output)
        
    with gr.Tab("Add Expense"):
        amount_input = gr.Number(label="Amount")
        category_input = gr.Textbox(label="Category")
        date_input = gr.DateTime(label="Date")
        description_input = gr.Textbox(label="Description", lines=2)
        add_button = gr.Button("Add Expense")
        add_output = gr.Textbox(label="Output")
        add_button.click(add_expense, inputs=[amount_input, category_input, date_input.value, description_input], outputs=add_output)
        
    with gr.Tab("Update Expense"):
        index_input = gr.Number(label="Index of Expense to Update")
        update_amount_input = gr.Number(label="New Amount")
        update_category_input = gr.Textbox(label="New Category")
        update_date_input = gr.DateTime(label="New Date")
        update_description_input = gr.Textbox(label="New Description", lines=2)
        update_button = gr.Button("Update Expense")
        update_output = gr.Textbox(label="Output")
        update_button.click(update_expense, inputs=[index_input, update_amount_input, update_category_input, update_date_input, update_description_input], outputs=update_output)

    with gr.Tab("Delete Expense"):
        delete_index_input = gr.Number(label="Index of Expense to Delete")
        delete_button = gr.Button("Delete Expense")
        delete_output = gr.Textbox(label="Output")
        delete_button.click(delete_expense, inputs=delete_index_input, outputs=delete_output)

    with gr.Tab("View Expenses"):
        start_date_input = gr.DateTime(label="Start Date")
        end_date_input = gr.DateTime(label="End Date")
        view_button = gr.Button("View Expenses")
        view_output = gr.Textbox(label="Expenses")
        view_button.click(view_expenses, inputs=[start_date_input, end_date_input], outputs=view_output)

    with gr.Tab("Generate Report"):
        period_input = gr.Radio(["weekly", "monthly", "yearly"], label="Period")
        report_button = gr.Button("Generate Report")
        report_output = gr.Textbox(label="Report")
        report_button.click(generate_report, inputs=period_input, outputs=report_output)

    with gr.Tab("View Balance"):
        balance_button = gr.Button("Get Balance")
        balance_text = gr.Textbox(label="Current Balance")
        balance_button.click(get_balance, outputs=balance_text)

demo.launch()