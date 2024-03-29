from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from taggit.models import Tag
from userauth.models import User
from .forms import ProductReviewForm

# Create your views here.


def index(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(
        product_status="published", featured=True)
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(
        product_status="published")
    context = {
        'products': products
    }
    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'core/category-list.html', context)


def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(
        product_status="published", category=category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'core/category-product-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors,
    }
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(
        product_status="published", vendor=vendor)

    context = {
        'vendor': vendor,
        'products': products
    }
    return render(request, 'core/vendor-detail.html', context)


def product_detail_view(request, pid):
    product = get_object_or_404(Product, pid=pid)

    related_products = Product.objects.filter(
        category=product.category).exclude(pid=pid)[:4]

    # getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by('-id')

    # getting average review
    average_rating = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))

    # review form
    review_form = ProductReviewForm()
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form

    }
    return render(request, 'core/product-detail.html', context)


def tag_list_view(request, tag_slug=None):
    products = Product.objects.filter(
        product_status="published").order_by('-id')
    tag = 0
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {
        'products': products,
        'tag': tag
    }
    return render(request, 'core/tag.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
        )
    
    context = {
        'user':user.username,
        'review':request.POST['review'],
        'rating':request.POST['rating'],
    }
   
    average_reviews = ProductReview.objects.filter(
        product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
        'bool':True,
        'context':context,
        'average_reviews':average_reviews
        }

    )
