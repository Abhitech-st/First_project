# button_bindings.py
import tkinter as tk
from suggestion import SuggestionEntry


def setup_bindings(app):
    """
    Attach keyboard shortcuts and navigation bindings to the DataEntryApp.
    :param app: DataEntryApp instance from gui.py
    """

    # Collect all entries in order (global first, then row inputs)
    app.all_entries = list(app.global_entries.values()) + list(app.row_entries.values())

    # Identify suggestion fields
    suggestion_fields = ["Party Name", "City", "Agent", "Mkt Committee"]

    # Bind Enter and Shift+Enter for navigation
    for entry in app.all_entries:
        if any(isinstance(entry, SuggestionEntry) for field in suggestion_fields if entry == app.row_entries.get(field)):
            # For suggestion entries
            entry.bind("<Return>", lambda e, current=entry: handle_suggestion_entry(app, current, e))
            entry.bind("<Tab>", lambda e, current=entry: handle_suggestion_entry(app, current, e))
        else:
            # For regular entries
            entry.bind("<Return>", lambda e, current=entry: focus_next(app, current))
        
        entry.bind("<Shift-Return>", lambda e, current=entry: focus_prev(app, current))
        entry.bind("<Control-BackSpace>", lambda e: "break")  # Prevent accidental deletion
        
    # Make Enter in the last entry add a new row
    if app.all_entries:
        last_entry = app.all_entries[-1]
        last_entry.bind("<Return>", lambda e: (app.add_entry(), "break"))

    # Shortcut keys (accelerators)
    app.bind("<Control-s>", lambda e: app.submit_data())
    app.bind("<Control-a>", lambda e: app.add_entry())
    app.bind("<Control-e>", lambda e: app.edit_formula())
    app.bind("<Control-v>", lambda e: app.view_data())
    app.bind("<Control-r>", lambda e: app.tree.delete(*app.tree.get_children()))  # Clear TreeView
    
    # Additional TreeView bindings
    app.tree.bind("<Delete>", lambda e: app.tree.delete(app.tree.selection()) if app.tree.selection() else None)  # Delete selected rows


def handle_suggestion_entry(app, entry, event):
    """
    Handle Enter/Tab key for suggestion entries.
    If suggestions are visible, selects the current suggestion.
    Otherwise, moves to the next field.
    """
    if hasattr(entry, 'listbox') and entry.listbox and entry.listbox.size() > 0:
        # If suggestion list is visible with items, select current suggestion
        entry.select_suggestion()
        focus_next(app, entry)  # Move to next field after selection
        return "break"  # Prevent default handling
    else:
        # If no suggestions shown, just move to next field
        focus_next(app, entry)


def focus_next(app, current_entry):
    """Move focus to the next entry field."""
    entries = app.all_entries
    if current_entry in entries:
        idx = entries.index(current_entry)
        next_idx = (idx + 1) % len(entries)
        entries[next_idx].focus_set()


def focus_prev(app, current_entry):
    """Move focus to the previous entry field."""
    entries = app.all_entries
    if current_entry in entries:
        idx = entries.index(current_entry)
        prev_idx = (idx - 1) % len(entries)
        entries[prev_idx].focus_set()
