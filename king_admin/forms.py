from django.forms import forms,ModelForm
from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"

def create_model_form(request,admin_class):
    '''动态生成modelform'''
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
            # field_obj.widget.attrs['maxlength']=getattr(field_obj,'max_length')
        # print("base fields",cls.base_fields)
        return ModelForm.__new__(cls)




    class Meta:
        model = admin_class.model
        fields="__all__"

    attrs = {'Meta':Meta,}
    _model_form_class = type("DynamicModelForm",(ModelForm,),attrs)
    setattr(_model_form_class, '__new__', __new__)
    print("model form",_model_form_class.Meta.model)
    return _model_form_class