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
    

    # dashboard 
    path('dash/dashboard',views.dashboard,name="dashboard"),
    path('dash/admin_category',views.admin_category,name="admin_category"),
    path('dash/admin_edit_category/<pk>',views.admin_edit_category,name="admin_edit_category"),
    path('dash/admin_delete_category/<pk>',views.admin_delete_category,name="admin_delete_category"),
    path('dash/admin_subcategory',views.admin_subcategory,name="admin_sub_category"),
    path('dash/admin_edit_subcategory/<pk>',views.admin_edit_subcategory,name="admin_edit_subcategory"),
    path('dash/admin_delete_subcategory/<pk>',views.admin_delete_subcategory,name="admin_delete_subcategory"),
    path('dash/admin_subsubcategory',views.admin_subsubcategory,name="admin_subsubcategory"),
    path('dash/admin_edit_subsubcategory/<pk>',views.admin_edit_subsubcategory,name="admin_edit_subsubcategory"),
    path('dash/admin_delete_subsubcategory/<pk>',views.admin_delete_subsubcategory,name="admin_delete_subsubcategory"),
    path('dash/admin_product',views.admin_product,name="admin_product"),
    path('dash/admin_edit_product/<pk>',views.admin_edit_product,name="admin_edit_product"),
    path('dash/admin_delete_product/<pk>',views.admin_delete_product,name="admin_delete_product"),
    path('dash/admin_productimage/<product>',views.admin_productimage,name="admin_productimage"),
    path('dash/admin_edit_productimage/<pk>',views.admin_edit_productimage,name="admin_edit_productimage"),
    path('dash/admin_delete_productimage/<pk>/<product>',views.admin_delete_productimage,name="admin_delete_productimage"),
    path('dash/admin_specification/<product>',views.admin_specification,name="admin_specification"),
    path('dash/admin_edit_specification/<product>/<pk>',views.admin_edit_specification,name="admin_edit_specification"),
    path('dash/admin_delete_specification/<product>/<pk>',views.admin_delete_specification,name="admin_delete_specification"),
    path('dash/admin_product_color/<product>',views.productcolor,name="admin_product_color"),
    path('dash/admin_product_color_edit/<product>/<pk>',views.productcolor_edit,name="product_color_edit"),
    path('dash/admin_product_color_delete/<product>/<pk>',views.productcolor_delete,name="product_color_delete"),

    path('api/product.json',views.json_file,name="product_json"),
    path('api/properties',views.search_data,name="search"),
    path('api/single_product/<pk>',views.single_product,name="single_product"),
    path("api/similar-products/", views.get_similar_products, name="ajax_similar_products"),
    path('api/alternative', views.alternative_products, name='alternative_products'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

