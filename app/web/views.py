import requests
from django.shortcuts import render
from django.core.paginator import Paginator


def index(request):
    find_faq = None
    search_query = request.GET.get('search', '')  # Получаем поисковый запрос

    try:
        find_faq = requests.get('http://127.0.0.1:8228/api/').json()

        # Фильтруем FAQ по поисковому запросу
        if search_query:
            find_faq = [faq for faq in find_faq if
                        search_query.lower() in faq['question'].lower() or search_query.lower() in faq[
                            'answer'].lower()]

        # Пагинация
        page_number = request.GET.get('page', 1)  # Номер страницы из GET-параметра
        paginator = Paginator(find_faq, 20)  # Создаем объект Paginator с лимитом 20
        current_page = paginator.get_page(page_number)  # Получаем текущую страницу

    except requests.exceptions.RequestException as e:
        print("Ошибка при запросе к API:", e)

    context = {
        'find_faq': current_page,
        'search_query': search_query,  # Передаем поисковый запрос
        'paginator': paginator,  # Передаем объект Paginator
    }

    return render(request, 'web/index.html', context)