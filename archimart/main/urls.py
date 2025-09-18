from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('construction',views.construction,name="construction"),
    path('product.json',views.json_file,name="product_json"),

    # dashboard 
    path('dashboard',views.dashboard,name="dashboard"),
    path('admin_category',views.admin_category,name="admin_category"),
    path('admin_edit_category/<pk>',views.admin_edit_category,name="admin_edit_category"),
    path('admin_delete_category/<pk>',views.admin_delete_category,name="admin_delete_category"),
    path('admin_subcategory',views.admin_subcategory,name="admin_sub_category"),
    path('admin_edit_subcategory/<pk>',views.admin_edit_subcategory,name="admin_edit_subcategory"),
    path('admin_delete_subcategory/<pk>',views.admin_delete_subcategory,name="admin_delete_subcategory"),
    path('admin_subsubcategory',views.admin_subsubcategory,name="admin_subsubcategory"),
    path('admin_edit_subsubcategory/<pk>',views.admin_edit_subsubcategory,name="admin_edit_subsubcategory"),
    path('admin_delete_subsubcategory/<pk>',views.admin_delete_subsubcategory,name="admin_delete_subsubcategory"),
    path('admin_product',views.admin_product,name="admin_product"),
    path('admin_edit_product/<pk>',views.admin_edit_product,name="admin_edit_product"),
    path('admin_delete_product/<pk>',views.admin_delete_product,name="admin_delete_product"),
    path('admin_productimage/<product>',views.admin_productimage,name="admin_productimage"),
    path('admin_edit_productimage/<pk>',views.admin_edit_productimage,name="admin_edit_productimage"),
    path('admin_delete_productimage/<pk>/<product>',views.admin_delete_productimage,name="admin_delete_productimage"),
    path('admin_specification/<product>',views.admin_specification,name="admin_specification"),
    path('admin_edit_specification/<product>/<pk>',views.admin_edit_specification,name="admin_edit_specification"),
    path('admin_delete_specification/<product>/<pk>',views.admin_delete_specification,name="admin_delete_specification"),
    

    path('api/search.html',views.search_data,name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()

