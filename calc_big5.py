import glob
import re
import os
from collections import defaultdict
from collections import Counter

n = 10

polarities = [
    "+", "-", "+", "-", "+", "-", "+", "-", "+", "-", # E MIN:-20 MAX:20
    "-", "+", "-", "+", "-", "-", "-", "-", "-", "-", # N MIN:-38 MAX:2
    "-", "+", "-", "+", "-", "+", "-", "+", "+", "+", # A MIN:-14 MAX:26
    "+", "-", "+", "-", "+", "-", "+", "-", "+", "+", # C MIN:-14 MAX:26
    "+", "-", "+", "-", "+", "-", "+", "+", "+", "+"  # O MIN:-8  MAX:32
]

E = {"High": 20, "Mid High": 10 , "Middle": 0, "Mid Low": -10, "Low": -20}
N = {"High": 2, "Mid High": -8 , "Middle": -18, "Mid Low": -28, "Low": -38}
A = {"High": 26, "Mid High": 16 , "Middle": 6, "Mid Low": -4, "Low": -14}
C = {"High": 26, "Mid High": 16 , "Middle": 6, "Mid Low": -4, "Low": -14}
O = {"High": 32, "Mid High": 22 , "Middle": 12, "Mid Low": 2, "Low": -8}

score_mapping = {
    "ext": E,
    "neu": N,
    "agr": A,
    "con": C,
    "ope": O
}

def calc_score(answers_file):
    answers_list = []
    scores = []
    with open(answers_file) as f:
        answers = f.read()
    for a in answers.split("\n"):
        pattern = r"^Q([1-9]*)\. (.+)$"
        # 文字列からパターンにマッチする部分を検索
        match = re.search(pattern, a)
        # マッチした部分を取り出す
        if match:
            ans = match.group(2)
            answers_list.append(ans)
    for i in range(0, len(polarities), n):
        
        score = 0
        for item in zip(answers_list[i: i+n], polarities[i: i+n]):
            ans = item[0]
            polarity = item[1]
            if polarity == "+":
                score += int(ans)
            elif polarity == "-":
                score -= int(ans)
        scores.append(score)
        
    big5_list = ["E", "N", "A", "C", "O"]
    big5_scores_dict = dict(zip(big5_list, scores))
    
    return big5_scores_dict


if __name__ == "__main__":
    
    answers_files = glob.glob("api_tokutyogo_en/*")
    
    diff_all = defaultdict(lambda: 0)
    diff_mape_all = defaultdict(lambda: 0)
    for file in answers_files:
        score_dict = calc_score(file)
        lis = os.path.splitext(os.path.basename(file))[0].split("_")
        instructions_dict = {
            "E": score_mapping[lis[0]][lis[1]],
            "A": score_mapping[lis[2]][lis[3]],
            "C": score_mapping[lis[4]][lis[5]],
            "N": score_mapping[lis[6]][lis[7]],
            "O": score_mapping[lis[8]][lis[9]]
        }
        diff_dict = {}
        diff_mape_dict = {}
        for item in score_dict.items():
            diff =  item[1] - instructions_dict[item[0]]
            diff_mape =  abs(item[1] - instructions_dict[item[0]]) /  abs(instructions_dict[item[0]])

            diff_dict[item[0]] = diff
            diff_mape_dict[item[0]] = diff_mape
        print(file)
        print(dict(sorted(score_dict.items())))
        print(dict(sorted(instructions_dict.items())))
        print(dict(sorted(diff_dict.items())))
        
        for item in diff_dict.items(): 
            diff_all[item[0]] += abs(item[1])
        for item in diff_mape_dict.items(): 
            diff_mape_all[item[0]] += item[1]
    print("diff all")
    print(dict(diff_all))
    print("diff mae")
    print(dict(Counter({key : diff_all[key] / 100 for key in diff_all})))
    print("diff mape")
    print(dict(diff_mape_all))
    