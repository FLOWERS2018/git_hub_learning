from django.shortcuts import render,redirect
from king_admin import king_admin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import importlib
from king_admin.utils import table_filter,table_sort,table_search
from king_admin.forms import create_model_form


# Create your views here.
def index(request):

    return render(request, "king_admin/table_index.html",{'table_list':king_admin.enabled_admins})


def display_table_objs(request,app_name,table_name):
    print("---->",app_name,table_name)
    # models_module = importlib.import_module('%s.models'%(app_name))
    # model_obj = getattr(models_module,table_name)
    admin_class = king_admin.enabled_admins[app_name][table_name]
    # object_list = admin_class.model.objects.all()
    object_list,filter_conditions= table_filter(request,admin_class)

    object_list=table_search(request,admin_class,object_list)

    object_list,orderby_key = table_sort(request,admin_class,object_list)
    # print("orderby key",orderby_key)

    paginator = Paginator(object_list, admin_class.list_per_page)  # Show 25 contacts per page

    page = request.GET.get('page')
    query_sets = paginator.get_page(page)

    return render(request,"king_admin/table_objs.html",{"admin_class":admin_class,"query_sets":query_sets,
                                                        "filter_conditions":filter_conditions,
                                                        "orderby_key":orderby_key,
                                                        "previous_orderby":request.GET.get("o",''),
                                                        "search_text":request.GET.get('_q','')})




def table_obj_change(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method=="POST":
        form_obj=model_form_class(request.POST,instance=obj)
        if form_obj.is_valid():
            form_obj.save()
    else:

        form_obj = model_form_class(instance=obj)

    return render(request,'king_admin/table_obj_change.html',{'form_obj':form_obj,
                                                                    "admin_class":admin_class,
                                                                    "app_name":app_name,
                                                                    "table_name":table_name})


def table_obj_add(request,app_name,table_name):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request, admin_class)
    if request.method=="POST":
        form_obj=model_form_class(request.POST,)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace('/add/','/'))
    else:

        form_obj = model_form_class()
    return render(request,'king_admin/table_obj_add.html',{'form_obj':form_obj,
                                                                'admin_class':admin_class})


def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)

    return render(request,'king_admin/table_obj_delete.html',{"obj":obj,
                                                                    "admin_class":admin_class})