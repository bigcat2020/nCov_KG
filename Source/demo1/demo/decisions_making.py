from django.shortcuts import render


def decisions_china(request):

    return render(request, "china_map.html")


def decisions_word(request):
    return render(request, "word_map.html")