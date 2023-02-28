import itertools
import sys
from calc_tipi_j import calc_tipi_j
import codecs
from tenacity import retry
import itertools
import os

from revChatGPT.V1 import Chatbot
from chatgpt_wrapper import ChatGPT


OPENAI_MAIL_ADDRESS = os.environ.get("OPENAI_MAIL_ADDRESS")
OPENAI_PASSWORD = os.environ.get("OPENAI_PASSWORD")
OPENAI_PAID_STATUS = bool(os.environ.get("OPENAI_PAID_STATUS", False))

def main():
    tipi_j_ans_1 = [1, 7, 1, 7, 1, 7, 1, 7, 1, 7]
    tipi_j_ans_2 = [7, 1, 7, 1, 7, 1, 7, 1, 7, 1]

    score_1 = calc_tipi_j(tipi_j_ans_1)
    score_2 = calc_tipi_j(tipi_j_ans_2)

    ans_1 = ""
    for n, a in enumerate(tipi_j_ans_1):
        ans_1 += f"{n+1}. {a}\n"

    ans_2 = ""
    for n, a in enumerate(tipi_j_ans_2):
        ans_2 += f"{n+1}. {a}\n"

    pillow = """    
以下の質問それぞれに
1.  活発で，外向的だと思う
2.  他人に不満をもち，もめごとを起こしやすいと思う
3. しっかりしていて，自分に厳しいと思う
4. 心配性で，うろたえやすいと思う
5. 新しいことが好きで，変わった考えをもつと思う
6.  ひかえめで，おとなしいと思う
7.  人に気をつかう，やさしい人間だと思う
8.  だらしなく，うっかりしていると思う
9.  冷静で，気分が安定していると思う
10. 発想力に欠けた，平凡な人間だと思う
以下の7段階評価
1: 全く違うと思う
2: おおよそ違うと思う
3: 少し違うと思う
4: どちらでもない
5: 少しそう思う
6: まあまあそう思う
7: 強くそう思う
で
{ans_2}と答えた時、
この時の性格傾向は
外向性:高い
協調性:高い
勤勉性:高い
情緒安定性:高い
開放性:高い
です。
また、
{ans_1}と答えた時、
この時の性格傾向は
外向性:低い
協調性:低い
勤勉性:低い
情緒安定性:低い
開放性:低い
です。

ではもしあなたが
外向性:{extraversion}
協調性:{agreeableness}
勤勉性:{conscientiousness}
情緒安定性:{neuroticism}
開放性:{openness}
のような性格傾向を持っている場合次からの質問に
1:全く当てはまらない
2:少し当てはまらない
3:どちらともいえない
4:少し当てはまる
5:とても当てはまる
の5段階評価でどう答えますか。それぞれの質問に対して「Q質問番号. 番号」のように回答ください。
"""

    text = """Q1. すぐ友だちを作ることできる
Q2. 人に会うことは，ワクワクする
Q3. 明るい性格だ
Q4. 交友関係は広い
Q5. 知らない人と話をすることは，苦にならない
Q6. 人と話しをするのが好きだ
Q7. イライラして、相手を怒ることはない
Q8. 八つ当たりはしない
Q9. 細かいことで，くよくよしない
Q10. 小さな事で，悩むことはない
Q11. 感情的に取り乱すことはない
Q12. 感情的な争いはしない
Q13. 決心をしたらやり通す
Q14. いい加減なことはしたくない
Q15. 確実に、こつこつと努力する方だ
Q16. 常に目標を持って行動している
Q17. 何事においてもプロ意識を持って行動している
Q18. 物事は正確に行う
Q19. チームワークを大切にしている
Q20. 自分よりも，仲間を大切にしている
Q21. 友だちと一緒に行動することが多い
Q22. 人と協力して，物事を成し遂げるのが好きだ
Q23. チームワークの方がやりやすい
Q24. 仲間と協力をして，物事を達成する
Q25. 物事の真意を調べることに興味がある
Q26. 社会で役に立つ知識を身につけている
Q27. 他人の優れた特徴を言い当てることが得意だ
Q28. 積極的に、新しい知識を身につける
Q29. 新しい経験を大切にしている
Q30. 様々な物事の構造について分析する
Q31. 劣等感に悩む
Q32. 現実と理想とする自己像が異なっている
Q33. 生きていく自信がない
Q34. 自分のすべきことが見つからない
Q35. 人生の選択で悩む
Q36. 自分自身の長所が見つからない
Q37. 独自性を持ち，創造力を実際に活用できる
Q38. 様々なことに興味・関心を持ち，好奇心を活用できる
Q39. 学ぶことが好きであり，学習したことを活用できる
Q40. 困難なことがあっても，経験や知識を生かして臨機応変に行動できる
Q41. 様々な知識を持っており，知識を活用できる
Q42. 自分の信念を貫き，勇敢に行動できる
Q43. 物事は忍耐強く，最後まで終わらせることができる
Q44. 物事に対して誠実に取り組み，誠実に行動できる
Q45. 熱意を持って，活発的に行動できる
Q46. 他の人に愛情を与えること，他の人から愛情を受け取ることが素直にできる
Q47. 親切な対応ができ，人が困っていたら，積極的に支援できる
Q48. 様々な人の気持ちが理解でき，人とのやり取りがうまくできる
Q49. 他人とチームを組んで活動することで，より成果を高められる
Q50. フェア（公平）な精神をもって，人に接することができる
Q51. リーダーシップを発揮して，グループの目標達成や人間関係を調整できる
Q52. 他人の失敗に対して寛大であり，相手を許せる
Q53. 他人からの意見を素直に受け入れるなど，謙虚に対応できる
Q54. 物事を台無しにしないように慎重に進められる
Q55. 自分自身を統制して，最適な状況を作り出せる
Q56. 自然や美しさなどの本質を見極め，感動や楽しみを見いだせる
Q57. 感謝できることに気づき，感謝を行動で示せる
Q58. 希望を見つけ，未来に向けて希望を構築できる
Q59. 楽しいことを考え，人を楽しませることができる
Q60. 瞑想や祈りをしたりして，精神性を高められる
Q61. 経済的に自立し，経済的な貢献ができる
Q62. 強みとなる資格を持っており，資格を活かせる
Q63. 様々な経験をもっており，経験を活用できる
Q64. 様々な人と連携し，人脈ネットワークを活かせる
Q65. 専門的な技術を持っており，技術を活かせる
Q66. 優れた賞を持っており，優れた賞を活かせる"""

    text_list = text.split('\n')
    n = 10

    # chatbot = Chatbot(config={
    #     "email": OPENAI_MAIL_ADDRESS,
    #     "password": OPENAI_PASSWORD,
    #     "paid": OPENAI_PAID_STATUS
    # })
    chatbot = ChatGPT()

    


    inp_list = ["低い", "高い"]
    products = list(itertools.product(inp_list, repeat=5))

    for p in products:
        if (p[0] == "低い" and p[1] == "高い" and p[2] == "高い" and p[3] == "高い" and p[4] == "高い"):
            chatbot.new_conversation()
            ans = """外向性:{extraversion}
    協調性:{agreeableness}
    勤勉性:{conscientiousness}
    情緒安定性:{neuroticism}
    開放性:{openness}
            """.format(openness=p[0],
                    conscientiousness=p[1],
                    extraversion=p[2],
                    agreeableness=p[3],
                    neuroticism=p[4])
            for i in range(0, len(text_list), n):
                tmp_q = '\n'.join(text_list[i: i+n])

                tmp_ans  = chatbot.ask(pillow.format(ans_1=ans_1,
                                                    ans_2=ans_2,
                                                    openness=p[0],
                                                    conscientiousness=p[1],
                                                    extraversion=p[2],
                                                    agreeableness=p[3],
                                                    neuroticism=p[4]) + tmp_q)
                ans += tmp_ans + "\n"
            print(ans)
            print(ans, file=codecs.open(f'tipi_j_answers/o_{p[0]}_c_{p[1]}_e_{p[2]}_a_{p[3]}_n_{p[4]}.txt', 'w', 'utf-8'))

high = "高い"
low = "低い"


if __name__ == "__main__":
    main()
