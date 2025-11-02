from tkinter import filedialog, messagebox
import openpyxl
from tkinter import messagebox
from datetime import datetime



# entry_viewer.py

def view_data(tree, all_columns, row_entries=None):
    """
    Load an Excel file into the TreeView and update suggestions if row_entries are provided.
    """
    filepath = filedialog.askopenfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel Files", "*.xlsx")],
        initialdir="exports",
        title="Open Excel File"
    )

    if not filepath:
        return  # user cancelled

    try:
        wb = openpyxl.load_workbook(filepath, data_only=False)
        ws = wb.active

        # Clear TreeView
        for child in tree.get_children():
            tree.delete(child)

        # Collect unique values for suggestions
        new_suggestions = {
            "Party Name": set(),
            "City": set(),
            "Agent": set(),
            "Mkt Committee": set()
        }

        # Read rows (skip header row)
        for row in ws.iter_rows(min_row=2, values_only=True):
            tree.insert("", "end", values=row)

            # Extract values for suggestion fields
            for field in new_suggestions.keys():
                try:
                    col_index = all_columns.index(field)
                    value = row[col_index]
                    if value:
                        new_suggestions[field].add(str(value))
                except Exception:
                    pass

        # ✅ Update suggestion JSON files if row_entries are provided
        if row_entries:
            for field, filename in [
                ("Party Name", "party_name_suggestions.json"),
                ("City", "city_suggestions.json"),
                ("Agent", "agent_suggestions.json"),
                ("Mkt Committee", "mkt_committee_suggestions.json")
            ]:
                entry_widget = row_entries.get(field)
                if hasattr(entry_widget, "update_suggestions"):
                    merged = set(entry_widget.suggestion_list) | new_suggestions[field]
                    entry_widget.update_suggestions(sorted(merged))

        messagebox.showinfo("View Data", f"Data loaded and suggestions updated from:\n{filepath}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load Excel file:\n{e}")


# entry_checker.py

def check_entries(tree, all_columns):
    """Validate all TreeView entries before export."""
    errors = []
    required_fields = ["Bill No.", "Bill Date", "Bags", "Bill Wt (Qtl)"]

    for row_idx, child in enumerate(tree.get_children(), start=1):
        values = tree.item(child)["values"]

        # Required field check
        for field in required_fields:
            try:
                value = values[all_columns.index(field)]
                if not value or str(value).strip() == "":
                    errors.append(f"Row {row_idx}: {field} is empty")
            except ValueError:
                pass

        # Numeric check
        numeric_fields = ["Bags", "Bill Wt (Qtl)", "Kanda Wt with Bardana(Qtl)", 
                         "Basic Rate as per Bill", "Sauda", "Moist(%)", "Fungus", "Broken"]
        for field in numeric_fields:
            try:
                value = values[all_columns.index(field)]
                if value and value != "" and not isinstance(value, (int, float)):
                    # Try to convert string to float
                    try:
                        float_val = float(str(value).replace(',', ''))  # Remove commas
                        if not isinstance(float_val, (int, float)):
                            raise ValueError
                    except ValueError:
                        errors.append(f"Row {row_idx}: {field} must be numeric")
            except Exception as e:
                if field in required_fields:  # Only show error for required fields
                    errors.append(f"Row {row_idx}: {field} must be numeric")

        # Date format check
        try:
            bill_date = values[all_columns.index("Bill Date")]
            if bill_date:
                datetime.strptime(str(bill_date), "%d/%m/%Y")
        except Exception:
            errors.append(f"Row {row_idx}: Bill Date must be in DD/MM/YYYY format")

    # Show results
    if errors:
        messagebox.showerror("Entry Check Failed", "\n".join(errors))
        return False
    else:
        messagebox.showinfo("Entry Check", "✅ All entries are valid!")
        return True
