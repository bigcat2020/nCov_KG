from django.shortcuts import HttpResponse, render
from modl.kgqa import parser
from modl.nlpltp import pltobj
from modl.answer import answer


def answering(request):
    if request.GET:
        text = request.GET.get("question", "")
        typ = parser.parse_question(text)

        print("类型", typ)

        # if typ == "未知":
        #     # 直接返回抱歉
        #     return render(request, 'question_answering.html', {'ret': "抱歉，无法识别该问题"})

        # if typ == "实体":
        #     ans = answer.zs_answer(text)
        #     print(ans)
        #     return render(request, 'question_answering.html', {'ret': ans})
        #     pass

        # if typ == "知识":
        #     list_st = pltobj.get_keywords(text)
        #     print(list_st)
        #     pass
        try:
            if typ == "疫情":

                ans = answer.yq_answer(text)
                if ans:
                    return render(request, 'question_answering.html', {'ret': {'answer': ans}})

            else:
                ans = answer.zs_answer(text)
                if ans:
                    return render(request, 'question_answering.html', {'ret': {'answer': ans}})
        except:
            return render(request, "question_answering.html", {'ctx': 1})

        return render(request, "question_answering.html", {'ctx': 1})
    else:
        return render(request, "question_answering.html")


