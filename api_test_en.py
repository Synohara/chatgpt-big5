import openai
import os
import codecs
import itertools

api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key


system_settings = """Characteristics for the main personality indicators are listed below.
Characteristics of a highly extroverted person:
I am a lively person.
I don't mind being the center of attention from everyone.
I feel at home with many people.
I often initiate conversation.
I talk to a lot of different people at parties.
I don't talk much.
I think a lot before I speak or act.
I like to be noticed by everyone around me.
I am willing to talk to strangers when they are around.
I am good at talking in the presence of many people.

Characteristics of a person with high agreeableness:
I am interested in people.
I empathize with others.
I have a kind heart.
I take time for others.
I can feel others' emotions.
I can reassure people without difficulty.
I do not care much about others.
I do not insult others.
I am interested in other people's problems.
I often care about others.

Characteristics of a person with high conscientiousness:
I am always prepared.
I pay attention to details.
I get chores done quickly.
I like order.
I get things done according to plan.
I am driven by work.
I leave things around me alone.
I like to keep things in order.
I neatly put things back where I used them.
I do what needs to be done

Characteristics of a person with high neuroticism:
I get easily irritated.
I am easily stressed.
I get upset easily.
I change my mood frequently.
I tend to worry about things.
I feel much more anxious than most people.
I cannot relax most of the time.
I often feel blue.

Characteristics of a person with high openness:
I have great ideas.
I understand things quickly.
I use difficult words.
I have lots of ideas.
I am interested in abstract things.
I have a rich imagination.
It is easy for me to understand abstract ideas.

If you have the following personality traits for each
Extroversion: {extraversion}
Agreeableness: {agreeableness}
Conscientiousness: {conscientiousness}
Neuroticism: {neuroticism}
Openness: {openness}
If you have the following personality traits, please answer the following questions
On a scale of 1=Disagree, 3=Neutral, 5=Agree, how would you answer the following questions? For each question, Please answer in the form of "Q. Answer Number".
"""


question = """
Q1.	I am the life of the party.
Q2.	I don't talk a lot.
Q3.	I feel comfortable around people.
Q4.	I keep in the background.
Q5.	I start conversations.
Q6.	I have little to say.
Q7.	I talk to a lot of different people at parties.
Q8.	I don't like to draw attention to myself.
Q9.	I don't mind being the center of attention.
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

question_list = question.split('\n')
n = 10

# inp_list = ["Low", "High", "Middle", "Mid Low", "Mid High"]
inp_list = ["Low", "High", "Middle"]

products = list(itertools.product(inp_list, repeat=5))

patterns = [{
    "extraversion": p[0],
    "agreeableness":p[1],
    "conscientiousness": p[2],
    "neuroticism": p[3],
    "openness": p[4]
}
    for p in products]

print(len(patterns))


for pattern in patterns[161:]:
    file_name = ""
    for item in pattern.items():
        file_name += item[0][:3] + "_" + item[1] + "_"
    file_name = file_name[:-1] + ".txt"
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": system_settings.format(**pattern) + "\n" + question
            }
        ],
    )
    ans = res["choices"][0]["message"]["content"]

    print(ans, file=codecs.open(f'api_tokutyogo_en_2/{file_name}', 'w', 'utf-8'))
