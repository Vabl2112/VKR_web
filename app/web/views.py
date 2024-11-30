import requests
from django.shortcuts import render
from django.core.paginator import Paginator

def index(request):
    find_faq = []
    search_query = request.GET.get('search', '')  # Получаем поисковый запрос
    selected_category = request.GET.get('category', '')  # Получаем выбранную категорию
    base_url = 'http://127.0.0.1:8228/api/'
    clear_url = 'http://127.0.0.1:8228'

    if selected_category:
        api_url = f'{base_url}{selected_category}/'
    else:
        api_url = base_url

    print("Запрос к API:", api_url)

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Поднимаем исключение для статусов 4xx/5xx
        find_faq = response.json()

        if search_query:
            find_faq = [faq for faq in find_faq if
                        search_query.lower() in faq['question'].lower() or search_query.lower() in faq['answer'].lower()]

        page_number = request.GET.get('page', 1)
        paginator = Paginator(find_faq, 20)
        current_page = paginator.get_page(page_number)

    except requests.exceptions.RequestException as e:
        print("Ошибка при запросе к API:", e)

    context = {
        'clear_url': clear_url,
        'find_faq': current_page,
        'search_query': search_query,
        'selected_category': selected_category,
        'paginator': paginator,
    }
    print(context)
    return render(request, 'web/index.html', context)

