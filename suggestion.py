import tkinter as tk
from tkinter import ttk
import json
import os
from path_utils import get_resource_path

class SuggestionEntry(ttk.Entry):
    def __init__(self, master=None, suggestion_file=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.suggestion_file = suggestion_file
        self.suggestion_list = self.load_suggestions_from_file() if suggestion_file else []
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace_add('write', self.show_suggestions)
        self.listbox = None
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)
        self.bind("<Return>", self.select_suggestion)
        self.bind("<FocusOut>", self.hide_suggestions)
        self.selected_index = -1

    def load_suggestions_from_file(self):
        suggestion_path = get_resource_path(self.suggestion_file) if self.suggestion_file else None
        if suggestion_path and os.path.exists(suggestion_path):
            try:
                with open(suggestion_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
            except Exception:
                pass
        return []

    def save_suggestions_to_file(self):
        if self.suggestion_file:
            suggestion_path = get_resource_path(self.suggestion_file)
            try:
                with open(suggestion_path, 'w', encoding='utf-8') as f:
                    json.dump(sorted(set(self.suggestion_list)), f, ensure_ascii=False, indent=2)
            except Exception:
                pass

    def show_suggestions(self, *args):
        value = self.var.get()
        if not value:
            self.hide_suggestions()
            return
        # Only suggest entries that are already in the suggestion file, not the current incomplete input
        matches = [s for s in self.suggestion_list if s.lower().startswith(value.lower()) and s.lower() != value.lower()]
        if matches:
            if not self.listbox:
                self.listbox = tk.Listbox(self.master, height=5)
                self.listbox.bind("<Button-1>", self.on_listbox_click)
                self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
            self.listbox.delete(0, tk.END)
            for match in matches:
                self.listbox.insert(tk.END, match)
            self.listbox.lift()
            self.selected_index = -1
        else:
            self.hide_suggestions()

    def hide_suggestions(self, *args):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None
            self.selected_index = -1

    def move_down(self, event):
        if self.listbox:
            if self.selected_index < self.listbox.size() - 1:
                self.selected_index += 1
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(self.selected_index)
                self.listbox.activate(self.selected_index)

    def move_up(self, event):
        if self.listbox:
            if self.selected_index > 0:
                self.selected_index -= 1
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(self.selected_index)
                self.listbox.activate(self.selected_index)

    def select_suggestion(self, event=None):
        if self.listbox:
            if self.selected_index >= 0:
                # If an item is selected, use it
                value = self.listbox.get(self.selected_index)
            elif self.listbox.size() > 0:
                # If no item is selected but suggestions exist, use the first one
                value = self.listbox.get(0)
            else:
                return "break"
            
            self.var.set(value)
            self.hide_suggestions()
            self.icursor(tk.END)
            self.event_generate('<Tab>')  # Generate Tab event to move to next field
            return "break"

    def on_listbox_click(self, event):
        if self.listbox:
            index = self.listbox.nearest(event.y)
            value = self.listbox.get(index)
            self.var.set(value)
            self.hide_suggestions()
            self.icursor(tk.END)

    def update_suggestions(self, new_suggestions):
        self.suggestion_list = new_suggestions
        self.save_suggestions_to_file()
