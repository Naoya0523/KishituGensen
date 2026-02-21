
import itertools
from Status import *
from weapons import *
from field import *


field_list  = [cls() for cls in Field.__subclasses__()]
weapon_list = [cls() for cls in Weapon.__subclasses__()]

def find_best_farming_routes(primary_weapon: Weapon, weapon_list: list, field_list: list):
    results = []

    # Step 1: 第1優先武器のステータスが全て含まれるフィールドを抽出
    valid_fields = []
    for field in field_list:
        if (primary_weapon.status_1 in field.status_1s and
            primary_weapon.status_2 in field.status_2s and
            primary_weapon.status_3 in field.status_3s):
            valid_fields.append(field)

    for field in valid_fields:
        # Step 2: ステータス2, 3の厳選指定パターン
        target_23_candidates = [primary_weapon.status_2, primary_weapon.status_3]

        for target_23 in target_23_candidates:
            # Step 3: 条件に合う他武器を抽出
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

            # Step 4: ステータス1の残り2枠の最適化
            fixed_status_1 = primary_weapon.status_1
            available_status_1s = field.status_1s - {fixed_status_1}

            candidates = list(available_status_1s)
            if len(candidates) < 2:
                combinations_1 = [tuple(candidates)]
            else:
                combinations_1 = list(itertools.combinations(candidates, 2))

            for combo in combinations_1:
                current_target_1s = {fixed_status_1} | set(combo)

                def calc_probability(w):
                    p1 = 1.0 / 3.0
                    if target_23 == w.status_2:
                        p23 = 1.0 / len(field.status_3s)
                    else:
                        p23 = 1.0 / len(field.status_2s)
                    return p1 * p23

                simultaneous_info = []
                for w in possible_other_weapons:
                    if w.status_1 in current_target_1s:
                        simultaneous_info.append({
                            'weapon': w,
                            'probability': calc_probability(w)
                        })

                results.append({
                    'field_name': field.field_name,
                    'target_1s': current_target_1s,
                    'target_23': target_23,
                    'primary_prob': calc_probability(primary_weapon),
                    'simultaneous_info': simultaneous_info
                })

    # === ここからが追加・変更部分（重複の排除） ===
    # 1. まずは今まで通り、「同時厳選できる武器数」と「確率」でソート
    results.sort(key=lambda x: (len(x['simultaneous_info']), x['primary_prob']), reverse=True)

    # 2. 重複をチェックして、ユニークな結果だけを残す
    unique_results = []
    seen_combinations = set()

    for route in results:
        # このルートで厳選できる他武器の名前のリストを抽出
        # frozenset（変更不可の集合）にすることで、順序を問わず「組み合わせ」として扱えるようにする
        weapon_names = frozenset(type(info['weapon']).__name__ for info in route['simultaneous_info'])

        # 「フィールド名」と「武器の組み合わせ」を判定用のキーにする
        unique_key = (route['field_name'], weapon_names)

        # まだ見たことがない組み合わせ（初登場）ならリストに追加
        if unique_key not in seen_combinations:
            seen_combinations.add(unique_key)
            unique_results.append(route)

    return unique_results