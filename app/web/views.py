import requests
from django.shortcuts import render
from django.core.paginator import Paginator


def index(request):
    search_query = request.GET.get('search', '')
    selected_category = request.GET.get('category', '')
    clear_url = 'http://127.0.0.1:8228'
    base_url = clear_url + '/api/'
    find_faq = []

    if selected_category:
        api_url = f'{base_url}{selected_category}/'
    else:
        api_url = base_url

    print("Запрос к API:", api_url)

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        find_faq = response.json()

        for faq in find_faq:
            if 'question_image' in faq:
                if not faq['question_image'].startswith('http'):
                    faq['question_image'] = clear_url + faq['question_image']

            if 'answer_image' in faq:
                if not faq['answer_image'].startswith('http'):
                    faq['answer_image'] = clear_url + faq['answer_image']

        if search_query:
            find_faq = [faq for faq in find_faq if
                        search_query.lower() in faq['question'].lower() or
                        search_query.lower() in faq['answer'].lower()]

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

