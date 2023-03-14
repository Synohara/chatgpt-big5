import openai
import os
import codecs
import itertools
import random
import re
from collections import defaultdict
from collections import Counter
from openai.error import RateLimitError
api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

system_settings = """Please answer the following questions
On a scale of 1=Disagree, 3=Neutral, 5=Agree, how would you answer the following questions? For each question, Please answer in the form of "Q. Answer Number".
"""

polarities = [
    "+", "-", "+", "-", "+", "-", "+", "-", "+", "-",
    "-", "+", "-", "+", "-", "-", "-", "-", "-", "-",
    "-", "+", "-", "+", "-", "+", "-", "+", "+", "+",
    "+", "-", "+", "-", "+", "-", "+", "-", "+", "+",
    "+", "-", "+", "-", "+", "-", "+", "+", "+", "+"
]
question = """Q1. I am the life of the party.
Q2. I don't talk a lot.
Q3. I feel comfortable around people.
Q4. I keep in the background.
Q5. I start conversations.
Q6. I have little to say.
Q7. I talk to a lot of different people at parties.
Q8. I don't like to draw attention to myself.
Q9. I don't mind being the center of attention.
Q10. I am quiet around strangers.
Q11. I get stressed out easily.
Q12. I am relaxed most of the time.
Q13. I worry about things.
Q14. I seldom feel blue.
Q15. I am easily disturbed.
Q16. I get upset easily.
Q17. I change my mood a lot.
Q18. I have frequent mood swings.
Q19. I get irritated easily.
Q20. I often feel blue.
Q21. I feel little concern for others.
Q22. I am interested in people.
Q23. I insult people.
Q24. I sympathize with others' feelings.
Q25. I am not interested in other people's problems.
Q26. I have a soft heart.
Q27. I am not really interested in others.
Q28. I take time out for others.
Q29. I feel others' emotions.
Q30. I make people feel at ease.
Q31. I am always prepared.
Q32. I leave my belongings around.
Q33. I pay attention to details.
Q34. I make a mess of things.
Q35. I get chores done right away.
Q36. I often forget to put things back in their proper place.
Q37. I like order.
Q38. I shirk my duties.
Q39. I follow a schedule.
Q40. I am exacting in my work.
Q41. I have a rich vocabulary.
Q42. I have difficulty understanding abstract ideas.
Q43. I have a vivid imagination.
Q44. I am not interested in abstract ideas.
Q45. I have excellent ideas.
Q46. I do not have a good imagination.
Q47. I am quick to understand things.
Q48. I use difficult words.
Q49. I spend time reflecting on things.
Q50. I am full of ideas.
"""

# 元
ocean_list = ["E" for i in range(10)] + ["N" for i in range(10)] + [
    "A" for i in range(10)] + ["C" for i in range(10)] + ["O" for i in range(10)]

mean_dict = defaultdict(lambda: 0)
count = 0
for i in range(30):
    if count == 10:
        break
    # ランダマイズ
    question_list = list(zip(question.split("\n"), polarities, ocean_list))
    random.shuffle(question_list)
    pattern = "I.+\."
    question_randamized = "\n".join([f"Q{n+1}. " + re.search(pattern, q[0]).group(0) for n, q in enumerate(question_list)])
    polarities_randamized = [q[1] for q in question_list]
    ocean_list_randamized = [q[2] for q in question_list]
    
    file_name = f"not_configured_answer_{i+1}.txt"
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": system_settings + "\n" + question_randamized
                }
            ],
        )
        ans = res["choices"][0]["message"]["content"]
    except Exception as e:
        print(e)
        continue

    print(ans, file=codecs.open(
        f'api_tokutyogo_en_not_configured/{file_name}', 'w', 'utf-8'))
    
    ans_list = ans.split("\n")
    scores = []
    for a in ans_list:
        if re.search(r"^[AQ][0-9]*\. (.+)$", a):
            score = re.search(r"^[AQ][0-9]*\. (.+)$", a).group(1)
            scores.append(score)
    score_dict = defaultdict(lambda: 0)
    for s in zip(scores, polarities_randamized, ocean_list_randamized):
        score = s[0]
        polarity = s[1]
        ocean = s[2]
        try:
            int(score)
        except:
            continue
        
        if polarity == "+":
            score_dict[ocean] += int(score)
        elif polarity == "-":
            score_dict[ocean] += 6 - int(score)
    print(dict(sorted(dict(score_dict).items())))
    if score_dict == {}:
        continue
    for key in score_dict.keys():
        mean_dict[key] += score_dict[key]
    count += 1
    

print(dict(Counter({key : mean_dict[key] / 10 for key in mean_dict})))