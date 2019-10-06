from crm import models

enabled_admins={}
class BaseAdmin(object):
    list_display=[]
    list_filter = []
    list_per_page = 20
    search_fields=[]
    ordering = None
    filter_horizontal = []
    actions = ['delete_selected_objs',]
    def delete_selected_objs (self,request,querysets):
        print("delete_selected_objs:",self,request,querysets)


class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','source','consultant','date','status','consult_course']
    list_filters = ['source','consultant','consult_course','status','date']
    search_fields = ['qq', 'name','consultant__name']
    list_per_page = 5
    ordering = 'qq'
    filter_horizontal = ('tags',)
    class Meta:
        verbose_name_plural = "客户表"


class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer','consultant','date')


def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label]={} # enabled_admins['crm']={}

    # admin_obj = admin_class()
    admin_class.model=model_class  # 绑定model对象和admin类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name]=admin_class
    #enabled_admins['crm']['customerfollowup']=CustomerFollowUpAdmin


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowup,CustomerFollowUpAdmin)

