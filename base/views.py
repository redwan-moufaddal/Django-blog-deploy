from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from .forms import RegisterForm ,CommentForm
from django.contrib import messages
from .models import *
import time
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.db.models import Case, IntegerField, Value, When
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import quote, urlencode
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


def register(request):
    if request.user.is_authenticated:
        return redirect('base:home')  # Redirect to home page if already logged in
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                pass1 = password=form.cleaned_data['password1']
                pass2 = password=form.cleaned_data['password2']
                country = form.cleaned_data['country']
                
                if not CustomUser.objects.filter(email=email).exists():
                    if pass1 == pass2 :
                            city = form.cleaned_data['city']
                            first_name = form.cleaned_data['first_name']
                            last_name = form.cleaned_data['last_name']
                            gender = request.POST.get('gender')
                            
                            # Create a new user instance
                            user = CustomUser.objects.create_user(
                                email=form.cleaned_data['email'],
                                password=form.cleaned_data['password1'],
                                first_name=first_name,
                                last_name=last_name,
                                city=city,
                                gender=gender,
                                country=country
                            )
                            user.save()
                            return redirect('base:login')
                    else:
                        messages.error(request, 'Passwords do not match.')
                else:
                    messages.error(request, 'This email address is already in use.')
            else:
                pass
        else:
            form = RegisterForm()  # Create new form instance
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Check if the user has exceeded the login attempts within 15 seconds
        login_attempts = request.session.get('login_attempts', 0)
        last_login_time = request.session.get('last_login_time', 0)
        current_time = time.time()

        if current_time - last_login_time > 15:
            login_attempts = 0  # Reset login attempts if it's been more than 15 seconds
        request.session['last_login_time'] = current_time

        if login_attempts >= 4:
            messages.error(request, f"You have exceeded the maximum login attempts. Please try again in ")
            return render(request, 'registration/login.html',{'count':True})

        if not any(char in email for char in ["'", '"', "-"]) or any(char in password for char in ["'", '"']):
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                request.session['login_attempts'] = 0  # Reset login attempts on successful login
                return redirect('base:home')
            else:
                try:
                    user = CustomUser.objects.get(email=email)
                    if not check_password(password, user.password):
                        messages.error(request, 'Incorrect password.')
                        return render(request, 'registration/login.html',{'email':email})
                except CustomUser.DoesNotExist:
                    messages.error(request, 'No account found with this email.')
                    return render(request, 'registration/login.html',{'all':True})
                login_attempts += 1
                request.session['login_attempts'] = login_attempts
                
        else:
            messages.error(request, "Password cannot contain ' or \" or -")
    return render(request, 'registration/login.html')

def logout_user(request):
    logout(request)
    return redirect('base:login')

def home_page(request):
    top_articles = Article.objects.order_by('-views_count')[:4]
    return render(request, 'homepage-v1.html', {'top_articles': top_articles})

def blog_style1_page(request):
    all_articles = Article.objects.all().order_by('-date')
    paginator = Paginator(all_articles, 15)  # Show 10 articles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'category-style-v1.html', context)


def blog_style2_page(request):
    all_articles = Article.objects.all().order_by('-date')
    paginator = Paginator(all_articles, 14)  # Show 10 articles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Split the articles in the current page into two halves
    first_half = page_obj[:7]
    second_half = page_obj[7:]

    context = {
        'page_obj': page_obj,
        'first_half': first_half,
        'second_half': second_half,
    }
    return render(request, 'category-style-v2.html', context)

def article_detail(request,aid,title):
    article = get_object_or_404(Article, aid=aid)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Save name and email in cookies
            response = HttpResponseRedirect(f"{reverse('base:article_detail', kwargs={'title': title, 'aid': aid})}#comments")
            response.set_cookie('comment_name', name)
            response.set_cookie('comment_email', email)

            BlogReview.objects.create(
                article=article,
                name=name,
                email=email,
                message=comment
            )
            return response
    reviews = article.reviews.all()  # Accessing related reviews using the related_name
    #keywords = article.keywords.split(',')
    key = article.keywords
    key = key.replace("'", "").replace('"', "")
    keywords = key.split(',')
    blog = article
    share_url = reverse('base:article_detail', kwargs={'title': blog.title, 'aid': aid})
    encoded_url = quote(share_url, safe='')
    twitter_share_url = f"https://twitter.com/intent/tweet?url=https://redblog.link{encoded_url}&text={article.title}"
    facebook_share_url = f"https://www.facebook.com/sharer/sharer.php?u=https://redblog.link{encoded_url}"
    telegram_share_url = f"https://t.me/share/url?url=https://redblog.link{encoded_url}&text={article.title}"
    whatsapp_share_url = f"https://api.whatsapp.com/send?text={article.title} - https://redblog.link{encoded_url}"
    linkedin_share_url = f"https://www.linkedin.com/shareArticle?url=https://redblog.link{encoded_url}&title={article.title}"

    # Create a dictionary with the platform names and their respective share URLs
    share_links = {
        'Twitter': twitter_share_url,
        'Facebook': facebook_share_url,
        'Telegram': telegram_share_url,
        'WhatsApp': whatsapp_share_url,
        'LinkedIn': linkedin_share_url
    }
    
    random_article1 = Article.objects.order_by('?').first()
    random_article2 = Article.objects.order_by('?').first()

    if 'visited_article_{}'.format(aid) not in request.session:
        # If not set, increase the views count and set the session variable
        article.views_count += 1
        article.save()
        request.session['visited_article_{}'.format(aid)] = True

    # Fetch the name and email from cookies if they exist
    name_from_cookie = request.COOKIES.get('comment_name', '')
    email_from_cookie = request.COOKIES.get('comment_email', '')
    form = CommentForm(initial={'name': name_from_cookie, 'email': email_from_cookie})
    context = {
            'article': article,
            'reviews': reviews,
            'keywords':keywords,
            'share_links':share_links,
            'form':form,
            'all_comment':reviews,
            'random_article1':random_article1,
            'random_article2':random_article2
    }
    return render(request, 'article-detail-v3.html', context)

def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')

        # Send email (example)
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
            )
        # Save name and email in cookies
        response = HttpResponse(render(request, 'contact.html'))
        response.set_cookie('contact_name', name)
        response.set_cookie('contact_email', email)

        msg = 'Thank you for your message!'
        # Optionally, redirect the user to a thank you page
        return response
    name_from_cookie = request.COOKIES.get('contact_name', '')
    email_from_cookie = request.COOKIES.get('contact_email', '')

    return render(request, 'contact.html', {'name_from_cookie': name_from_cookie, 'email_from_cookie': email_from_cookie})

def about_page(request):
    return render(request, 'about-us.html')

def error(request,exception):
    return render(request, '404.html', status=404)


def articles_by_category(request, category):
    all_articles = Article.objects.filter(category=category).order_by('-date')
    paginator = Paginator(all_articles, 14)  # Show 14 articles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Split the articles in the current page into two halves
    first_half = page_obj[:7]
    second_half = page_obj[7:]

    context = {
        'page_obj': page_obj,
        'first_half': first_half,
        'second_half': second_half,
        'category': category,
    }
    return render(request, 'category-style-v1.html', context)

def search_results(request):
    query = request.GET.get('q')  # Retrieve the search query from the request
    
    if query:
        results = Article.objects.filter(title__icontains=query)  # Adjust field name according to your Article model
    else:
        results = Article.objects.none()  # Return an empty queryset if no query is provided



    context = {
        'query': query,
        'page_obj': results,
    }
    return render(request, 'category-style-v1.html', context)