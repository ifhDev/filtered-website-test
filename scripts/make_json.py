import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import os

LARGE_FIELDS = ["blurb", "altText", "tropes", "readerNotes", "purchaseOptions", "miniBlurb", "similarBooks"]
CONFIG_FILE = "app_config.json"
DEFAULT_CONFIG = {
    "last_path": "",
    "active_template": "Books",
    "templates": {
        "Books": [
            "id", "title", "series", "positionInSeries", "releaseDate", 
            "coverImage", "altText", "blurb", "isRecent", "isFeatured", 
            "tropes", "dynamics", "readerNotes", "isKU", "purchaseOptions", 
            "miniBlurb", "tagLine", "similarBooks"
        ],
        "Reader Magnets & Extras": [
            "parentBookId", "type", "chronology", "timelineContext", 
            "requirement", "bookfunnelLink"
        ],
        "Tropes": [
            "slug", "name", "description", "featured", "canonical"
        ]
    }
}

class DynamicDataManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Database Manager")
        self.root.geometry("1100x700")
        
        self.config = self.load_config()
        self.file_path = self.config.get("last_path")
        self.data = self.load_json_data()
        self.current_fields = self.config["templates"].get(self.config["active_template"], ["id", "title"])
        self.widgets = {}

        self.top_frame = tk.Frame(root, padx=10, pady=5, bg="#e0e0e0")
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Pack the Left Form FIRST or the right one will EAT IT
        self.setup_scrollable_form()
        
        # 2. Pack the Right Table SECOND so it behaves in a civilised manner
        self.right_frame = tk.Frame(root, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.BOTH)

        self.setup_top_bar()
        self.build_dynamic_ui()

    def load_config(self):
        config = DEFAULT_CONFIG.copy()
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config.update(json.load(f))
            except json.JSONDecodeError: pass
        with open(CONFIG_FILE, 'w') as f: json.dump(config, f, indent=4)
        return config

    def save_config(self):
        with open(CONFIG_FILE, 'w') as f: json.dump(self.config, f, indent=4)

    def load_json_data(self):
        if self.file_path and os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f: return json.load(f)
            except: return []
        return []

    def setup_top_bar(self):
        tk.Label(self.top_frame, text="Active Template:", bg="#e0e0e0").pack(side=tk.LEFT, padx=(0, 5))
        
        self.template_var = tk.StringVar(value=self.config["active_template"])
        self.template_dropdown = ttk.Combobox(
            self.top_frame, textvariable=self.template_var, 
            values=list(self.config["templates"].keys()) + ["-- Auto-Detect from JSON --"],
            state="readonly", width=25
        )
        self.template_dropdown.pack(side=tk.LEFT)
        self.template_dropdown.bind("<<ComboboxSelected>>", self.change_template)

        tk.Button(self.top_frame, text="Load New JSON File", command=self.change_file).pack(side=tk.RIGHT)

    def setup_scrollable_form(self):
        container = tk.Frame(self.root, width=450)
        container.pack(side=tk.LEFT, fill=tk.Y)
        
        self.canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0, width=430)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.left_frame = tk.Frame(self.canvas, padx=15)

        self.left_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.left_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    def build_dynamic_ui(self):
        for widget in self.left_frame.winfo_children(): widget.destroy()
        for widget in self.right_frame.winfo_children(): widget.destroy()
        self.widgets.clear()

        tk.Label(self.left_frame, text="Edit / Add Entry", font=("Arial", 14, "bold")).pack(pady=15)
        
        for field in self.current_fields:
            lbl_text = field.replace("_", " ").title()
            tk.Label(self.left_frame, text=lbl_text, font=("Arial", 10, "bold")).pack(anchor='w', pady=(5, 0))
            
            if field.lower() in [f.lower() for f in LARGE_FIELDS]:
                widget = tk.Text(self.left_frame, height=4, width=45, font=("Arial", 10), padx=5, pady=5)
            else:
                widget = tk.Entry(self.left_frame, width=45, font=("Arial", 10))
            
            widget.pack(fill=tk.X, pady=(0, 10))
            self.widgets[field] = widget

        tk.Button(self.left_frame, text="SAVE / UPDATE ENTRY", command=self.save_entry, 
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), height=2).pack(pady=20, fill=tk.X)
        tk.Button(self.left_frame, text="Add New Field to Schema", command=self.add_new_field, 
                  bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=(0, 30))
        tk.Button(self.left_frame, text="Manage / Reorder Fields", command=self.open_schema_manager, 
                  bg="#9b59b6", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=(0, 10))
        tk.Button(self.left_frame, text="Clear Form", command=self.clear_form).pack(fill=tk.X, pady=(0, 30))

        # 1. Create the scrollbar first and pack it at the very bottom
        self.tree_xscroll = ttk.Scrollbar(self.right_frame, orient="horizontal")
        self.tree_xscroll.pack(side=tk.BOTTOM, fill=tk.X)

        # 2. Tell the Treeview to use this scrollbar
        self.tree = ttk.Treeview(self.right_frame, columns=self.current_fields, show="headings", xscrollcommand=self.tree_xscroll.set)
        
        for col in self.current_fields:
            self.tree.heading(col, text=col.title())
            # Optional: You can lower the width here if you want columns narrower by default
            self.tree.column(col, width=120, anchor=tk.W) 
            
        # 3. Pack the tree on top so it fills the rest of the space
        self.tree.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        
        # 4. Tell the scrollbar to talk back to the Treeview
        self.tree_xscroll.config(command=self.tree.xview)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.refresh_table()

    def change_template(self, event=None):
        selected = self.template_var.get()
        if selected == "-- Auto-Detect from JSON --":
            all_keys = set()
            for item in self.data: all_keys.update(item.keys())
            self.current_fields = ["id"] + [k for k in all_keys if k not in ["id", "slug"]]
        else:
            self.current_fields = self.config["templates"][selected]
            self.config["active_template"] = selected
            self.save_config()
        self.build_dynamic_ui()

    def change_file(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            self.file_path = path
            self.config["last_path"] = path
            self.save_config()
            self.data = self.load_json_data()
            self.refresh_table()

    def get_widget_value(self, field):
        w = self.widgets[field]
        return w.get("1.0", "end-1c").strip() if isinstance(w, tk.Text) else w.get().strip()

    def set_widget_value(self, field, value):
        w = self.widgets[field]
        if isinstance(w, tk.Text):
            w.delete("1.0", tk.END)
            w.insert(tk.END, str(value))
        else:
            w.delete(0, tk.END)
            w.insert(0, str(value))

    def save_entry(self):
        new_data = {}
        for f in self.current_fields:
            raw_val = self.get_widget_value(f)
            
            # Smart Type Parsing to keep Astro happy
            if raw_val == "":
                new_data[f] = ""
            elif raw_val.lower() == "true":
                new_data[f] = True
            elif raw_val.lower() == "false":
                new_data[f] = False
            else:
                try:
                    # Parse lists, dicts, ints, and floats safely
                    if raw_val[0] in "[{" or raw_val.lstrip('-').replace('.','',1).isdigit():
                        new_data[f] = json.loads(raw_val)
                    else:
                        new_data[f] = raw_val
                except:
                    new_data[f] = raw_val

        # Dynamically use the first field of the template as the primary key
        pk_field = self.current_fields[0] 
        pk_val = new_data.get(pk_field)

        if not pk_val:
            messagebox.showerror("Error", f"'{pk_field}' is required as a unique identifier.")
            return

        existing_index = next((i for i, item in enumerate(self.data) if str(item.get(pk_field)) == str(pk_val)), None)

        if existing_index is not None:
            self.data[existing_index].update(new_data)
        else:
            self.data.append(new_data)

        with open(self.file_path, 'w') as f: json.dump(self.data, f, indent=4)
        self.refresh_table()
        messagebox.showinfo("Success", f"Saved: {pk_val}")

    def refresh_table(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for index, entry in enumerate(self.data):
            # Cleanly format data for the table display only
            row_data = [str(entry.get(f, "")) for f in self.current_fields]
            # We bind the internal list index to the row so we never lose track of the data
            self.tree.insert("", tk.END, iid=str(index), values=row_data)

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        # Bypass the table strings completely and pull the real dict from memory
        data_index = int(selected[0]) 
        actual_entry = self.data[data_index]
        
        self.clear_form()
        for field in self.current_fields:
            val = actual_entry.get(field, "")
            
            # Format lists/dicts beautifully for the text boxes
            if isinstance(val, (list, dict)):
                val = json.dumps(val, indent=2)
                
            self.set_widget_value(field, val)

    def clear_form(self):
        for f in self.current_fields: self.set_widget_value(f, "")
    
    def add_new_field(self):
        # Prevent editing the read-only auto-detect template
        if self.template_var.get() == "-- Auto-Detect from JSON --":
            messagebox.showwarning("Warning", "Please select a specific template to modify fields, not Auto-Detect.")
            return

        # Prompt user for the new field name
        new_field = simpledialog.askstring("Add Field", "Enter new field name (e.g., camelCase or under_scores):", parent=self.root)
        
        if not new_field or not new_field.strip():
            return
            
        new_field = new_field.strip()
        
        if new_field in self.current_fields:
            messagebox.showinfo("Info", "Field already exists in this template.")
            return

        # 1. Update the configuration template
        self.current_fields.append(new_field)
        self.config["templates"][self.config["active_template"]] = self.current_fields
        self.save_config()

        # 2. Inject the new field into all existing JSON entries
        if self.data:
            for entry in self.data:
                if new_field not in entry:
                    entry[new_field] = ""
            
            # Save the updated data immediately to the file
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, 'w') as f: 
                    json.dump(self.data, f, indent=4)

        # 3. Refresh the UI to render the new entry box and table column
        self.build_dynamic_ui()
        messagebox.showinfo("Success", f"Field '{new_field}' successfully added to all entries.")

    def open_schema_manager(self):
        if self.template_var.get() == "-- Auto-Detect from JSON --":
            messagebox.showwarning("Warning", "Cannot reorder Auto-Detect fields. Select a specific template.")
            return

        # Create a popup window
        manager_window = tk.Toplevel(self.root)
        manager_window.title(f"Manage Fields: {self.config['active_template']}")
        manager_window.geometry("300x400")
        manager_window.transient(self.root) # Keeps it on top of main window
        manager_window.grab_set() # Disables main window until this is closed

        tk.Label(manager_window, text="Select a field to move it:", font=("Arial", 10, "bold")).pack(pady=10)

        # The Listbox to hold our fields
        listbox = tk.Listbox(manager_window, selectmode=tk.SINGLE, font=("Arial", 11), height=12)
        listbox.pack(fill=tk.BOTH, expand=True, padx=20)

        # Populate the listbox
        for field in self.current_fields:
            listbox.insert(tk.END, field)

        # Helper functions for moving items
        def move_up():
            selected = listbox.curselection()
            if not selected or selected[0] == 0: return
            idx = selected[0]
            val = listbox.get(idx)
            listbox.delete(idx)
            listbox.insert(idx - 1, val)
            listbox.selection_set(idx - 1)

        def move_down():
            selected = listbox.curselection()
            if not selected or selected[0] == listbox.size() - 1: return
            idx = selected[0]
            val = listbox.get(idx)
            listbox.delete(idx)
            listbox.insert(idx + 1, val)
            listbox.selection_set(idx + 1)

        def save_new_order():
            # Extract the new order from the listbox
            new_order = list(listbox.get(0, tk.END))
            
            # Update our app state
            self.current_fields = new_order
            self.config["templates"][self.config["active_template"]] = new_order
            self.save_config()
            
            # Refresh the main UI
            self.build_dynamic_ui()
            manager_window.destroy()

        # Control Buttons
        btn_frame = tk.Frame(manager_window)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Move Up ⬆", command=move_up).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Move Down ⬇", command=move_down).grid(row=0, column=1, padx=5)
        
        tk.Button(manager_window, text="Save New Order", command=save_new_order, 
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill=tk.X, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    DynamicDataManager(root)
    root.mainloop()