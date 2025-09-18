from django.template.response import TemplateResponse
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from django.http import JsonResponse
# Create your views here.

async def home(request):
    return TemplateResponse(request, 'archimart/index.html')

async def construction(request):
    return TemplateResponse(request, 'archimart/construction.html')



@sync_to_async
def get_paginated_products(page_number, per_page, category=None, sub_category=None, sub_sub_category=None):
    products_qs = Product.objects.prefetch_related(
        "productimage_set", "specification_set"
    ).order_by("id")

    # Apply filters if provided
    if category:
        products_qs = products_qs.filter(category=category)
    if sub_category:
        products_qs = products_qs.filter(sub_category=sub_category)
    if sub_sub_category:
        products_qs = products_qs.filter(sub_sub_category=sub_sub_category)

    paginator = Paginator(products_qs, per_page)
    page_obj = paginator.get_page(page_number)

    results = []
    for product in page_obj.object_list:
        results.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "currency": product.currency,
            "description": product.description,
            "images": [img.image.url for img in product.productimage_set.all()],
            "specifications": [
                {"key": spec.key, "value": spec.value, "price": spec.price}
                for spec in product.specification_set.all()
            ]
        })

    return {
        "count": paginator.count,
        "num_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "results": results,
    }
dfddd

async def json_file(request):
    category = request.GET.get("category")
    sub_category = request.GET.get("subcategory")
    sub_sub_category = request.GET.get("subsubcategory")
    page_number = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 10))
    
    data = await get_paginated_products(
        page_number, per_page, category, sub_category, sub_sub_category
    )
    return JsonResponse(data, safe=False)

#######################################
# Dashboard Start After this code 
############################################

@login_required
async def dashboard(request):
    return TemplateResponse(request,'dashboard/dashboard.html')

# Category start here 
@login_required
async def admin_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            category = form.save(commit=False)
            await category.asave()
            return redirect('admin_category')
        else:
            print (form.errors)

    data = [category async for category in Category.objects.all()]  # ✅ Async iteration

    context = {
        'form': form,
        'data': data,
    }
    return TemplateResponse(request, 'dashboard/category.html', context)

@login_required
async def admin_edit_category(request, pk):
    cat_data = await Category.objects.aget(id = pk)
    

    form = CategoryForm(instance=cat_data)

    if request.method == 'POST':
        form = CategoryForm(request.POST or None, request.FILES or None, instance=cat_data)
        if form.is_valid():
            data = form.save(commit=False)
            await data.asave() 
            return redirect('admin_category')
    data = [category async for category in Category.objects.all()]
    context = {
        'form': form,
        'data': data,
    }
    return TemplateResponse(request, 'dashboard/category.html', context)

@login_required
async def admin_delete_category(request, pk):
    cat = await Category.objects.aget(id=pk)
    await cat.adelete()  # ✅ Added await and use adelete()
    return redirect('admin_category')

# Sub Category start Here 
@login_required
async def admin_subcategory(request):
    
    form = SubCategoryForm()
    
    if request.method == 'POST':
        form = SubCategoryForm(request.POST or None, request.FILES or None)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            subcategory = form.save(commit=False)
            await subcategory.asave()  
            return redirect('admin_sub_category')
    data = [sub async for sub in SubCategory.objects.all()]    
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subcategory.html', context)

@login_required
async def admin_edit_subcategory(request, pk):
    sub_data = await SubCategory.objects.aget(id=pk)
    data = [sub async for sub in SubCategory.objects.all()]  # ✅ Async iteration
    form = SubCategoryForm(instance=sub_data)
    
    if request.method == 'POST':
        form = SubCategoryForm(request.POST or None, request.FILES or None, instance=sub_data)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            subcategory = form.save(commit=False)
            await subcategory.asave()  # ✅ Added await
            return redirect('admin_sub_category')
            
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subcategory.html', context)

@login_required
async def admin_delete_subcategory(request, pk):
    data = await SubCategory.objects.aget(id=pk)
    await data.adelete()  # ✅ Added await and use adelete()
    return redirect('admin_sub_category')

# Sub Sub Category start here 
@login_required
async def admin_subsubcategory(request):
    data = [sub async for sub in SubSubCategory.objects.all()]  # ✅ Async iteration
    form = SubSubCategoryForm()
    
    if request.method == 'POST':
        form = SubSubCategoryForm(request.POST or None, request.FILES or None)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            subsubcategory = form.save(commit=False)
            await subsubcategory.asave()  # ✅ Added await
            return redirect('admin_subsubcategory')
            
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subsubcategory.html', context)

@login_required
async def admin_edit_subsubcategory(request, pk):
    sub_data = await SubSubCategory.objects.aget(id=pk)
    form = SubSubCategoryForm(instance=sub_data)
    
    if request.method == 'POST':
        form = SubSubCategoryForm(request.POST or None, request.FILES or None, instance=sub_data)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            subsubcategory = form.save(commit=False)
            await subsubcategory.asave()  # ✅ Added await
            return redirect('admin_subsubcategory')
    
    data = [sub async for sub in SubSubCategory.objects.all()]  # ✅ Async iteration
    context = {
        'data': data,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/subsubcategory.html', context)

@login_required
async def admin_delete_subsubcategory(request, pk):
    data = await SubSubCategory.objects.aget(id=pk)
    await data.adelete()  # ✅ Added await and use adelete()
    return redirect('admin_subsubcategory')

# Product start here 
@login_required
async def admin_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            product = form.save(commit=False)
            await product.asave()  # ✅ Added await
            return redirect('admin_product')

    # ✅ Proper async queryset handling for pagination
    product_queryset = Product.objects.all()
    product_list = await sync_to_async(list)(product_queryset)

    # Pagination setup
    page_number = request.GET.get('page', 1)
    paginator = Paginator(product_list, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'data': page_obj,
    }
    return TemplateResponse(request, 'dashboard/product.html', context)

@login_required
async def admin_edit_product(request, pk):
    p_data = await Product.objects.aget(id=pk)
    
    form = ProductForm(instance=p_data)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None, instance=p_data)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            product = form.save(commit=False)
            await product.asave()  # ✅ Added await
            return redirect('admin_product')
            
    # ✅ Proper async handling
    product_queryset = Product.objects.all()
    data = await sync_to_async(list)(product_queryset)
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'data': page_obj,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/product.html', context)

@login_required
async def admin_delete_product(request, pk):
    p_data = await Product.objects.aget(id=pk)
    await p_data.adelete()  # ✅ Added await and use adelete()
    return redirect('admin_product')

# Product image start here 
@login_required
async def admin_productimage(request, product):
    p_data = await Product.objects.aget(id=product)
    p_image = [img async for img in ProductImage.objects.filter(product=p_data)]  # ✅ Async iteration
    form = ProductImageForm()
    form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
    form.fields['product'].initial = p_data.id      
    if request.method == 'POST':
        form = ProductImageForm(request.POST or None, request.FILES or None)
        form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
        form.fields['product'].initial = p_data.id               # 👈 Set value
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            pro = form.save(commit=False)
            await pro.asave()  
            return redirect('admin_productimage', product=product)
            
    context = {
        'data': p_image,
        'form': form,
    }
    return TemplateResponse(request, 'dashboard/productimage.html', context)

@login_required
async def admin_edit_productimage(request):
    return TemplateResponse(request, 'dashboard/productimage.html')

@login_required
async def admin_delete_productimage(request, pk, product):
    data = await ProductImage.objects.aget(id=pk)
    await data.adelete()  
    return redirect('admin_productimage', product=product)  # ✅ Fixed redirect params

# Specification start here 
@login_required
async def admin_specification(request, product):
    p_data = await Product.objects.aget(id=product)
    spec = [s async for s in Specification.objects.filter(product=p_data)]

    if request.method == 'POST':
        form = SpecificationForm(request.POST, request.FILES)
        form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
        form.fields['product'].initial = p_data.id               # 👈 Set value
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            specification = form.save(commit=False)
            specification.product = p_data                       # 👈 Ensure correct product
            await specification.asave()
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
async def admin_edit_specification(request, product, pk):
    p_data = await Product.objects.aget(id=product)
    spec = [s async for s in Specification.objects.filter(product=p_data)]
    s = await Specification.objects.aget(id=pk)

    if request.method == 'POST':
        form = SpecificationForm(request.POST, request.FILES, instance=s)
        form.fields['product'].widget = forms.HiddenInput()      # 👈 Hide field
        form.fields['product'].initial = p_data.id               # 👈 Set value
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            specification = form.save(commit=False)
            specification.product = p_data                       # 👈 Ensure correct product
            await specification.asave()
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
async def admin_delete_specification(request, product, pk):
    data = await Specification.objects.aget(id=pk)
    await data.adelete()  # ✅ Added await and use adelete()
    return redirect('admin_specification', product=product)