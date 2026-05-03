import json
import random
import threading
import time
import tkinter as tk
from tkinter import messagebox
from urllib.error import URLError
from urllib.request import Request, urlopen

THEMES = {
    "Red": {
        "bg": "#1e0f10",
        "panel": "#2f1e1f",
        "button": "#b02a33",
        "button_active": "#d75860",
        "text": "#ffffff",
        "accent": "#ff4d5f",
    },
    "Black": {
        "bg": "#121212",
        "panel": "#1e1e1e",
        "button": "#2f2f2f",
        "button_active": "#4c4c4c",
        "text": "#e5e5e5",
        "accent": "#878787",
    },
    "White": {
        "bg": "#f5f5f5",
        "panel": "#ffffff",
        "button": "#e1e1e1",
        "button_active": "#c5c5c5",
        "text": "#111111",
        "accent": "#2a6ebd",
    },
    "Orange": {
        "bg": "#1f1307",
        "panel": "#2c1c0f",
        "button": "#d96c26",
        "button_active": "#e58e4f",
        "text": "#ffffff",
        "accent": "#ffb86c",
    },
    "Pink": {
        "bg": "#1e0f1c",
        "panel": "#2f1f30",
        "button": "#e54da8",
        "button_active": "#f27fcd",
        "text": "#ffffff",
        "accent": "#ff9ed8",
    },
    "Blue": {
        "bg": "#091828",
        "panel": "#122436",
        "button": "#2c82d1",
        "button_active": "#4d9fe8",
        "text": "#eef7ff",
        "accent": "#67b0ff",
    },
}

BIOMES = [
    "Corruption",
    "Eggland",
    "Heaven",
    "Hell",
    "Null",
    "Rainy",
    "Sand Storm",
    "Singularity",
    "Snowy",
    "Starfall",
    "Windy",
    "Cyberspace",
    "Dreamspace",
    "Glitched",
]

class SolsRngMacroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MultiFMacro - Sols RNG Macro")
        self.root.geometry("1040x640")
        self.root.configure(bg=THEMES["Black"]["bg"])
        self.theme_name = "Black"
        self.running = False
        self.paused = False
        self.config = {
            "webhook_url": "",
            "private_server": "",
            "discord_id": "",
            "roblox_user": "",
            "theme": self.theme_name,
            "biomes": {name: False for name in BIOMES},
            "afk_mode": False,
            "multiaccount": False,
            "use_aura_biome": False,
        }
        self.page_states = {
            "Aura": {"scan": False, "color": "cyan"},
            "Detections": {"mode": "Off"},
            "Antikick": {"enabled": False},
            "Fishing": {"auto": False},
            "Leaderboard": {"view": "Weekly"},
            "Remote": {"spy": False},
            "UI": {"accent_mode": False},
        }
        self.load_config()
        self.create_ui()
        self.apply_theme(self.theme_name)

    def create_ui(self):
        self.left_frame = tk.Frame(self.root, width=220, bg=THEMES[self.theme_name]["panel"])
        self.left_frame.pack(side="left", fill="y")
        self.left_frame.pack_propagate(False)

        self.top_label = tk.Label(
            self.root,
            text="Made by Coder-masa",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            bg=THEMES[self.theme_name]["bg"],
            fg=THEMES[self.theme_name]["accent"],
        )
        self.top_label.place(x=14, y=14)

        self.add_left_nav()
        self.main_area = tk.Frame(self.root, bg=THEMES[self.theme_name]["bg"])
        self.main_area.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        self.status_frame = tk.Frame(self.main_area, bg=THEMES[self.theme_name]["bg"])
        self.status_frame.pack(fill="x", pady=(0, 10))

        self.macro_status_label = tk.Label(
            self.status_frame,
            text="Macro Status: Idle",
            bg=THEMES[self.theme_name]["bg"],
            fg=THEMES[self.theme_name]["accent"],
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        )
        self.macro_status_label.pack(side="left", padx=(0, 8))

        self.last_event_label = tk.Label(
            self.status_frame,
            text="Last RNG event: None",
            bg=THEMES[self.theme_name]["bg"],
            fg=THEMES[self.theme_name]["text"],
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.last_event_label.pack(side="left", padx=(12, 0))

        self.page_container = tk.Frame(self.main_area, bg=THEMES[self.theme_name]["bg"])
        self.page_container.pack(fill="both", expand=True)

        self.build_main_panel()

    def add_left_nav(self):
        title = tk.Label(
            self.left_frame,
            text="WEBHOOK",
            fg=THEMES[self.theme_name]["accent"],
            bg=THEMES[self.theme_name]["panel"],
            font=("Segoe UI", 11, "bold"),
        )
        title.pack(pady=(20, 10), anchor="w", padx=18)

        nav_buttons = [
            "Webhook",
            "Aura",
            "Detections",
            "Antikick",
            "Fishing",
            "Leaderboard",
            "Remote",
            "UI",
            "Credits",
        ]

        self.nav_buttons = {}
        for label in nav_buttons:
            button = tk.Button(
                self.left_frame,
                text=label,
                width=18,
                relief="flat",
                bg=THEMES[self.theme_name]["button"],
                fg=THEMES[self.theme_name]["text"],
                activebackground=THEMES[self.theme_name]["button_active"],
                command=lambda l=label: self.on_nav(l),
            )
            button.pack(pady=4, padx=12)
            self.nav_buttons[label] = button

        self.control_frame = tk.Frame(self.left_frame, bg=THEMES[self.theme_name]["panel"])
        self.control_frame.pack(fill="x", pady=(24, 8), padx=12)

        for text, cmd in [("Start", self.start_macro), ("Pause", self.pause_macro), ("Stop", self.stop_macro)]:
            tk.Button(
                self.control_frame,
                text=text,
                width=18,
                bg=THEMES[self.theme_name]["button"],
                fg=THEMES[self.theme_name]["text"],
                activebackground=THEMES[self.theme_name]["button_active"],
                relief="flat",
                command=cmd,
            ).pack(pady=4)

        tk.Button(
            self.left_frame,
            text="Test Webhook",
            width=18,
            bg=THEMES[self.theme_name]["button"],
            fg=THEMES[self.theme_name]["text"],
            activebackground=THEMES[self.theme_name]["button_active"],
            relief="flat",
            command=self.test_webhook,
        ).pack(pady=(12, 2), padx=12)

        tk.Button(
            self.left_frame,
            text="Save Config",
            width=18,
            bg=THEMES[self.theme_name]["button"],
            fg=THEMES[self.theme_name]["text"],
            activebackground=THEMES[self.theme_name]["button_active"],
            relief="flat",
            command=self.save_config,
        ).pack(pady=2, padx=12)

    def activate_nav_button(self, label):
        theme = THEMES[self.theme_name]
        for name, button in self.nav_buttons.items():
            if name == label:
                button.configure(bg=theme["button_active"], fg=theme["text"])
            else:
                button.configure(bg=theme["button"], fg=theme["text"])

    def build_main_panel(self):
        self.page_frames = {}
        theme = THEMES[self.theme_name]

        # Webhook page
        webhook_page = tk.Frame(self.page_container, bg=theme["bg"])
        self.page_frames["Webhook"] = webhook_page

        top_area = tk.Frame(webhook_page, bg=theme["bg"])
        top_area.pack(fill="both", expand=False)

        left_area = tk.Frame(top_area, bg=theme["bg"])
        left_area.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_area = tk.Frame(top_area, bg=theme["bg"], width=340)
        right_area.pack(side="right", fill="y")

        self.webhook_panel = tk.LabelFrame(
            left_area,
            text="Webhook Config",
            bg=theme["panel"],
            fg=theme["text"],
            font=("Segoe UI", 10, "bold"),
            bd=1,
            relief="flat",
            padx=14,
            pady=12,
        )
        self.webhook_panel.pack(fill="x", pady=(0, 12))

        connection_label = tk.Label(
            self.webhook_panel,
            text="Connection",
            bg=theme["panel"],
            fg=theme["accent"],
            font=("Segoe UI", 9, "bold"),
        )
        connection_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.add_form_row(self.webhook_panel, "Webhook URL", "webhook_url")
        self.add_form_row(self.webhook_panel, "Private Server", "private_server")
        self.add_form_row(self.webhook_panel, "Discord ID", "discord_id")
        self.add_form_row(self.webhook_panel, "Roblox User", "roblox_user")

        apply_username_btn = tk.Button(
            self.webhook_panel,
            text="Apply Username",
            bg=theme["button"],
            fg=theme["text"],
            activebackground=theme["button_active"],
            relief="flat",
            command=self.apply_username,
        )
        apply_username_btn.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="w")

        self.options_panel = tk.LabelFrame(
            left_area,
            text="Options",
            bg=theme["panel"],
            fg=theme["text"],
            font=("Segoe UI", 10, "bold"),
            bd=1,
            relief="flat",
            padx=14,
            pady=12,
        )
        self.options_panel.pack(fill="x", pady=(0, 12))

        self.afk_var = tk.BooleanVar(value=self.config["afk_mode"])
        self.multi_var = tk.BooleanVar(value=self.config["multiaccount"])
        self.aura_var = tk.BooleanVar(value=self.config["use_aura_biome"])

        tk.Checkbutton(
            self.options_panel,
            text="AFK Mode",
            variable=self.afk_var,
            bg=theme["panel"],
            fg=theme["text"],
            activebackground=theme["panel"],
            selectcolor=theme["button"],
            command=self.update_config_flags,
        ).grid(row=0, column=0, sticky="w", pady=4)

        tk.Checkbutton(
            self.options_panel,
            text="Multiaccount",
            variable=self.multi_var,
            bg=theme["panel"],
            fg=theme["text"],
            activebackground=theme["panel"],
            selectcolor=theme["button"],
            command=self.update_config_flags,
        ).grid(row=0, column=1, sticky="w", pady=4, padx=(18, 0))

        tk.Checkbutton(
            self.options_panel,
            text="Aura / Biome Notifications",
            variable=self.aura_var,
            bg=theme["panel"],
            fg=theme["text"],
            activebackground=theme["panel"],
            selectcolor=theme["button"],
            command=self.update_config_flags,
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=4)

        theme_label = tk.Label(
            self.options_panel,
            text="Theme:",
            bg=theme["panel"],
            fg=theme["text"],
        )
        theme_label.grid(row=2, column=0, sticky="w", pady=(10, 4))

        self.theme_var = tk.StringVar(value=self.theme_name)
        self.theme_menu = tk.OptionMenu(
            self.options_panel,
            self.theme_var,
            *THEMES.keys(),
            command=self.apply_theme,
        )
        self.theme_menu.configure(
            bg=theme["button"],
            fg=theme["text"],
            activebackground=theme["button_active"],
            highlightthickness=0,
            relief="flat",
        )
        self.theme_menu.grid(row=2, column=1, sticky="w", pady=(10, 4), padx=(18, 0))

        random_button = tk.Button(
            self.options_panel,
            text="Random Colors",
            bg=theme["button"],
            fg=theme["text"],
            activebackground=theme["button_active"],
            relief="flat",
            command=self.apply_random_theme,
        )
        random_button.grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.stats_panel = tk.LabelFrame(
            right_area,
            text="Biome Ping",
            bg=theme["panel"],
            fg=theme["text"],
            font=("Segoe UI", 10, "bold"),
            bd=1,
            relief="flat",
            padx=14,
            pady=12,
        )
        self.stats_panel.pack(fill="both", expand=True)

        all_sessions_label = tk.Label(
            self.stats_panel,
            text="all sessions",
            bg=theme["panel"],
            fg=theme["accent"],
            font=("Segoe UI", 8),
        )
        all_sessions_label.grid(row=0, column=2, sticky="e", padx=(0, 6))

        stats_desc = tk.Label(
            self.stats_panel,
            text="notify when a biome starts",
            bg=theme["panel"],
            fg=theme["text"],
            font=("Segoe UI", 9),
        )
        stats_desc.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 8))

        self.biome_checks = {}
        for idx, biome in enumerate(BIOMES):
            var = tk.BooleanVar(value=self.config["biomes"].get(biome, False))
            chk = tk.Checkbutton(
                self.stats_panel,
                text=biome,
                variable=var,
                bg=theme["panel"],
                fg=theme["text"],
                activebackground=theme["panel"],
                selectcolor=theme["button"],
                command=self.update_biome_config,
            )
            chk.grid(row=(idx // 3) + 2, column=idx % 3, sticky="w", padx=8, pady=4)
            self.biome_checks[biome] = var

        self.status_label = tk.Label(
            webhook_page,
            text="No biomes detected yet.",
            bg=theme["bg"],
            fg=theme["accent"],
            anchor="w",
            font=("Segoe UI", 10),
        )
        self.status_label.pack(fill="x", pady=(10, 0), padx=4)

        self.last_event_detail = tk.Label(
            webhook_page,
            text="Last RNG event: Waiting for the macro to start.",
            bg=theme["bg"],
            fg=theme["text"],
            anchor="w",
            font=("Segoe UI", 10),
        )
        self.last_event_detail.pack(fill="x", pady=(4, 0), padx=4)

        self.log_text = tk.Text(
            webhook_page,
            height=6,
            bg=theme["panel"],
            fg=theme["text"],
            relief="flat",
            insertbackground=theme["text"],
        )
        self.log_text.pack(fill="both", expand=True, pady=(8, 0))
        self.log_text.insert("end", "Ready. Select settings and press Start.\n")
        self.log_text.config(state="disabled")

        # Additional section pages
        self.page_frames["Aura"] = self.create_placeholder_page(
            "Aura",
            "Aura settings and clickable helpers.",
            ["Aura Scan", "Aura Color", "Aura Range", "Aura Actions"],
        )
        self.page_frames["Detections"] = self.create_placeholder_page(
            "Detections",
            "Tap any detection option to test the UI.",
            ["Entity Scan", "Alert Sound", "Distance Check", "Auto Report"],
        )
        self.page_frames["Antikick"] = self.create_placeholder_page(
            "Antikick",
            "Anti-kick protection controls.",
            ["Enable Guard", "Safe Mode", "Server Keep", "Session Watch"],
        )
        self.page_frames["Fishing"] = self.create_placeholder_page(
            "Fishing",
            "Fishing mode, catch rate and auto-bait.",
            ["Auto Fish", "Bait Select", "Fish Detector", "Catch Tracker"],
        )
        self.page_frames["Leaderboard"] = self.create_placeholder_page(
            "Leaderboard",
            "Leaderboard and rank overview.",
            ["Weekly", "Daily", "All-Time", "Friends"],
        )
        self.page_frames["Remote"] = self.create_placeholder_page(
            "Remote",
            "Remote spy and command tools.",
            ["Remote Spy", "Execute", "Request Log", "Guard"],
        )
        self.page_frames["UI"] = self.create_placeholder_page(
            "UI",
            "Theme selection and layout settings.",
            ["Theme Picker", "Random Colors", "Accent Mode", "Reset UI"],
        )
        self.page_frames["Credits"] = self.create_placeholder_page(
            "Credits",
            "Made by Coder-masa.",
            ["About", "License", "Version Info"],
        )

        self.show_page("Webhook")

    def create_placeholder_page(self, title, description, actions):
        theme = THEMES[self.theme_name]
        frame = tk.Frame(self.page_container, bg=theme["bg"])

        label = tk.Label(
            frame,
            text=title,
            bg=theme["bg"],
            fg=theme["accent"],
            font=("Segoe UI", 18, "bold"),
        )
        label.pack(anchor="w", pady=(0, 8))

        desc_label = tk.Label(
            frame,
            text=description,
            bg=theme["bg"],
            fg=theme["text"],
            font=("Segoe UI", 10),
        )
        desc_label.pack(anchor="w", pady=(0, 16))

        content_area = tk.Frame(frame, bg=theme["bg"])
        content_area.pack(fill="both", expand=True)

        action_holder = tk.Frame(content_area, bg=theme["bg"])
        action_holder.pack(side="left", fill="y", padx=(0, 12), pady=(0, 4))

        for action in actions:
            button = tk.Button(
                action_holder,
                text=action,
                width=28,
                bg=theme["button"],
                fg=theme["text"],
                activebackground=theme["button_active"],
                relief="flat",
                command=lambda name=action, page=title: self.handle_page_action(page, name),
            )
            button.pack(fill="x", pady=4)

        detail_area = tk.Frame(content_area, bg=theme["bg"])
        detail_area.pack(side="left", fill="both", expand=True)

        if title == "Leaderboard":
            listbox = tk.Listbox(
                detail_area,
                bg=theme["panel"],
                fg=theme["text"],
                bd=0,
                highlightthickness=0,
                selectbackground=theme["accent"],
                font=("Segoe UI", 10),
            )
            listbox.pack(fill="both", expand=True, pady=(0, 8))
            sample = [
                "1. Coder-masa - 999 pts",
                "2. ShadowFox - 842 pts",
                "3. GhostBlade - 781 pts",
                "4. IceFang - 712 pts",
                "5. Nova - 698 pts",
            ]
            for item in sample:
                listbox.insert("end", item)
            setattr(frame, "leaderboard_box", listbox)

        elif title == "Remote":
            cmd_label = tk.Label(
                detail_area,
                text="Remote command:",
                bg=theme["bg"],
                fg=theme["text"],
                font=("Segoe UI", 10, "bold"),
            )
            cmd_label.pack(anchor="w", pady=(0, 4))
            entry = tk.Entry(
                detail_area,
                bg=theme["panel"],
                fg=theme["text"],
                insertbackground=theme["text"],
                relief="flat",
            )
            entry.pack(fill="x", pady=(0, 8))
            output = tk.Text(
                detail_area,
                height=8,
                bg=theme["panel"],
                fg=theme["text"],
                relief="flat",
                insertbackground=theme["text"],
            )
            output.pack(fill="both", expand=True)
            output.insert("end", "Remote output will appear here.\n")
            output.config(state="disabled")
            setattr(frame, "remote_entry", entry)
            setattr(frame, "remote_output", output)

        elif title == "UI":
            accent_card = tk.Label(
                detail_area,
                text="Accent mode is currently off.",
                bg=theme["panel"],
                fg=theme["text"],
                font=("Segoe UI", 10),
                bd=1,
                relief="solid",
                padx=8,
                pady=8,
            )
            accent_card.pack(fill="x", pady=(0, 8))
            setattr(frame, "accent_card", accent_card)
            preview = tk.Label(
                detail_area,
                text="Theme preview",
                bg=theme["bg"],
                fg=theme["accent"],
                font=("Segoe UI", 12, "bold"),
            )
            preview.pack(anchor="w", pady=(0, 4))
            color_bar = tk.Frame(detail_area, bg=theme["accent"], height=24)
            color_bar.pack(fill="x", pady=(0, 8))
            setattr(frame, "color_bar", color_bar)

        elif title == "Credits":
            credit_text = tk.Label(
                detail_area,
                text="Sols RNG Macro UI\nMade by Coder-masa\n2026 All rights reserved.",
                bg=theme["bg"],
                fg=theme["text"],
                font=("Segoe UI", 10),
                justify="left",
            )
            credit_text.pack(anchor="w", pady=(0, 8))

        else:
            detail_text = tk.Text(
                detail_area,
                height=8,
                bg=theme["panel"],
                fg=theme["text"],
                relief="flat",
                insertbackground=theme["text"],
            )
            detail_text.pack(fill="both", expand=True)
            detail_text.insert("end", "Select a setting or action on the left to see details.\n")
            detail_text.config(state="disabled")
            setattr(frame, "page_detail", detail_text)

        status_label = tk.Label(
            frame,
            text="Ready.",
            bg=theme["bg"],
            fg=theme["accent"],
            font=("Segoe UI", 9),
            anchor="w",
        )
        status_label.pack(fill="x", pady=(10, 0))
        setattr(frame, "status_label", status_label)

        return frame

    def show_page(self, name):
        for page_name, frame in self.page_frames.items():
            frame.pack_forget()
        selected = self.page_frames.get(name)
        if selected:
            selected.pack(fill="both", expand=True)
            self.activate_nav_button(name)

    def handle_page_action(self, page, action):
        message = ""
        page_frame = self.page_frames.get(page)
        detail_text = getattr(page_frame, "page_detail", None)

        if page == "Aura":
            if action == "Aura Scan":
                self.page_states[page]["scan"] = not self.page_states[page]["scan"]
                state = "enabled" if self.page_states[page]["scan"] else "disabled"
                message = f"Aura scan {state}."
            elif action == "Aura Color":
                self.page_states[page]["color"] = "magenta" if self.page_states[page]["color"] == "cyan" else "cyan"
                message = f"Aura color set to {self.page_states[page]['color']}."
            elif action == "Aura Range":
                message = "Aura range set to 18 meters."
            elif action == "Aura Actions":
                message = "Aura actions activated."
            if detail_text:
                detail_text.config(state="normal")
                detail_text.delete("1.0", "end")
                detail_text.insert("end", f"Aura scan: {'ON' if self.page_states[page]['scan'] else 'OFF'}\n")
                detail_text.insert("end", f"Aura color: {self.page_states[page]['color']}\n")
                detail_text.insert("end", "Aura range: 18 meters\n")
                detail_text.insert("end", "Aura actions are ready.\n")
                detail_text.config(state="disabled")
        elif page == "Detections":
            if action == "Entity Scan":
                self.page_states[page]["mode"] = "Scanning"
                message = "Entity scan started."
            elif action == "Alert Sound":
                self.page_states[page]["mode"] = "Alert sound enabled"
                message = "Alert sound enabled."
            elif action == "Distance Check":
                self.page_states[page]["mode"] = "Distance check set to 32."
                message = "Distance check mode set to 32."
            elif action == "Auto Report":
                self.page_states[page]["mode"] = "Auto report active"
                message = "Auto report toggled."
            if detail_text:
                detail_text.config(state="normal")
                detail_text.delete("1.0", "end")
                detail_text.insert("end", f"Current detection mode: {self.page_states[page]['mode']}\n")
                detail_text.insert("end", "Entity scan and reporting controls are live.\n")
                detail_text.config(state="disabled")
        elif page == "Antikick":
            if action == "Enable Guard":
                self.page_states[page]["enabled"] = True
                message = "Antikick guard enabled."
            elif action == "Safe Mode":
                self.page_states[page]["enabled"] = True
                message = "Safe mode activated."
            elif action == "Server Keep":
                message = "Server keep alive option is on."
            elif action == "Session Watch":
                message = "Session watch started."
            if detail_text:
                detail_text.config(state="normal")
                enabled = self.page_states[page].get("enabled", False)
                detail_text.delete("1.0", "end")
                detail_text.insert("end", f"Antikick guard: {'ON' if enabled else 'OFF'}\n")
                detail_text.insert("end", "Session watch is monitoring your connection.\n")
                detail_text.config(state="disabled")
        elif page == "Fishing":
            if action == "Auto Fish":
                self.page_states[page]["auto"] = not self.page_states[page]["auto"]
                message = "Auto fish enabled." if self.page_states[page]["auto"] else "Auto fish disabled."
            elif action == "Bait Select":
                message = "Bait selection opened."
            elif action == "Fish Detector":
                message = "Fish detector is listening."
            elif action == "Catch Tracker":
                message = "Catch tracker started."
            if detail_text:
                detail_text.config(state="normal")
                detail_text.delete("1.0", "end")
                detail_text.insert("end", f"Auto fishing: {'ENABLED' if self.page_states[page]['auto'] else 'DISABLED'}\n")
                detail_text.insert("end", "Fishing detector and bait tools are ready.\n")
                detail_text.config(state="disabled")
        elif page == "Leaderboard":
            if action in ["Weekly", "Daily", "All-Time", "Friends"]:
                self.page_states[page]["view"] = action
                message = f"Now showing {action} leaderboard."
                page_frame = self.page_frames.get(page)
                if page_frame and hasattr(page_frame, "leaderboard_box"):
                    box = page_frame.leaderboard_box
                    box.delete(0, "end")
                    sample = []
                    if action == "Weekly":
                        sample = [
                            "1. Coder-masa - 999 pts",
                            "2. ShadowFox - 842 pts",
                            "3. GhostBlade - 781 pts",
                        ]
                    elif action == "Daily":
                        sample = [
                            "1. Flash - 192 pts",
                            "2. Holo - 180 pts",
                            "3. Ember - 169 pts",
                        ]
                    elif action == "All-Time":
                        sample = [
                            "1. Coder-masa - 12,134 pts",
                            "2. NightStalker - 11,051 pts",
                            "3. Pixel - 10,764 pts",
                        ]
                    elif action == "Friends":
                        sample = [
                            "1. FriendA - 733 pts",
                            "2. FriendB - 692 pts",
                            "3. FriendC - 652 pts",
                        ]
                    for item in sample:
                        box.insert("end", item)
        elif page == "Remote":
            if action == "Remote Spy":
                self.page_states[page]["spy"] = not self.page_states[page].get("spy", False)
                message = "Remote spy enabled." if self.page_states[page]["spy"] else "Remote spy disabled."
                if self.page_states[page]["spy"]:
                    self.send_discord_notification("Remote spy enabled", "Remote spy mode has been activated.")
            elif action == "Execute":
                page_frame = self.page_frames.get(page)
                command_text = ""
                if page_frame and hasattr(page_frame, "remote_entry") and hasattr(page_frame, "remote_output"):
                    command_text = page_frame.remote_entry.get().strip()
                    output = page_frame.remote_output
                    output.config(state="normal")
                    if command_text:
                        output.insert("end", f"> {command_text}\nExecuted command: {command_text}\n")
                        message = f"Executed remote command: {command_text}"
                    else:
                        output.insert("end", "> No command entered.\n")
                        message = "No command entered."
                    output.see("end")
                    output.config(state="disabled")
            elif action == "Request Log":
                page_frame = self.page_frames.get(page)
                if page_frame and hasattr(page_frame, "remote_output"):
                    output = page_frame.remote_output
                    output.config(state="normal")
                    output.insert("end", "Request log opened. No recent remote requests.\n")
                    output.see("end")
                    output.config(state="disabled")
                message = "Request log displayed."
            elif action == "Guard":
                message = "Remote guard enabled."
        elif page == "UI":
            if action == "Theme Picker":
                message = "Use the theme dropdown to change your UI theme."
            elif action == "Random Colors":
                self.apply_random_theme()
                message = "Random colors applied."
            elif action == "Accent Mode":
                self.page_states[page]["accent_mode"] = not self.page_states[page]["accent_mode"]
                page_frame = self.page_frames.get(page)
                if page_frame and hasattr(page_frame, "accent_card") and hasattr(page_frame, "color_bar"):
                    on_text = "on" if self.page_states[page]["accent_mode"] else "off"
                    page_frame.accent_card.configure(text=f"Accent mode is currently {on_text}.")
                    page_frame.color_bar.configure(bg=THEMES[self.theme_name]["accent"] if self.page_states[page]["accent_mode"] else THEMES[self.theme_name]["button"])
                message = "Accent mode toggled."
            elif action == "Reset UI":
                self.apply_theme("Black")
                self.theme_var.set("Black")
                message = "UI reset to Black theme."
        elif page == "Credits":
            if action == "About":
                messagebox.showinfo("About", "Sols RNG Macro UI by Coder-masa")
                message = "About shown."
            elif action == "License":
                messagebox.showinfo("License", "This UI is provided as-is.")
                message = "License shown."
            elif action == "Version Info":
                messagebox.showinfo("Version Info", "Version 1.0\nBuild 2026")
                message = "Version info shown."

        if page_frame and hasattr(page_frame, "status_label"):
            page_frame.status_label.configure(text=message)
        self.log(f"{page} action: {action} -> {message}")


    def add_form_row(self, parent, label_text, key):
        row = parent.grid_size()[1]
        label = tk.Label(
            parent,
            text=label_text,
            bg=THEMES[self.theme_name]["panel"],
            fg=THEMES[self.theme_name]["text"],
        )
        label.grid(row=row, column=0, sticky="w", pady=4)
        entry = tk.Entry(
            parent,
            width=55,
            bg="#1b1b1b",
            fg="#ffffff",
            insertbackground="#ffffff",
        )
        entry.grid(row=row, column=1, pady=4, padx=(12, 0), sticky="w")
        entry.insert(0, self.config.get(key, ""))
        setattr(self, f"{key}_entry", entry)

    def apply_username(self):
        username = self.roblox_user_entry.get().strip()
        if username:
            self.log(f"Username set to {username}.")
        else:
            self.log("No Roblox username entered.")

    def update_config_flags(self):
        self.config["afk_mode"] = self.afk_var.get()
        self.config["multiaccount"] = self.multi_var.get()
        self.config["use_aura_biome"] = self.aura_var.get()

    def update_biome_config(self):
        self.config["biomes"] = {name: var.get() for name, var in self.biome_checks.items()}

    def apply_random_theme(self):
        random_theme = {
            "bg": f"#{random.randint(0, 0xAAAAAA):06x}",
            "panel": f"#{random.randint(0, 0xAAAAAA):06x}",
            "button": f"#{random.randint(0, 0xFFFFFF):06x}",
            "button_active": f"#{random.randint(0, 0xFFFFFF):06x}",
            "text": "#ffffff",
            "accent": f"#{random.randint(0, 0xFFFFFF):06x}",
        }
        THEMES["Random"] = random_theme
        self.theme_var.set("Random")
        self.apply_theme("Random")

        menu = self.theme_menu["menu"]
        menu.delete(0, "end")
        for theme_name in THEMES.keys():
            menu.add_command(
                label=theme_name,
                command=lambda name=theme_name: self.theme_var.set(name) or self.apply_theme(name),
            )
        self.log("Applied random UI colors.")

    def on_nav(self, label):
        self.show_page(label)
        self.log(f"Navigation selected: {label}")

    def style_widget(self, widget, theme):
        if isinstance(widget, tk.LabelFrame):
            widget.configure(bg=theme["panel"], fg=theme["text"])
        elif isinstance(widget, tk.Frame):
            widget.configure(bg=theme["bg"])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=theme["button"], fg=theme["text"], activebackground=theme["button_active"])
        elif isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["text"])
        elif isinstance(widget, tk.Checkbutton):
            widget.configure(bg=theme["panel"], fg=theme["text"], activebackground=theme["panel"], selectcolor=theme["button"])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
        elif isinstance(widget, tk.Text):
            widget.configure(bg=theme["panel"], fg=theme["text"], insertbackground=theme["text"])
        elif isinstance(widget, tk.Menubutton):
            widget.configure(bg=theme["button"], fg=theme["text"], activebackground=theme["button_active"])

        for child in widget.winfo_children():
            self.style_widget(child, theme)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def start_macro(self):
        if self.running:
            self.log("Macro already running.")
            return
        self.running = True
        self.paused = False
        self.update_config_flags()
        self.update_biome_config()
        self.log("Starting Sols RNG macro...")
        threading.Thread(target=self.run_macro_loop, daemon=True).start()
        if hasattr(self, "macro_status_label"):
            self.macro_status_label.config(text="Macro Status: Running")
        self.send_discord_notification("Macro started", "Sols RNG macro started.")

    def pause_macro(self):
        if not self.running:
            self.log("Macro is not running.")
            return
        self.paused = not self.paused
        state = "paused" if self.paused else "resumed"
        self.log(f"Macro {state}.")
        if hasattr(self, "macro_status_label"):
            self.macro_status_label.config(text=f"Macro Status: {state.title()}")
        self.send_discord_notification("Macro paused/resumed", f"Macro {state}.")

    def stop_macro(self):
        if not self.running:
            self.log("Macro is not running.")
            return
        self.running = False
        self.paused = False
        self.log("Macro stopped.")
        if hasattr(self, "macro_status_label"):
            self.macro_status_label.config(text="Macro Status: Idle")
        self.send_discord_notification("Macro stopped", "Sols RNG macro stopped.")

    def run_macro_loop(self):
        iteration = 0
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            iteration += 1
            event = random.choice([
                "Rare spawn rolled",
                "Perfect RNG result found",
                "Aura shimmer detected",
                "Biome signal active",
                "Lucky RNG check succeeded",
                "Stream event triggered",
                "Ghost RNG pulse",
                "Hidden treasure ping",
            ])
            event_text = f"Iteration {iteration}: {event}"
            if self.config["afk_mode"]:
                event_text += " [AFK mode]"
            if self.config["multiaccount"]:
                event_text += " [Multi-account]"
            if self.config["use_aura_biome"]:
                event_text += " [Aura/Biome tracking enabled]"

            self.macro_status_label.config(text=f"Macro Status: Running ({iteration})")
            if hasattr(self, "last_event_label"):
                self.last_event_label.config(text=f"Last RNG event: {event}")
            if hasattr(self, "last_event_detail"):
                self.last_event_detail.config(text=event_text)
            self.log(event_text)

            if iteration % 5 == 0 and self.config["use_aura_biome"]:
                detected = [name for name, enabled in self.config["biomes"].items() if enabled]
                if detected:
                    self.status_label.config(text=f"Detected: {', '.join(detected[:3])}")
                    self.send_discord_notification(
                        "Aura/Biome alert",
                        f"Detected selected biomes: {', '.join(detected[:3])}",
                    )
                else:
                    self.status_label.config(text="Aura/Biome tracking active, no selected biomes detected.")
            time.sleep(1.2)

        self.status_label.config(text="Macro stopped.")
        self.macro_status_label.config(text="Macro Status: Idle")

    def test_webhook(self):
        webhook_url = self.webhook_url_entry.get().strip()
        if not webhook_url:
            messagebox.showwarning("Webhook", "Please enter a Webhook URL first.")
            return
        self.send_discord_notification("Webhook test", "This is a test notification from the Sols RNG macro UI.")
        self.log("Webhook test sent.")

    def send_discord_notification(self, title, content):
        webhook_url = self.webhook_url_entry.get().strip()
        if not webhook_url:
            return
        payload = json.dumps({
            "username": "Sols RNG Macro",
            "embeds": [
                {
                    "title": title,
                    "description": content,
                    "color": 15277667,
                }
            ]
        }).encode("utf-8")
        try:
            request = Request(webhook_url, data=payload, method="POST")
            request.add_header("Content-Type", "application/json")
            with urlopen(request, timeout=10) as response:
                if 200 <= response.status < 300:
                    self.log("Discord notification sent.")
                else:
                    self.log(f"Webhook failed: HTTP {response.status}")
        except URLError as exc:
            self.log(f"Webhook error: {exc}")

    def save_config(self):
        self.config.update(
            webhook_url=self.webhook_url_entry.get().strip(),
            private_server=self.private_server_entry.get().strip(),
            discord_id=self.discord_id_entry.get().strip(),
            roblox_user=self.roblox_user_entry.get().strip(),
            theme=self.theme_name,
        )
        self.update_biome_config()
        with open("macro_config.json", "w", encoding="utf-8") as file:
            json.dump(self.config, file, indent=4)
        self.log("Configuration saved.")
        messagebox.showinfo("Save Config", "Configuration saved to macro_config.json.")

    def load_config(self):
        try:
            with open("macro_config.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.config.update(data)
                self.theme_name = self.config.get("theme", self.theme_name)
        except (FileNotFoundError, ValueError):
            pass

    def apply_theme(self, theme_name):
        if theme_name not in THEMES:
            return
        self.theme_name = theme_name
        theme = THEMES[theme_name]
        self.root.configure(bg=theme["bg"])
        self.left_frame.configure(bg=theme["panel"])
        self.main_area.configure(bg=theme["bg"])
        self.page_container.configure(bg=theme["bg"])
        self.top_label.configure(bg=theme["bg"], fg=theme["accent"])
        self.theme_menu.configure(bg=theme["button"], fg=theme["text"], activebackground=theme["button_active"])
        self.style_widget(self.main_area, theme)
        self.style_widget(self.left_frame, theme)
        self.style_widget(self.page_container, theme)
        if hasattr(self, "status_label"):
            self.status_label.configure(bg=theme["bg"], fg=theme["accent"])
        self.activate_nav_button(self.theme_var.get() if self.theme_var.get() in self.page_frames else "Webhook")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolsRngMacroApp(root)
    root.mainloop()
