from .models import Article

def common_articles(request):

    return {
        'five_articles': Article.objects.order_by('-date')[:5],
        'two_articles': Article.objects.order_by('-date')[1:3],
        'one_article': Article.objects.order_by('-date')[:1],
        'sixteen_articles': Article.objects.order_by('-date')[4:20],
        'top_articles': Article.objects.order_by('-views_count')[:4],  # Adjusted to return the top 4
        'sport_articles': Article.objects.filter(category='Sports')[:16],
        'two_last_article': Article.objects.filter(category='National News').order_by('-date')[:2],
        'two_last_article1': Article.objects.filter(category='News').order_by('-date')[2:4],
        'categories': Article.objects.values_list('category', flat=True).distinct(),
        'local_news': Article.objects.filter(category='Local News')[:16],
        'national_news': Article.objects.filter(category='National News')[:3],
        'national_news1': Article.objects.filter(category='National News')[3:6],
        'four_last_article': Article.objects.filter(category='News').order_by('-date')[4:8],
        'four_last_article1': Article.objects.filter(category='National News').order_by('-date')[4:8],
        'four_last_article2': Article.objects.filter(category='Local News').order_by('-date')[4:8],
        'four_last_article3': Article.objects.filter(category='Sports').order_by('-date')[4:8],
        
    }
