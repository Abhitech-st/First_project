# gui.py
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from path_utils import get_resource_path
from button_bindings import setup_bindings
from suggestion import SuggestionEntry
from formula_editor import open_formula_editor
from excel_handler import export_to_excel
from field_inspect import view_data, check_entries

class DataEntryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Entry Application")
        self.geometry("1600x800")

        # Store entry widgets
        self.global_entries = {}
        self.row_entries = {}

        # Define all columns in desired final order
        self.all_columns = [
            "Arrival Lot date",    # Row input
            "MRN No.",            # Formula
            "Bill No.",           # Row input
            "Bill Date",          # Row input
            "Agent",              # Row input
            "Party Name",         # Row input
            "City",               # Row input
            "Mkt Committee",      # Row input
            "Vehicle No.",        # Row input
            "Bags",               # Row input
            "Bill Wt (Qtl)",      # Row input
            "Kanda Wt with Bardana(Qtl)",  # Row input
            "Kanda Wt without Bardana(Qtl)",  # Formula
            "Basic Rate as per Bill",  # Global input
            "Bill Basic Amt",     # Formula
            "Dami Amt",           # Formula
            "Other Amt",           # Row input
            "Other Crs amt",      # Formula
            "Total Bill Amt (Rounded Off)",  # Formula
            "Cost as per Bill",   # Formula
            "Sauda",              # Global input
            "Moist(%)",           # Global input
            "Fungus",             # Global input
            "Broken",             # Global input
            "Shortage",           # Formula
            "Shortage Amt",       # Formula
            "Rate Diff (per Qtl)", # Formula
            "Rate Diff Amt",      # Formula
            "Fungus Cut",         # Formula
            "Broken Cut",         # Formula
            "Moisture Cut",       # Formula
            "Raw Material Value"  # Formula
        ]
        self.all_ordered_columns = [
            "Arrival Lot date",    # Row input
            "MRN No.",            # Formula
            "Bill No.",           # Row input
            "Bill Date",          # Row input
            "Agent",              # Row input
            "Party Name",         # Row input
            "City",               # Row input
            "Mkt Committee",      # Row input
            "Vehicle No.",        # Row input
            "Bags",               # Row input
            "Bill Wt (Qtl)",      # Row input
            "Kanda Wt with Bardana(Qtl)",  # Row input
            "Kanda Wt without Bardana(Qtl)",  # Formula
            "Basic Rate as per Bill",  # Global input
            "Bill Basic Amt",     # Formula
            "Dami Amt",           # Formula
            "Other Amt",           # Row input
            "Other Crs amt",      # Formula
            "Total Bill Amt (Rounded Off)",  # Formula
            "Cost as per Bill",   # Formula
            "Sauda",              # Global input
            "Moist(%)",           # Global input
            "Fungus",             # Global input
            "Broken",             # Global input
            "Shortage",           # Formula
            "Shortage Amt",       # Formula
            "Rate Diff (per Qtl)", # Formula
            "Rate Diff Amt",      # Formula
            "Fungus Cut",         # Formula
            "Broken Cut",         # Formula
            "Moisture Cut",       # Formula
            "Raw Material Value"  # Formula
        ]

        # Split columns into their respective types while maintaining the original grouping logic
        self.global_columns = [
            "Basic Rate as per Bill", "Sauda", "Moist(%)", "Fungus", "Broken"
        ]

        self.row_columns = [
            "Arrival Lot date", "Bill No.", "Bill Date", "Agent", "Party Name",
            "City", "Mkt Committee", "Vehicle No.", "Bags", "Bill Wt (Qtl)",
            "Kanda Wt with Bardana(Qtl)", "Other Amt"
        ]

        self.formula_columns = [
            "MRN No.", "Kanda Wt without Bardana(Qtl)", "Bill Basic Amt",
            "Dami Amt", "Other Crs amt", "Total Bill Amt (Rounded Off)",
            "Cost as per Bill", "Shortage", "Shortage Amt", "Rate Diff (per Qtl)",
            "Rate Diff Amt", "Fungus Cut", "Broken Cut", "Moisture Cut",
            "Raw Material Value"
        ]
        # Split into input types while preserving original functionality
        self.global_columns = [
            "Basic Rate as per Bill", "Sauda", "Moist(%)", "Fungus", "Broken"
        ]

        self.row_columns = [
            "Arrival Lot date", "Bill No.", "Bill Date", "Agent", "Party Name",
            "City", "Mkt Committee", "Vehicle No.", "Bags", "Bill Wt (Qtl)",
            "Kanda Wt with Bardana(Qtl)", "Other Amt"
        ]

        self.formula_columns = [
            "MRN No.", "Kanda Wt without Bardana(Qtl)", "Bill Basic Amt",
            "Dami Amt", "Other Crs amt", "Total Bill Amt (Rounded Off)",
            "Cost as per Bill", "Shortage", "Shortage Amt", "Rate Diff (per Qtl)",
            "Rate Diff Amt", "Fungus Cut", "Broken Cut", "Moisture Cut",
            "Raw Material Value"
        ]

        # Build GUI
        self.create_global_inputs()
        self.create_row_inputs()
        self.create_buttons()
        self.create_treeview()

    def create_global_inputs(self):
        frame = ttk.LabelFrame(self, text="Global Inputs (Persistent)")
        frame.pack(fill="x", padx=10, pady=5)

        for idx, col in enumerate(self.global_columns):
            label = ttk.Label(frame, text=col)
            label.grid(row=0, column=idx * 2, padx=5, pady=5, sticky="w")

            entry = ttk.Entry(frame, width=20)
            entry.grid(row=0, column=idx * 2 + 1, padx=5, pady=5)
            self.global_entries[col] = entry

    def create_row_inputs(self):
        frame = ttk.LabelFrame(self, text="Row Inputs (Cleared After Add)")
        frame.pack(fill="x", padx=10, pady=5)

        for idx, col in enumerate(self.row_columns):
            label = ttk.Label(frame, text=col)
            label.grid(row=idx // 4, column=(idx % 4) * 2, padx=5, pady=5, sticky="w")

            # Use SuggestionEntry for Party Name, City, Agent, and Mkt Committee with separate files
            if col == "Party Name":
                entry = SuggestionEntry(frame, suggestion_file="party_name_suggestions.json", width=20)
            elif col == "City":
                entry = SuggestionEntry(frame, suggestion_file="city_suggestions.json", width=20)
            elif col == "Agent":
                entry = SuggestionEntry(frame, suggestion_file="agent_suggestions.json", width=20)
            elif col == "Mkt Committee":
                entry = SuggestionEntry(frame, suggestion_file="mkt_committee_suggestions.json", width=20)
            else:
                entry = ttk.Entry(frame, width=20)
            entry.grid(row=idx // 4, column=(idx % 4) * 2 + 1, padx=5, pady=5)
            self.row_entries[col] = entry

    def create_buttons(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=5)

        # Left-aligned buttons
        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left", fill="x")

        ttk.Button(left_frame, text="Add Entry", command=self.add_entry).pack(side="left", padx=5)
        ttk.Button(left_frame, text="Edit Formula", command=self.edit_formula).pack(side="left", padx=5)
        ttk.Button(left_frame, text="Submit", command=self.submit_data).pack(side="left", padx=5)
        ttk.Button(left_frame, text="View Data", command=self.view_data).pack(side="left", padx=5)
        ttk.Button(left_frame, text="Check Entries", command=lambda: check_entries(self.tree, self.all_columns)).pack(side="left", padx=5)

        # Right-aligned buttons
        right_frame = ttk.Frame(frame)
        right_frame.pack(side="right", fill="x")

        ttk.Button(right_frame, text="Edit Entry", command=self.edit_selected_row).pack(side="left", padx=5)
        ttk.Button(right_frame, text="Delete Entry", command=self.delete_selected_row).pack(side="left", padx=5)

    def show_formula_popup(self, event):
        """Show formula popup when a formula cell is clicked"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if not item:
            return

        # Get the column that was clicked and the cell value
        column = self.tree.identify_column(event.x)
        col_num = int(column[1]) - 1  # Convert #1, #2 etc to 0-based index
        col_name = self.all_columns[col_num]
        cell_value = self.tree.item(item)["values"][col_num]

        # Only show popup if:
        # 1. It's a formula column
        # 2. It's not the MRN No. column
        # 3. The cell contains "📝 Formula"
        if (col_name in self.formula_columns and 
            col_name != "MRN No." and 
            str(cell_value) == "📝 Formula"):
            try:
                formula_path = get_resource_path("formulas.json")
                with open(formula_path, "r", encoding="utf-8") as f:
                    formulas = json.load(f)
                    if col_name in formulas and "formula" in formulas[col_name]:
                        formula = formulas[col_name]["formula"]
                        
                        # Create popup window
                        popup = tk.Toplevel(self)
                        popup.title(f"Formula for {col_name}")
                        popup.geometry("600x150")
                        
                        # Add formula text
                        text = tk.Text(popup, wrap=tk.WORD, height=4, width=60)
                        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
                        text.insert("1.0", formula)
                        text.config(state="disabled")  # Make read-only
                        
                        # Add close button
                        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=5)
                        
                        # Center popup on screen
                        popup.update_idletasks()
                        width = popup.winfo_width()
                        height = popup.winfo_height()
                        x = (popup.winfo_screenwidth() // 2) - (width // 2)
                        y = (popup.winfo_screenheight() // 2) - (height // 2)
                        popup.geometry(f'+{x}+{y}')
                        
                        # Make popup modal (must close to continue)
                        popup.transient(self)
                        popup.grab_set()
                        self.wait_window(popup)
            except Exception as e:
                print(f"Error showing formula: {e}")

    def create_treeview(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(frame, orient="vertical")
        tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal")

        self.tree = ttk.Treeview(
            frame,
            columns=self.all_columns,
            show="headings",
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            height=15
        )

        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)

        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        # Set headings
        for col in self.all_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
            
        # Bind click event for formula popup
        self.tree.bind('<ButtonRelease-1>', self.show_formula_popup)

    def add_entry(self):
        """Add new row to TreeView"""
        row_data = {}  # Use dictionary to ensure correct column order

        try:
            # Add global and row inputs
            for col in self.global_columns:
                row_data[col] = self.global_entries[col].get().strip()
            
            for col in self.row_columns:
                row_data[col] = self.row_entries[col].get().strip()

            # Load formulas from file
            formulas = self.load_formulas()
            
            if not formulas:
                messagebox.showerror("Error", 
                    "Could not load formulas.json. The application may not work correctly.\n\n"
                    "Please ensure formulas.json is in the same folder as the application.")
                return

            # Add formulas for formula columns
            for col in self.formula_columns:
                if col in formulas and "formula" in formulas[col]:
                    formula = formulas[col]["formula"]
                    if formula.strip().upper() == "=ROW()-1":  # Special case for MRN No.
                        # For MRN No., show actual value
                        value = len(self.tree.get_children()) + 1
                        row_data[col] = value
                    else:
                        # For other formula columns, just show "Formula"
                        row_data[col] = "📝 Formula"
                else:
                    row_data[col] = ""

            # Convert dictionary to list in the correct column order
            ordered_row_data = [row_data.get(col, "") for col in self.all_columns]
            
            # Insert into TreeView
            self.tree.insert("", "end", values=ordered_row_data)

        except Exception as e:
            import traceback
            print("Error in add_entry:", str(e))
            print(traceback.format_exc())

        # Update suggestions
        for field, filename in [
            ("Party Name", "party_name_suggestions.json"),
            ("City", "city_suggestions.json"),
            ("Agent", "agent_suggestions.json"),
            ("Mkt Committee", "mkt_committee_suggestions.json")
        ]:
            value = self.row_entries[field].get().strip()
            entry_widget = self.row_entries[field]
            if hasattr(entry_widget, "suggestion_list") and value and value not in entry_widget.suggestion_list:
                entry_widget.suggestion_list.append(value)
                entry_widget.save_suggestions_to_file()

        # Clear row inputs
        for col in self.row_columns:
            self.row_entries[col].delete(0, tk.END)


    def edit_formula(self):
        open_formula_editor(self)

    def submit_data(self):
    # Collect all rows from TreeView
        rows = []
        for child in self.tree.get_children():
            rows.append(self.tree.item(child)["values"])

        # Export to Excel with Save As dialog
        filepath = export_to_excel(self.all_columns, rows, ask_filename=True)
        print(f"Data exported to {filepath}")

        # ✅ Clear TreeView after export
        for child in self.tree.get_children():
            self.tree.delete(child)

    def view_data(self):
        view_data(self.tree, self.all_columns, self.row_entries)

    def edit_selected_row(self):
        """Edit the selected row in TreeView"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a row to edit.")
            return
        
        # Get the selected item's values
        item = selected_items[0]
        values = self.tree.item(item)['values']
        
        # Create edit dialog
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Entry")
        edit_window.geometry("800x600")
        
        # Create scrollable frame
        canvas = tk.Canvas(edit_window)
        scrollbar = ttk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create entry fields for editable columns
        entries = {}
        row = 0
        
        # Global inputs
        ttk.Label(scrollable_frame, text="Global Inputs", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        for col in self.global_columns:
            ttk.Label(scrollable_frame, text=col).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            entry = ttk.Entry(scrollable_frame)
            idx = self.all_columns.index(col)
            entry.insert(0, str(values[idx]) if values[idx] is not None else "")
            entry.grid(row=row, column=1, padx=5, pady=2, sticky="w")
            entries[col] = entry
            row += 1
        
        # Row inputs
        ttk.Label(scrollable_frame, text="Row Inputs", font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        for col in self.row_columns:
            ttk.Label(scrollable_frame, text=col).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            if col in ["Party Name", "City", "Agent", "Mkt Committee"]:
                entry = SuggestionEntry(scrollable_frame)
            else:
                entry = ttk.Entry(scrollable_frame)
            idx = self.all_columns.index(col)
            entry.insert(0, str(values[idx]) if values[idx] is not None else "")
            entry.grid(row=row, column=1, padx=5, pady=2, sticky="w")
            entries[col] = entry
            row += 1
        
        def save_changes():
            # Update the values
            new_values = list(values)  # Convert tuple to list for modification
            for col, entry in entries.items():
                idx = self.all_columns.index(col)
                new_values[idx] = entry.get().strip()
            
            # Update TreeView
            self.tree.item(item, values=new_values)
            edit_window.destroy()
            messagebox.showinfo("Success", "Entry updated successfully!")
        
        # Add Save button
        ttk.Button(scrollable_frame, text="Save Changes", command=save_changes).grid(row=row, column=0, columnspan=2, pady=20)
        
        # Pack the scrollable frame
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    def delete_selected_row(self):
        """Delete the selected row(s) from TreeView"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select at least one row to delete.")
            return
        
        # Ask for confirmation
        if len(selected_items) == 1:
            msg = "Are you sure you want to delete this entry?"
        else:
            msg = f"Are you sure you want to delete these {len(selected_items)} entries?"
        
        if messagebox.askyesno("Confirm Delete", msg):
            # Delete selected items
            for item in selected_items:
                self.tree.delete(item)
            messagebox.showinfo("Success", "Selected entries deleted successfully!")

    def load_formulas(self):
        """Load formulas from JSON file with better error handling"""
        try:
            formula_path = get_resource_path("formulas.json")
            
            if os.path.exists(formula_path):
                try:
                    with open(formula_path, "r", encoding="utf-8") as f:
                        formulas = json.load(f)
                        print(f"Successfully loaded formulas from {formula_path}")
                        return formulas
                except Exception as e:
                    print(f"Error loading formulas from {formula_path}: {str(e)}")
            else:
                print(f"formulas.json not found at {formula_path}")
            
            return {}
                    
        except Exception as e:
            print(f"Critical error loading formulas: {str(e)}")
            return {}


if __name__ == "__main__":
    app = DataEntryApp()
    setup_bindings(app)
    app.mainloop()
