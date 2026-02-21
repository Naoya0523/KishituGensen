
from weapons import *
from selector import *
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("基質厳選くん")
        self.geometry("900x400")

        self.weapon_dict = {w.name: w for w in weapon_list}
        self.create_widgets()

    def create_widgets(self):
        # --- 上部フレーム（入力・操作エリア） ---
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10, fill=tk.X, padx=10)

        tk.Label(control_frame, text="第1優先武器:").pack(side=tk.LEFT)

        self.weapon_var = tk.StringVar()
        self.weapon_combo = ttk.Combobox(control_frame, textvariable=self.weapon_var, state="readonly")
        self.weapon_combo['values'] = list(self.weapon_dict.keys())
        self.weapon_combo.current(0)
        self.weapon_combo.pack(side=tk.LEFT, padx=10)

        calc_btn = tk.Button(control_frame, text="計算する", command=self.on_calculate, bg="#e0e0e0")
        calc_btn.pack(side=tk.LEFT)

        # --- 下部フレーム（結果表示エリア：Treeview） ---
        result_frame = tk.Frame(self)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 表の列（カラム）を定義
        columns = ("rank", "field", "status1", "status23", "others")
        self.tree = ttk.Treeview(result_frame, columns=columns, show="headings")

        # 列の見出しを設定
        self.tree.heading("rank", text="候補")
        self.tree.heading("field", text="フィールド")
        self.tree.heading("status1", text="ステータス1 (3枠)")
        self.tree.heading("status23", text="ステータス2/3 (1枠)")
        #self.tree.heading("primary_prob", text="第1優先確率")
        self.tree.heading("others", text="同時厳選可能武器 (各ドロップ確率)")

        # 列の幅と配置を設定
        self.tree.column("rank", width=50, anchor=tk.CENTER)
        self.tree.column("field", width=100, anchor=tk.CENTER)
        self.tree.column("status1", width=180, anchor=tk.CENTER)
        self.tree.column("status23", width=120, anchor=tk.CENTER)
        #self.tree.column("primary_prob", width=90, anchor=tk.CENTER)
        self.tree.column("others", width=300, anchor=tk.W) # 左寄せ

        # スクロールバーの追加
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_calculate(self):
        # 表（Treeview）の中身を一旦すべてクリア
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_name = self.weapon_var.get()
        primary_weapon = self.weapon_dict[selected_name]

        best_routes = find_best_farming_routes(primary_weapon, weapon_list, field_list)

        if not best_routes:
            # 該当なしの場合は空行を1つ入れてメッセージ表示
            self.tree.insert("", tk.END, values=("-", "-", "条件に合致するルートが見つかりませんでした", "-", "-", "-"))
            return

        # 表にデータを挿入
        for i, route in enumerate(best_routes[:10]): # 最大10候補まで表示
            rank = f"{i + 1}"
            field_name = route['field_name']

            # ステータスのセットを見やすい文字列に変換 ("敏捷, 筋力, 意思" など)
            status1_str = ", ".join(route['target_1s'])
            status23_str = route['target_23']

            # 第1優先の確率
            p_prob_str = f"{route['primary_prob'] * 100:.2f}%"

            # 他武器の情報を1つの文字列にまとめる ("Kagami(4.17%) / TestWeapon1(4.17%)" など)
            sim_info = route['simultaneous_info']
            if sim_info:
                others_list = [f"{info['weapon'].name}" for info in sim_info]
                others_str = " / ".join(others_list)
            else:
                others_str = "なし"

            # 行を追加
            self.tree.insert("", tk.END, values=(rank, field_name, status1_str, status23_str, others_str))

if __name__ == "__main__":
    app = App()
    app.mainloop()