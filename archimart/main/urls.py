from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('construction',views.construction,name="construction"),
    path('cart',views.cart,name="cart"),
    path('compare',views.compare,name="compare"),
    path('detail',views.detail,name="detail"),

    path('bkash-payment/',views.bkash_payment, name='bkash_payment'),
    

    # dashboard 
    path('api/dashboard',views.dashboard,name="dashboard"),
    path('api/admin_category',views.admin_category,name="admin_category"),
    path('api/admin_edit_category/<pk>',views.admin_edit_category,name="admin_edit_category"),
    path('api/admin_delete_category/<pk>',views.admin_delete_category,name="admin_delete_category"),
    path('api/admin_subcategory',views.admin_subcategory,name="admin_sub_category"),
    path('api/admin_edit_subcategory/<pk>',views.admin_edit_subcategory,name="admin_edit_subcategory"),
    path('api/admin_delete_subcategory/<pk>',views.admin_delete_subcategory,name="admin_delete_subcategory"),
    path('api/admin_subsubcategory',views.admin_subsubcategory,name="admin_subsubcategory"),
    path('api/admin_edit_subsubcategory/<pk>',views.admin_edit_subsubcategory,name="admin_edit_subsubcategory"),
    path('api/admin_delete_subsubcategory/<pk>',views.admin_delete_subsubcategory,name="admin_delete_subsubcategory"),
    path('api/admin_product',views.admin_product,name="admin_product"),
    path('api/admin_edit_product/<pk>',views.admin_edit_product,name="admin_edit_product"),
    path('api/admin_delete_product/<pk>',views.admin_delete_product,name="admin_delete_product"),
    path('api/admin_productimage/<product>',views.admin_productimage,name="admin_productimage"),
    path('api/admin_edit_productimage/<pk>',views.admin_edit_productimage,name="admin_edit_productimage"),
    path('api/admin_delete_productimage/<pk>/<product>',views.admin_delete_productimage,name="admin_delete_productimage"),
    path('api/admin_specification/<product>',views.admin_specification,name="admin_specification"),
    path('api/admin_edit_specification/<product>/<pk>',views.admin_edit_specification,name="admin_edit_specification"),
    path('api/admin_delete_specification/<product>/<pk>',views.admin_delete_specification,name="admin_delete_specification"),
    
    path('api/admin_product_color/<product>',views.productcolor,name="admin_product_color"),
    path('api/admin_product_color_edit/<product>/<pk>',views.productcolor_edit,name="product_color_edit"),
    path('api/admin_product_color_delete/<product>/<pk>',views.productcolor_delete,name="product_color_delete"),

    path('api/admin_product_size/<product>',views.productsize,name="admin_product_size"),
    path('api/admin_product_size_edit/<product>/<pk>',views.productsize_edit,name="product_size_edit"),
    path('api/admin_product_size_delete/<product>/<pk>',views.productsize_delete,name="product_size_delete"),

    path('api/admin_product_thickness/<product>',views.productthickness,name="admin_product_thickness"),
    path('api/admin_product_thickness_edit/<product>/<pk>',views.productthickness_edit,name="product_thickness_edit"),
    path('api/admin_product_thickness_delete/<product>/<pk>',views.productthickness_delete,name="product_thickness_delete"),

    path('api/create_order',views.create_order,name="create_order"),
    path('api/admin_orders',views.admin_order,name="admin_orders"),
    path('api/admin_order_details/<order_id>',views.admin_order_detail,name="admin_order_details"),

    path('api/product.json',views.json_file,name="product_json"),
    path('api/properties',views.search_data,name="search"),
    path('api/single_product/<pk>',views.single_product,name="single_product"),
    path("api/similar-products/", views.get_similar_products, name="ajax_similar_products"),
    path('api/alternative', views.alternative_products, name='alternative_products'),
    path('api/search',views.search_products,name="search_products"),
    path('api/invoice/<path:order_id>',views.invoice,name="invoice"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

