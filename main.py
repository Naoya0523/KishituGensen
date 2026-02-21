
import tkinter as tk
from tkinter import ttk
import itertools
from Status import *
from weapons import *
from field import *

# ==========================================
# 1. データ準備
# ==========================================
field_list = [cls() for cls in Field.__subclasses__()]
weapon_list = [cls() for cls in Weapon.__subclasses__()]

# ==========================================
# 2. 演算ロジック (確率計算を削除)
# ==========================================
def find_best_farming_routes(primary_weapon: Weapon, weapon_list: list, field_list: list):
    results = []
    valid_fields = []
    
    for field in field_list:
        if (primary_weapon.status_1 in field.status_1s and 
            primary_weapon.status_2 in field.status_2s and 
            primary_weapon.status_3 in field.status_3s):
            valid_fields.append(field)

    for field in valid_fields:
        target_23_candidates = [primary_weapon.status_2, primary_weapon.status_3]

        for target_23 in target_23_candidates:
            possible_other_weapons = []
            for w in weapon_list:
                if w == primary_weapon or not w.is_owned:
                    continue
                if not (w.status_1 in field.status_1s and 
                        w.status_2 in field.status_2s and 
                        w.status_3 in field.status_3s):
                    continue
                if w.status_2 != target_23 and w.status_3 != target_23:
                    continue
                possible_other_weapons.append(w)

            fixed_status_1 = primary_weapon.status_1
            available_status_1s = field.status_1s - {fixed_status_1}
            
            candidates = list(available_status_1s)
            if len(candidates) < 2:
                combinations_1 = [tuple(candidates)]
            else:
                combinations_1 = list(itertools.combinations(candidates, 2))

            for combo in combinations_1:
                current_target_1s = {fixed_status_1} | set(combo)

                simultaneous_weapons = []
                for w in possible_other_weapons:
                    if w.status_1 in current_target_1s:
                        simultaneous_weapons.append(w)

                results.append({
                    'field_name': field.field_name,
                    'target_1s': current_target_1s,
                    'target_23': target_23,
                    'simultaneous_weapons': simultaneous_weapons
                })

    # 確率がなくなったため、単純に「同時厳選できる武器数が多い順」だけでソート
    results.sort(key=lambda x: len(x['simultaneous_weapons']), reverse=True)

    unique_results = []
    seen_combinations = set()

    for route in results:
        weapon_names = frozenset(type(w).__name__ for w in route['simultaneous_weapons'])
        unique_key = (route['field_name'], weapon_names)

        if unique_key not in seen_combinations:
            seen_combinations.add(unique_key)
            unique_results.append(route)

    return unique_results

# ==========================================
# 3. GUI フレームワーク (表の列や表示から確率を除外)
# ==========================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("武器厳選ルート計算ツール")
        self.geometry("800x550") # 確率列が消えた分、少し横幅をスリムに

        self.weapon_dict = {w.name: w for w in weapon_list}
        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, pady=10, fill=tk.X, padx=10)

        tk.Label(control_frame, text="第1優先武器:").pack(side=tk.LEFT)
        
        self.weapon_var = tk.StringVar()
        self.weapon_combo = ttk.Combobox(control_frame, textvariable=self.weapon_var, state="readonly")
        self.weapon_combo['values'] = list(self.weapon_dict.keys())
        self.weapon_combo.current(0)
        self.weapon_combo.pack(side=tk.LEFT, padx=10)

        calc_btn = tk.Button(control_frame, text="計算する", command=self.on_calculate, bg="#e0e0e0")
        calc_btn.pack(side=tk.LEFT)

        self.list_outer_frame = tk.LabelFrame(self, text="武器ごとの当たり基質ステータス")
        self.list_outer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

        self.canvas = tk.Canvas(self.list_outer_frame, height=130)
        h_scrollbar = ttk.Scrollbar(self.list_outer_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        self.weapons_inner_frame = tk.Frame(self.canvas)
        
        self.weapons_inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.weapons_inner_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=h_scrollbar.set)
        
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Label(self.weapons_inner_frame, text="「計算する」ボタンを押すと、ここに厳選対象の武器が表示されます。", fg="gray").pack(padx=10, pady=30)

        result_frame = tk.Frame(self)
        result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 確率列（primary_prob）を削除
        columns = ("rank", "field", "status1", "status23", "others")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")

        self.tree.heading("rank", text="候補")
        self.tree.heading("field", text="フィールド")
        self.tree.heading("status1", text="ステータス1 (3枠)")
        self.tree.heading("status23", text="ステータス2/3 (1枠)")
        self.tree.heading("others", text="同時厳選可能武器")

        self.tree.column("rank", width=50, anchor=tk.CENTER)
        self.tree.column("field", width=100, anchor=tk.CENTER)
        self.tree.column("status1", width=180, anchor=tk.CENTER)
        self.tree.column("status23", width=120, anchor=tk.CENTER)
        self.tree.column("others", width=250, anchor=tk.W)

        v_scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_weapon_cards(self, display_weapons):
        for widget in self.weapons_inner_frame.winfo_children():
            widget.destroy()

        for w in display_weapons:
            card = tk.Frame(self.weapons_inner_frame, relief=tk.RIDGE, borderwidth=2)
            card.pack(side=tk.LEFT, padx=5, pady=5)
            
            w_name = w.name
            tk.Label(card, text=w_name, font=("", 10, "bold")).pack(padx=10, pady=(5, 0))
            tk.Label(card, text=w.status_1).pack()
            tk.Label(card, text=w.status_2).pack()
            tk.Label(card, text=w.status_3).pack(pady=(0, 5))

    def on_calculate(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_name = self.weapon_var.get()
        primary_weapon = self.weapon_dict[selected_name]

        best_routes = find_best_farming_routes(primary_weapon, weapon_list, field_list)

        if not best_routes:
            self.tree.insert("", tk.END, values=("-", "-", "条件に合致するルートが見つかりませんでした", "-", "-"))
            self.update_weapon_cards([primary_weapon])
            return

        display_weapons = [primary_weapon]
        seen_weapons = {type(primary_weapon).__name__}

        for i, route in enumerate(best_routes[:10]):
            rank = f"{i + 1}"
            field_name = route['field_name']
            status1_str = ", ".join(route['target_1s'])
            status23_str = route['target_23']
            
            sim_weapons = route['simultaneous_weapons']
            if sim_weapons:
                others_list = []
                for w in sim_weapons:
                    w_name = w.name
                    others_list.append(w_name)
                    
                    if w_name not in seen_weapons:
                        seen_weapons.add(w_name)
                        display_weapons.append(w)
                        
                others_str = " / ".join(others_list)
            else:
                others_str = "なし"

            # 確率データなしで表に行を挿入
            self.tree.insert("", tk.END, values=(rank, field_name, status1_str, status23_str, others_str))

        self.update_weapon_cards(display_weapons)

if __name__ == "__main__":
    app = App()
    app.mainloop()