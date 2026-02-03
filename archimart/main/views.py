from django.template.response import TemplateResponse
from .models import *
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Prefetch
from .tasks import send_appointment_email
import logging,json
# import requests
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)  # Add at top of file
# Create your views here.

def home(request):
    return TemplateResponse(request, 'archimart/index.html')


def construction(request):
    return TemplateResponse(request, 'archimart/construction.html')

def cart(request):
    return TemplateResponse(request, 'archimart/cart.html')

def compare(request):
    return TemplateResponse(request, 'archimart/compare.html')

def detail(request):
    return TemplateResponse(request, 'archimart/product.html')

def grant_token(app_key, app_secret, username, password):

    cache_key = f"bkash_token:{app_key}:{username}"
    token = cache.get(cache_key)
    if token:
        return token

    url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/token/grant'
    headers = {
        'Content-Type': 'application/json',
        'username': username,
        'password': password,
    }
    data = {
        'app_key': app_key,
        'app_secret': app_secret,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        response.raise_for_status()
        response_data = response.json()
        token = response_data.get('id_token')
        if token:
            # Cache token for 1 hour
            cache.set(cache_key, token, 3600)
        return token
    except Exception as e:
        logger.exception("Failed to obtain bKash token: %s", e)
        return None

def bkash_payment(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    token = grant_token(
        settings.BKASH_APP_KEY,
        settings.BKASH_APP_SECRET,
        settings.BKASH_USERNAME,
        settings.BKASH_PASSWORD
    )
    url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create'
    headers = {
        'Authorization': token,
        'X-APP-Key': settings.BKASH_APP_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        'mode': '0011',
        'payerReference': data_json.get('invoice'),
        'callbackURL': 'https://archimart.com/bkash-callback/0',
        'amount': str(data_json.get('amount')),
        'currency': 'BDT',
        'intent': 'sale',
        'merchantInvoiceNumber': data_json.get('invoice'),
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    return response_data
    # return JsonResponse({'token': token})



def search_data(request):
    json = {

        "count": 2,

        "num_pages": 2,

        "current_page": 1,

        "has_next": True,

        "has_previous": False,

        "results": [

        {

        "id": 1,

        "title": "Modern Apartment in Uttara Sector-7",

        "location": "Uttara Sector-7, Dhaka",

        "price": 35000,

        "bedrooms": 3,

        "bathrooms": 2,

        "area": 1200,

        "type": "Apartment",

        "images": [

            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop",

        "features": ["Parking", "Gym", "Security", "Generator", "Swimming Pool"],

        "description": "Beautiful modern apartment with all amenities in prime Uttara location. Perfect for families with spacious rooms and contemporary design."

        },


        {

        "id": 2,

        "title": "Luxury Villa in Banani",

        "location": "Banani, Dhaka",

        "price": 85000,

        "bedrooms": 4,

        "bathrooms": 3,

        "area": 2200,

        "type": "Villa",

        "images": [

            "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=300&fit=crop",

        "features": ["Swimming Pool", "Garden", "Parking", "Security", "Gym"],

        "description": "Spacious luxury villa in the heart of Banani with premium amenities and modern architecture."

        },

        {

        "id": 3,

        "title": "Cozy Studio in Dhanmondi 15",

        "location": "Dhanmondi 15, Dhaka",

        "price": 18000,

        "bedrooms": 1,

        "bathrooms": 1,

        "area": 650,

        "type": "Studio",

        "images": [

            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1560448075-bb485b067938?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400&h=300&fit=crop",

        "features": ["Furnished", "AC", "Internet", "Security"],

        "description": "Perfect studio apartment for young professionals in Dhanmondi with modern furnishing."

        },

        {

        "id": 4,

        "title": "Family Home in Bashundhara R/A",

        "location": "Bashundhara R/A, Dhaka",

        "price": 65000,

        "bedrooms": 4,

        "bathrooms": 3,

        "area": 1800,

        "type": "House",

        "images": [

            "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400&h=300&fit=crop",

        "features": ["Garden", "Garage", "Security", "Playground"],

        "description": "Spacious family home in well-planned Bashundhara residential area."

        },

        {

        "id": 5,

        "title": "Modern Flat in Mirpur-10",

        "location": "Mirpur-10, Dhaka",

        "price": 28000,

        "bedrooms": 2,

        "bathrooms": 2,

        "area": 900,

        "type": "Apartment",

        "images": [

            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop",

        "features": ["Lift", "Security", "Backup Power"],

        "description": "Well-maintained apartment in developing Mirpur area."

        },

        {

        "id": 6,

        "title": "Heritage Property in Old Dhaka",

        "location": "Wari, Old Dhaka",

        "price": 22000,

        "bedrooms": 3,

        "bathrooms": 2,

        "area": 1100,

        "type": "Traditional",

        "images": [

            "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400&h=300&fit=crop",

        "features": [

            "Traditional Architecture",

            "Central Location",

            "Heritage Value"

        ],

        "description": "Beautiful traditional property in historic Old Dhaka area."

        },
        {

        "id": 7,

        "title": "Modern Apartment in Uttara Sector-7",

        "location": "Uttara Sector-7, Dhaka",

        "price": 35000,

        "bedrooms": 3,

        "bathrooms": 2,

        "area": 1200,

        "type": "Apartment",

        "images": [

            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop",

            "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?w=800&h=600&fit=crop"

        ],

        "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop",

        "features": ["Parking", "Gym", "Security", "Generator", "Swimming Pool"],

        "description": "Beautiful modern apartment with all amenities in prime Uttara location. Perfect for families with spacious rooms and contemporary design."

        },

        ]

        }
    return JsonResponse(json)


def search_products(request):
    query = request.GET.get("q", "").strip()
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 10)

    logger.info("search_products called: q=%s page=%s per_page=%s user=%s",
                query, page_number, per_page, getattr(request, "user", None))

    # If per_page is a numeric string or int, cap it to 50 without raising exceptions
    if isinstance(per_page, str) and per_page.isdigit():
        per_page = min(int(per_page), 50)
        logger.debug("per_page normalized from string to %s", per_page)
    elif isinstance(per_page, int):
        per_page = min(per_page, 50)
        logger.debug("per_page normalized from int to %s", per_page)
    try:
        per_page = int(per_page)
        if per_page <= 0:
            logger.warning("per_page <= 0, resetting to default 10 (received: %s)", per_page)
            per_page = 10
    except (TypeError, ValueError):
        logger.warning("Invalid per_page value, resetting to default 10 (received: %s)", per_page)
        per_page = 10

    try:
        if query:
            logger.info("Performing search for query: %s", query)
            products_qs = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).distinct().order_by("id")
        else:
            logger.info("No query provided, returning all products")
            products_qs = Product.objects.all().order_by("id")

        paginator = Paginator(products_qs, per_page)
        page_obj = paginator.get_page(page_number)

        logger.info("Pagination: total=%s pages=%s current=%s per_page=%s",
                    paginator.count, paginator.num_pages, page_obj.number, per_page)

        results = []
        for product in page_obj.object_list:
            results.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "discount": product.discount,
                "currency": product.currency,
                "description": product.description,
                "recomended_title": getattr(product, "recomended_title", None),
                "recomended_text": getattr(product, "recomended_text", None),
                "category": product.subsubcategory.subcategory.category.name if getattr(product, "subsubcategory", None) else None,
                "subcategory": product.subsubcategory.subcategory.name if getattr(product, "subsubcategory", None) else None,
                "subsubcategory": product.subsubcategory.name if getattr(product, "subsubcategory", None) else None,
                "specifications": getattr(product, "Specification", None),
                "images": [
                    request.build_absolute_uri(img.url)
                    for img in (product.image1, product.image2, product.image3)
                    if img and getattr(img, "url", None)
                ],
            })

        logger.debug("Returning %s results for current page", len(results))

        data = {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "results": results,
        }
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.exception("Error in search_products: %s", e)
        return JsonResponse({"error": "Internal server error"}, status=500)

def get_paginated_products(request,page_number, per_page, category=None, sub_category=None, sub_sub_category=None):
    products_qs = Product.objects.prefetch_related(
        "product_color_set","product_size_set","product_thickness_set","similar_products","specification_set"
    ).order_by("id")
    # Apply filters if provided
    if sub_sub_category:
        logger.info("Subsubcategory filter: %s", sub_sub_category)
        products_qs = products_qs.filter(subsubcategory__name__iexact=sub_sub_category)
        logger.info("Subsubcategory filter: %s", products_qs.count())
    elif sub_category:
        logger.info("Subcategory filter: %s", sub_category)
        products_qs = products_qs.filter(subsubcategory__subcategory__name__iexact=sub_category)
    
    elif category:
        logger.info("Category filter: %s", category)
        products_qs = products_qs.filter(subsubcategory__subcategory__category__name__iexact=category)
    
    paginator = Paginator(products_qs, per_page)
    page_obj = paginator.get_page(page_number)

    results = []
    for product in page_obj.object_list:
        results.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "discount": product.discount,
            "description": product.description,
            "images": [
                request.build_absolute_uri(img.url)
                for img in (product.image1, product.image2, product.image3)
                if img and getattr(img, "url", None)
            ],
            "colors": [
                {
                    "color": p_color.color,
                    "images": [
                        request.build_absolute_uri(img.url)
                        for img in [p_color.image1, p_color.image2, p_color.image3]
                        if img and getattr(img, "url", None)
                    ],
                    "stock": p_color.stock,
                    "price": p_color.price,
                }
                for p_color in product.product_color_set.all()
            ],
            "sizes": [
                {
                    "size": p_size.size,
                    "stock": p_size.stock,
                    "price": p_size.price,
                    "images": [
                        request.build_absolute_uri(img.url)
                        for img in [p_size.image1, p_size.image2, p_size.image3]
                        if img and getattr(img, "url", None)
                    ],
                }
                for p_size in product.product_size_set.all()
            ],

            
            
        })

    return {
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "products": results,
    }

def json_file(request):
    category = request.GET.get("category")
    sub_category = request.GET.get("subcategory")
    sub_sub_category = request.GET.get("subsubcategory")
    page_number = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 12))
    
    data = get_paginated_products(
        request,page_number, per_page, category, sub_category, sub_sub_category
    )
    return JsonResponse(data, safe=False)


# def get_similar_products(request):
#     sub_id = request.GET.get("product_id")
#     option = request.GET.get("option")
#     print (sub_id, option)
#     if sub_id:
#         sub_id = sub_id.split(",")
#         # For each product id, get its most expensive similar product
#         result = []
#         for pid in sub_id:
#             try:
#                 product = Product.objects.get(id=pid)
#                 if option == "high":
#                     similar = product.similar_products.all().order_by("-price").first()
#                     if similar and similar.price > product.price:
#                         pass
#                     else:
#                         similar = None
#                 elif option == "low":
#                     similar = product.similar_products.all().order_by("price").first()
#                     if similar and similar.price < product.price:
#                         pass
#                     else:
#                         similar = None

#                 if similar:
#                     result.append({
#                         "product_id": product.id,
#                         "product_name": product.name,
#                         "price": product.price,
#                         "discount": product.discount,
#                         "alternate": {
#                             "id": similar.id,
#                             "name": similar.name,
#                             "price": similar.price,
#                             "discount": similar.discount,
#                         }
#                     })
#                 else:
#                     result.append({
#                         "product_id": product.id,
#                         "product_name": product.name,
#                         "price": product.price,
#                         "discount": product.discount,
#                         "alternate": None
#                     })
#             except Product.DoesNotExist:
#                 continue
#         data = result
#     else:
#         data = []
#     return JsonResponse(data, safe=False)


def get_similar_products(request):
    """AJAX endpoint for the dual-listbox.

    Expects GET params:
      - subsubcategory_id: id of SubSubCategory to list products from
      - current_id: optional id of current product to exclude

    Returns a JSON list of objects with `id` and `name`.
    """
    sub_id = request.GET.get("subsubcategory_id")
    current_id = request.GET.get("current_id")

    if not sub_id:
        return JsonResponse([], safe=False)

    try:
        qs = Product.objects.filter(subsubcategory_id=sub_id)
        if current_id:
            qs = qs.exclude(id=current_id)
        qs = qs.order_by("name")
        data = list(qs.values("id", "name"))
    except Exception as e:
        logger.exception("ajax_similar_products error: %s", e)
        data = []

    return JsonResponse(data, safe=False)

def single_product(request, pk):
    try:
        product = Product.objects.prefetch_related(
            "product_color_set","product_size_set","product_thickness_set","similar_products","specification_set"
        ).get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

    data = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "discount": product.discount,
        "currency": product.currency,
        "description": product.description,
        "recomended_title": product.recomended_title,
        "recomended_text": product.recomended_text,
        "category": product.subsubcategory.subcategory.category.name,
        "subcategory": product.subsubcategory.subcategory.name,
        "subsubcategory": product.subsubcategory.name,
        'specifications': product.Specification,
        "images": [
            request.build_absolute_uri(img.url)
            for img in (product.image1, product.image2, product.image3)
            if img and getattr(img, "url", None)
        ],
        "colors": [
            {
                "color": p_color.color,
                "images": [
                    request.build_absolute_uri(img.url)
                    for img in [p_color.image1, p_color.image2, p_color.image3]
                    if img and getattr(img, "url", None)
                ],
                "stock": p_color.stock,
                "price": p_color.price,
            }
            for p_color in product.product_color_set.all()
        ],
        "sizes": [
            {
                "size": p_size.size,
                "stock": p_size.stock,
                "price": p_size.price,
                "images": [
                    request.build_absolute_uri(img.url)
                    for img in [p_size.image1, p_size.image2, p_size.image3]
                    if img and getattr(img, "url", None)
                ],
            }
            for p_size in product.product_size_set.all()
        ],
        "thicknesses": [
            {
                "thickness": p_thickness.thickness,
                "stock": p_thickness.stock,
                "price": p_thickness.price,
                "images": [
                    request.build_absolute_uri(img.url)
                    for img in [p_thickness.image1, p_thickness.image2, p_thickness.image3]
                    if img and getattr(img, "url", None)
                ],
            }
            for p_thickness in product.product_thickness_set.all()
        ],
        "similar_products": [
            {
                "id": sp.id,
                "name": sp.name,
                "price": sp.price,
                "discount": sp.discount,
                "currency": sp.currency,
                "images": [
                    request.build_absolute_uri(img.url)
                    for img in (sp.image1, sp.image2, sp.image3)
                    if img and getattr(img, "url", None)
                ],
            }
            for sp in product.similar_products.all()
        ],
    }

    return JsonResponse(data, safe=False)


def alternative_products(request):
    product_list = request.GET.get("product_list")
    option = request.GET.get("option", "low").lower()  # ensure lowercase input

    if not product_list:
        return JsonResponse({"error": "Product list required"}, status=400)

    product_ids = [pid.strip() for pid in product_list.split(",") if pid.strip().isdigit()]

    if not product_ids:
        return JsonResponse({"error": "Invalid product IDs"}, status=400)

    products = (
        Product.objects.filter(id__in=product_ids)
        .prefetch_related(Prefetch("productimage_set"), Prefetch("similar_products__productimage_set"))
    )

    alternatives = []
    for product in products:
        if option == "low":
            m = "This is Basic Product"
            alt = product.similar_products.filter(price__lt=product.price).order_by("price").first()
        elif option == "high":
            m= "This is Premium Product"
            alt = product.similar_products.filter(price__gt=product.price).order_by("-price").first()
        else:
            return JsonResponse({"error": "Invalid option parameter. Use 'high' or 'low'."}, status=400)
        logger.info(f"Found alternative for product {product.id}: {alt.id if alt else 'None'}")
        if alt:
            alternatives.append({
                "original": {
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "discount": product.discount,
                    "currency": product.currency,
                    "images": [
                        request.build_absolute_uri(img.url)
                        for img in (product.image1, product.image2, product.image3)
                        if img and getattr(img, "url", None)
                    ],
                },
                "alternative": {
                    "id": alt.id,
                    "name": alt.name,
                    "price": float(alt.price),
                    "discount": alt.discount,
                    "currency": alt.currency,
                    "images": [
                        request.build_absolute_uri(img.url)
                        for img in (alt.image1, alt.image2, alt.image3)
                        if img and getattr(img, "url", None)
                    ],
                },
            })
        else:
            
            alternatives.append({
                "original": {
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "discount": product.discount,
                    "currency": product.currency,
                    "images": [
                        request.build_absolute_uri(img.url)
                        for img in (product.image1, product.image2, product.image3)
                        if img and getattr(img, "url", None)
                    ],
                },
                "alternative": m,
            })

    return JsonResponse(alternatives, safe=False)

@csrf_exempt
def create_order(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Create the order
            order = Order.objects.create(
                customer_name=data.get("customer_name"),
                customer_phone=data.get("customer_phone"),
                customer_address=data.get("customer_address"),
                customer_email=data.get("customer_email"),
                pay_method=data.get("pay_method", "Cash on Delivery"),
                invoice_number=data.get("invoice_number"),
                total = data.get("total", 0.0),
            )

            # Loop through products
            for item in data.get("items", []):
                product = Product.objects.get(id=item["product_id"])
                quantity = int(item.get("quantity", 1))
                price = product.price

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    color=item.get("color"),
                    size=item.get("size"),
                    thickness=item.get("thickness"),
                    price=price,
                )
            send_appointment_email(name = order.customer_name, email=order.customer_email, invoice=order.invoice_number,phone=order.customer_phone).delay()


            return JsonResponse({
                "success": True,
                "order_id": order.invoice_number,
                "total_amount": order.total
            }, status=201)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"detail": "Only POST allowed"}, status=405)








#######################################
# Dashboard Start After this code 
############################################

@login_required
def dashboard(request):
    return TemplateResponse(request,'dashboard/dashboard.html')


# Category start here 
@login_required
def admin_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
        else:
            print (form.errors)

    data = Category.objects.all()

    context = {
        'form': form,
        'data': data,
    }
    return TemplateResponse(request, 'dashboard/category.html', context)


@login_required
def admin_edit_category(request, pk):
    cat_data = Category.objects.get(id=pk)
    
    form = CategoryForm(instance=cat_data)

    if request.method == 'POST':
        form = CategoryForm(request.POST or None, request.FILES or None, instance=cat_data)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
            
    data = Category.objects.all()
    context = {
        'form': form,
        'data': data,
    }
    return TemplateResponse(request, 'dashboard/category.html', context)


@login_required
def admin_delete_category(request, pk):
    cat = Category.objects.get(id=pk)
    cat.delete()
    return redirect('admin_category')

# Sub Category start Here 
@login_required
def admin_subcategory(request):
    
    form = SubCategoryForm()
    
    if request.method == 'POST':
        form = SubCategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('admin_sub_category')
            
    data = SubCategory.objects.all()
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subcategory.html', context)


@login_required
def admin_edit_subcategory(request, pk):
    sub_data = SubCategory.objects.get(id=pk)
    data = SubCategory.objects.all()
    form = SubCategoryForm(instance=sub_data)
    
    if request.method == 'POST':
        form = SubCategoryForm(request.POST or None, request.FILES or None, instance=sub_data)
        if form.is_valid():
            form.save()
            return redirect('admin_sub_category')
            
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subcategory.html', context)


@login_required
def admin_delete_subcategory(request, pk):
    data = SubCategory.objects.get(id=pk)
    data.delete()
    return redirect('admin_sub_category')

# Sub Sub Category start here 
@login_required
def admin_subsubcategory(request):
    data = SubSubCategory.objects.all()
    form = SubSubCategoryForm()
    
    if request.method == 'POST':
        form = SubSubCategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('admin_subsubcategory')
            
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subsubcategory.html', context)


@login_required
def admin_edit_subsubcategory(request, pk):
    sub_data = SubSubCategory.objects.get(id=pk)
    form = SubSubCategoryForm(instance=sub_data)
    
    if request.method == 'POST':
        form = SubSubCategoryForm(request.POST or None, request.FILES or None, instance=sub_data)
        if form.is_valid():
            form.save()
            return redirect('admin_subsubcategory')
    
    data = SubSubCategory.objects.all()
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subsubcategory.html', context)


@login_required
def admin_delete_subsubcategory(request, pk):
    data = SubSubCategory.objects.get(id=pk)
    data.delete()
    return redirect('admin_subsubcategory')

# Product start here 
@login_required
def admin_product(request):
    form = ProductForm()
    print (form)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('admin_product')

    # Pagination setup
    product_queryset = Product.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(product_queryset, 20)
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'data': page_obj,
    }
    return TemplateResponse(request, 'dashboard/product.html', context)


@login_required
def admin_edit_product(request, pk):
    p_data = Product.objects.get(id=pk)
    
    form = ProductForm(instance=p_data)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None, instance=p_data)
        if form.is_valid():
            form.save()
            return redirect('admin_product')
            
    # Pagination setup
    product_queryset = Product.objects.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(product_queryset, 10)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'data': page_obj,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/product.html', context)


@login_required
def admin_delete_product(request, pk):
    p_data = Product.objects.get(id=pk)
    p_data.delete()
    return redirect('admin_product')

# Product image start here 
@login_required
def admin_productimage(request, product):
    p_data = Product.objects.get(id=product)
    p_image = ProductImage.objects.filter(product=p_data)
    form = ProductImageForm()
    form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
    form.fields['product'].initial = p_data.id      
    
    if request.method == 'POST':
        form = ProductImageForm(request.POST or None, request.FILES or None)
        form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
        form.fields['product'].initial = p_data.id               # 👈 Set value
        if form.is_valid():
            form.save()
            return redirect('admin_productimage', product=product)
            
    context = {
        'data': p_image,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/productimage.html', context)


@login_required
def admin_edit_productimage(request):
    return TemplateResponse(request, 'dashboard/productimage.html')


@login_required
def admin_delete_productimage(request, pk, product):
    data = ProductImage.objects.get(id=pk)
    data.delete()
    return redirect('admin_productimage', product=product)

# Specification start here 
@login_required
def admin_specification(request, product):
    p_data = Product.objects.get(id=product)
    spec = Specification.objects.filter(product=p_data)

    if request.method == 'POST':
        form = SpecificationForm(request.POST, request.FILES)
        form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
        form.fields['product'].initial = p_data.id               # 👈 Set value
        if form.is_valid():
            specification = form.save(commit=False)
            specification.product = p_data                       # 👈 Ensure correct product
            specification.save()
            return redirect('admin_specification', product=product)
    else:
        form = SpecificationForm()
        form.fields['product'].widget = forms.HiddenInput()
        form.fields['product'].initial = p_data.id

    context = {
        'data': spec,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/specification.html', context)


@login_required
def admin_edit_specification(request, product, pk):
    p_data = Product.objects.get(id=product)
    spec = Specification.objects.filter(product=p_data)
    s = Specification.objects.get(id=pk)

    if request.method == 'POST':
        form = SpecificationForm(request.POST, request.FILES, instance=s)
        form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
        form.fields['product'].initial = p_data.id               # 👈 Set value
        if form.is_valid():
            specification = form.save(commit=False)
            specification.product = p_data                       # 👈 Ensure correct product
            specification.save()
            return redirect('admin_specification', product=product)
    else:
        form = SpecificationForm(instance=s)
        form.fields['product'].widget = forms.HiddenInput()
        form.fields['product'].initial = p_data.id

    context = {
        'data': spec,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/specification.html', context)


@login_required
def admin_delete_specification(request, product, pk):
    data = Specification.objects.get(id=pk)
    data.delete()
    return redirect('admin_specification', product=product)


@login_required
def productcolor(request, product):
    pro = get_object_or_404(Product, id=product)
    data = Product_Color.objects.filter(Product=pro)

    if request.method == 'POST':
        form = ProductColorForm(request.POST, request.FILES)
        if form.is_valid():
            color_instance = form.save(commit=False)
            color_instance.Product = pro
            color_instance.save()
            return redirect('admin_product_color', product=product)
    else:
        form = ProductColorForm()
        form.fields['Product'].widget = forms.HiddenInput()
        form.fields['Product'].initial = pro

    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/color.html', context)


@login_required
def productcolor_edit(request, product, pk):
    pro = get_object_or_404(Product, id=product)
    data = Product_Color.objects.filter(Product=pro)
    single_color = get_object_or_404(Product_Color, id=pk)

    if request.method == 'POST':
        form = ProductColorForm(request.POST, request.FILES, instance=single_color)
        if form.is_valid():
            color_instance = form.save(commit=False)
            color_instance.Product = pro
            color_instance.save()
            return redirect('admin_product_color', product=product)
    else:
        form = ProductColorForm(instance=single_color)
        form.fields['Product'].widget = forms.HiddenInput()
        form.fields['Product'].initial = pro

    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/color.html', context)


@login_required()
def productcolor_delete(request,product,pk):
    data = Product_Color.objects.get(id=pk)
    data.delete()
    return redirect('admin_product_color',product=product)

@login_required
def productsize(request, product):
    pro = get_object_or_404(Product, id=product)
    data = Product_Size.objects.filter(Product=pro)

    if request.method == 'POST':
        form = ProductSizeForm(request.POST, request.FILES)
        if form.is_valid():
            size_instance = form.save(commit=False)
            size_instance.Product = pro
            size_instance.save()
            return redirect('admin_product_size', product=product)
    else:
        form = ProductSizeForm()
        form.fields['Product'].widget = forms.HiddenInput()
        form.fields['Product'].initial = pro

    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/size.html', context)


@login_required
def productsize_edit(request, product, pk):
    pro = get_object_or_404(Product, id=product)
    data = Product_Size.objects.filter(Product=pro)
    single_size = get_object_or_404(Product_Size, id=pk)

    if request.method == 'POST':
        form = ProductSizeForm(request.POST, request.FILES, instance=single_size)
        if form.is_valid():
            size_instance = form.save(commit=False)
            size_instance.Product = pro
            size_instance.save()
            return redirect('admin_product_size', product=product)
    else:
        form = ProductSizeForm(instance=single_size)
        form.fields['Product'].widget = forms.HiddenInput()
        form.fields['Product'].initial = pro

    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/size.html', context)


@login_required()
def productsize_delete(request,product,pk):
    data = Product_Size.objects.get(id=pk)
    data.delete()
    return redirect('admin_product_size',product=product)


@login_required
def productthickness(request, product):
    pro = get_object_or_404(Product, id=product)
    data = Product_Thickness.objects.filter(Product=pro)

    if request.method == 'POST':
        form = ProductThicknessForm(request.POST, request.FILES)
        if form.is_valid():
            thickness_instance = form.save(commit=False)
            thickness_instance.Product = pro
            thickness_instance.save()
            return redirect('admin_product_thickness', product=product)
    else:
        form = ProductThicknessForm()
        form.fields['Product'].widget = forms.HiddenInput()
        form.fields['Product'].initial = pro

    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/thickness.html', context)


@login_required
def productthickness_edit(request, pk, product):
    pro = get_object_or_404(Product, id=product)
    data = Product_Thickness.objects.filter(Product=pro)
    single_thickness = get_object_or_404(Product_Thickness, id=pk)

    if request.method == 'POST':
        form = ProductThicknessForm(request.POST, request.FILES, instance=single_thickness)
        if form.is_valid():
            thickness_instance = form.save(commit=False)
            thickness_instance.Product = pro
            thickness_instance.save()
            return redirect('admin_product_thickness', product=product)
    else:
        form = ProductThicknessForm(instance=single_thickness)
        form.fields['Product'].widget = forms.HiddenInput()
        form.fields['Product'].initial = pro

    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/thickness.html', context)



@login_required()
def productthickness_delete(request,product,pk):
    data = Product_Thickness.objects.get(id=pk)
    data.delete()
    return redirect('admin_product_thickness',product=product)




# Order Management Start Here
def admin_order(request):
    """Return all orders with their items."""
    orders = Order.objects.all().order_by('-id')
    context = {
        "data": orders,
    }
    return TemplateResponse(request, "dashboard/order.html", context)


def admin_order_detail(request, order_id):
    """Display or update a single order."""
    order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id)
    
    # Handle status update
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order._meta.get_field('status').choices).keys():
            order.status = new_status
            order.save()
            return redirect('admin_order_details', order_id=order.id)
    
    # Add status_choices to context
    context = {
        "order": order,
        "status_choices": Order._meta.get_field('status').choices  # Add this line
    }
    return TemplateResponse(request, "dashboard/order_detail.html", context)