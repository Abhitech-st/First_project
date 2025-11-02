# formula_editor.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from path_utils import get_resource_path

FORMULA_FILE = get_resource_path("formulas.json")

# Default formulas (column-name based)
DEFAULT_FORMULAS = {
    "Kanda Wt without Bardana(Qtl)": "=[Kanda Wt with Bardana(Qtl)] - [Bags] * 0.02",  # assuming 2% weight of bags
    "Bill Basic Amt": "=[Bill Wt (Qtl)] * [Basic Rate as per Bill]",
    "Dami Amt": "=[Other Amt]",
    "MRN No.":"=ROW()-1",
    "Other Crs Amt": "=[Other Amt]",  # consistency adjustment
    "Total Bill Amt (Rounded Off)": "=ROUND([Bill Basic Amt] + [Dami Amt], 0)",
    "Cost as per Bill": "=[Total Bill Amt (Rounded Off)]",
    "Shortage": "=[Bill Wt (Qtl)] - [Kanda Wt without Bardana(Qtl)]",
    "Shortage Amt": "=[Shortage] * [Basic Rate as per Bill]",
    "Rate Diff (per Qtl)": "=[Basic Rate as per Bill] - [Sauda]",
    "Rate Diff Amt": "=[Rate Diff (per Qtl)] * [Bill Wt (Qtl)]",
    "Fungus Cut": "=[Fungus] * 1",   # replace 1 with rate if fixed
    "Broken Cut": "=[Broken] * 1",   # replace 1 with rate if fixed
    "Moisture Cut": "=[Moist(%)] * 1",  # replace 1 with rate if fixed
    "Raw Material Value": "=[Total Bill Amt (Rounded Off)] - [Fungus Cut] - [Broken Cut] - [Moisture Cut]"
}


def load_formulas():
    """Load formulas from JSON, fallback to defaults."""
    if os.path.exists(FORMULA_FILE):
        try:
            with open(FORMULA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        col: {"formula": f, "excel_formula": ""}
        for col, f in DEFAULT_FORMULAS.items()
    }


def save_formulas(formulas):
    """Save formulas to JSON."""
    with open(FORMULA_FILE, "w", encoding="utf-8") as f:
        json.dump(formulas, f, indent=2, ensure_ascii=False)


class FormulaEditor(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Formula Editor")
        self.geometry("900x600")
        self.formulas = load_formulas()

        # --- Instructions ---
        instructions = (
            "Instructions:\n"
            "- Use column names inside [brackets]. Example: =[Bill Wt (Qtl)] * [Basic Rate as per Bill]\n"
            "- You can use Excel functions like ROUND, SUM, etc.\n"
            "- Formulas entered here will be saved and applied in Excel export.\n"
        )
        ttk.Label(self, text=instructions, justify="left").pack(fill="x", padx=10, pady=10)

        # --- Scrollable Frame ---
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Column Headings ---
        ttk.Label(self.scrollable_frame, text="Column Name", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(self.scrollable_frame, text="Formula", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # --- Editable Rows ---
        self.entry_widgets = {}
        for idx, (col, details) in enumerate(self.formulas.items(), start=1):
            formula = details.get("formula", "")
            ttk.Label(self.scrollable_frame, text=col, width=35, anchor="w").grid(row=idx, column=0, padx=5, pady=3, sticky="w")

            entry = ttk.Entry(self.scrollable_frame, width=80)
            entry.insert(0, formula)
            entry.grid(row=idx, column=1, padx=5, pady=3, sticky="w")

            self.entry_widgets[col] = entry

        # --- Save Button ---
        save_btn = ttk.Button(self, text="Save All", command=self.save_all)
        save_btn.pack(pady=10)

    def save_all(self):
        """Save all formulas from entry widgets."""
        for col, entry in self.entry_widgets.items():
            new_formula = entry.get().strip()
            self.formulas[col]["formula"] = new_formula
            self.formulas[col]["excel_formula"] = f"[to be mapped for {col}]"  # placeholder

        save_formulas(self.formulas)
        messagebox.showinfo("Saved", "All formulas have been saved!")


def open_formula_editor(master):
    FormulaEditor(master)
