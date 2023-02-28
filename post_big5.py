import requests
from bs4 import BeautifulSoup
import re
import glob
import codecs
import os

url = "http://www.sinritest.com/bigfive/STRbigfive.php"
init_data = {'q01': '5', 'q02': '5', 'q03': '5', 'q04': '5', 'q05': '5', 'q06': '5', 'q07': '5', 'q08': '5', 'q09': '5', 'q10': '5', 'q11': '5', 'q12': '5', 'q13': '5', 'q14': '5', 'q15': '5', 'q16': '5', 'q17': '5', 'q18': '5', 'q19': '5', 'q20': '5', 'q21': '5', 'q22': '5', 'q23': '5', 'q24': '5', 'q25': '5', 'q26': '5', 'q27': '5', 'q28': '5', 'q29': '5', 'q30': '5', 'q31': '5', 'q32': '5', 'q33': '5', 'q34': '5', 'q35': '5', 'q36': '5', 'q37': '5',
             'q38': '5', 'q39': '5', 'q40': '5', 'q41': '5', 'q42': '5', 'q43': '5', 'q44': '5', 'q45': '5', 'q46': '5', 'q47': '5', 'q48': '5', 'q49': '5', 'q50': '5', 'q51': '5', 'q52': '5', 'q53': '5', 'q54': '5', 'q55': '5', 'q56': '5', 'q57': '5', 'q58': '5', 'q59': '5', 'q60': '5', 'q61': '5', 'q62': '5', 'q63': '5', 'q64': '5', 'q65': '5', 'q66': '5', 'fs01': '1', 'fs02': '20', 'fs03': '13', 'fs04': '7', 'fs05': '3', 'fs06': '4', 'c01': '1', 'c02': '2'}

zeroshot_files = glob.glob("zeroshot_answers/*")
tokutyogo_files = glob.glob("tokutyogo_answers/*")
tipi_j_files = glob.glob("tipi_j_answers/*")


def post_big5(file, save_dir):
    data = init_data.copy()
    with open(file) as f:
        ans = f.read()

    for a in ans.split("\n"):
        pattern = r"^Q([1-9]*)\. (.+)$"
        # 文字列からパターンにマッチする部分を検索
        match = re.search(pattern, a)
        # マッチした部分を取り出す
        if match:
            q_no = match.group(1).zfill(2)
            data[f"q{q_no}"] = match.group(2)
    files = {(None, None)}
    response = requests.post(url, data=data, files=files)
    html = response.content.decode("sjis")
    soup = BeautifulSoup(html, 'html.parser')
    score_trs = soup.find_all('tr')
    result = ""
    input = os.path.splitext(os.path.basename(file))[0].split("_")
    input_ = f"外向性:{input[5]}\n情緒安定性:{input[9]}\n誠実性:{input[3]}\n協調性:{input[7]}\n開放性:{input[1]}"
    input_map = {
        "外向性": input[5],
        "情緒安定性": input[9],
        "誠実性": input[3],
        "協調性": input[7],
        "開放性": input[1]
    }
    # result += "インプットしたBig5\n\n" + input + "\n"
    # result += "------------------------------\n"
    # result += "質問回答からのBig5\n\n"
    result_map = {}
    for tr in score_trs:
        if re.search("[0-9]*点[^）]", tr.text) and len(tr.text) <= 50:
            # result += tr.text.strip().replace("\n", ":").replace(" ",
            #                                                      "").replace("　", "").replace("::", ":") + "\n"
            r = tr.text.strip().replace("\n", ":").replace(
                " ", "").replace("　", "").replace("::", ":").split(":")
            if len(r) == 3:
                result_map[r[0]] = f"{r[2]}({r[1]})" 
    for item in result_map.items():
        if item[0] != "自己ギャップ":
            result += f"{item[0]} 指示:{input_map[item[0]]} 結果:{item[1]}\n"

    print(result, file=codecs.open(
        f'{save_dir}/{os.path.splitext(os.path.basename(file))[0]}_result', 'w', 'utf-8'))
    return result

zeroshot_result = ""
tokutyogo_result = ""
tipi_j_result = ""
for file in zeroshot_files:
    result = post_big5(file, "zeroshot_results")
    zeroshot_result += result + "\n"
    zeroshot_result += "----------------------------\n"
    print(zeroshot_result, file=codecs.open(
        f'zeroshot_results/zeroshot_result', 'w', 'utf-8'))
for file in tokutyogo_files:
    result = post_big5(file, "tokutyogo_results")
    tokutyogo_result += result + "\n"
    tokutyogo_result += "----------------------------\n"
    print(tokutyogo_result, file=codecs.open(
        f'tokutyogo_results/tokutyogo_result', 'w', 'utf-8'))
for file in tipi_j_files:
    result = post_big5(file, "tipi_j_results")
    tipi_j_result += result + "\n"
    tipi_j_result += "----------------------------\n"
    print(tipi_j_result, file=codecs.open(
        f'tipi_j_results/tipi_j_result', 'w', 'utf-8'))
