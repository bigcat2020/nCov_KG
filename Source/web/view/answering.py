from django.shortcuts import render
from modl.answer import answer
from modl.classify import QuestionClassify

cla = QuestionClassify()


def answering(request):
    if request.GET:
        text = request.GET.get("question", "")

        typ = cla.get_question_type(text)

        print("类型", typ)

        try:
            if typ == 1:  # "疫情":
                ans = answer.yq_answer(text)
                if ans:
                    return render(request, 'question_answering.html', {'ret': {'answer': ans}})

            elif typ == 2:  # 知识
                ans = answer.zs_answer(text)
                if ans:
                    return render(request, 'question_answering.html', {'ret': {'answer': ans}})
        except:
            return render(request, "question_answering.html", {'ctx': 1})

        return render(request, "question_answering.html", {'ctx': 1})
    else:
        return render(request, "question_answering.html")


