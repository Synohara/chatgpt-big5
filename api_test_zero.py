import openai
import os
import codecs

api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

description = """
もしあなたが各項目について
外向性:{extraversion}
協調性:{agreeableness}
勤勉性:{conscientiousness}
情緒安定性:{neuroticism}
開放性:{openness}
のような性格傾向を持っている場合、次からの質問に
1:全く当てはまらない
2:少し当てはまらない
3:どちらともいえない
4:少し当てはまる
5:とても当てはまる
の5段階評価でどう答えますか。それぞれの質問に対して「Q質問番号. 番号」のように回答してください。
"""

question = """Q1. すぐ友だちを作ることできる
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
Q高い. 様々な物事の構造について分析する
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
Q66. 優れた賞を持っており，優れた賞を活かせる
"""

question_list = question.split('\n')
n = 10

patterns = [
    {"extraversion": "高い", "agreeableness": "高い",
        "conscientiousness": "高い", "neuroticism": "高い", "openness": "高い"},
    {"extraversion": "低い", "agreeableness": "低い",
        "conscientiousness": "低い", "neuroticism": "低い", "openness": "低い"},
    {"extraversion": "普通", "agreeableness": "普通",
        "conscientiousness": "普通", "neuroticism": "普通", "openness": "普通"},
    {"extraversion": "高い", "agreeableness": "低い",
        "conscientiousness": "低い", "neuroticism": "低い", "openness": "高い"},
    {"extraversion": "やや低い", "agreeableness": "普通",
        "conscientiousness": "やや高い", "neuroticism": "高い", "openness": "やや低い"},
]

for pattern in patterns:
    file_name = ""
    for item in pattern.items():
        file_name += item[0][:3] + "_" + item[1] + "_"
    file_name = file_name[:-1] + ".txt"
    # ans = ""
    # for i in range(0, len(question_list), n):
    #     tmp_q = '\n'.join(question_list[i: i+n])
    #     # print(system_settings.format(**pattern) + "\n" + tmp_q)
    #     res = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": system_settings.format(**pattern) + "\n" + tmp_q
    #             }
    #         ],
    #     )
    #     ans += res["choices"][0]["message"]["content"]
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "これからあなたには性格指標を測る質問に答えてもらいます。"
            },
            {
                "role": "user",
                "content": description.format(**pattern)
            },
            {
                "role": "user",
                "content": question
            }
        ],
    )
    print(res["choices"][0]["message"]["content"], file=codecs.open(
        f'api_wiki/{file_name}', 'w', 'utf-8'))
