import glob
import re
import os
from collections import defaultdict
from collections import Counter

n = 10

polarities = [
    "+", "-", "+", "-", "+", "-", "+", "-", "+", "-",
    "-", "+", "-", "+", "-", "-", "-", "-", "-", "-",
    "-", "+", "-", "+", "-", "+", "-", "+", "+", "+",
    "+", "-", "+", "-", "+", "-", "+", "-", "+", "+",
    "+", "-", "+", "-", "+", "-", "+", "+", "+", "+" 
]

E = {"High": 50, "Mid High": 40 , "Middle": 30, "Mid Low": 20, "Low": 10}
N = {"High": 50, "Mid High": 40 , "Middle": 30, "Mid Low": 20, "Low": 10}
A = {"High": 50, "Mid High": 40 , "Middle": 30, "Mid Low": 20, "Low": 10}
C = {"High": 50, "Mid High": 40 , "Middle": 30, "Mid Low": 20, "Low": 10}
O = {"High": 50, "Mid High": 40 , "Middle": 30, "Mid Low": 20, "Low": 10}

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
        pattern = r"^[AQ]([1-9]*)\. (.+)$"
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
                score += 6 - int(ans)
        scores.append(score)
        
    big5_list = ["E", "N", "A", "C", "O"]
    big5_scores_dict = dict(zip(big5_list, scores))
    
    return big5_scores_dict


if __name__ == "__main__":
    
    answers_files = glob.glob("api_tokutyogo_en_2/*")
    
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
    