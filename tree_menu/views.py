from django.shortcuts import render

def index(request):
    return render(request, 'tree_menu/index.html')

def page1(request):
    return render(request, 'tree_menu/page1.html')

def page1_2(request):
    return render(request, 'tree_menu/page1_2.html')

def page2(request):
    return render(request, 'tree_menu/page2.html')

def page3(request):
    return render(request, 'tree_menu/page3.html')
