from django import forms
from .models import Cargo, Departamento, TipoContrato, Empleado, Rol
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.forms import DateInput

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'


class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = '__all__'


class TipoContratoForm(forms.ModelForm):
    class Meta:
        model = TipoContrato
        fields = '__all__'


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['empleado', 'sueldo', 'horas_extra', 'bono']  # el resto se calcula automáticamente
        widgets = {
            'aniomes': DateInput(attrs={'type': 'date'}),
        }
def get_form_by_model_name(model_name):
    forms_dict = {
        'cargo': CargoForm,
        'departamento': DepartamentoForm,
        'tipocontrato': TipoContratoForm,
        'empleado': EmpleadoForm,
        'rol': RolForm,
    }
    return forms_dict.get(model_name)

class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(label='¿Es administrador?', required=False)
    admin_secret = forms.CharField(label='Clave de administrador', required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_staff', 'admin_secret']

    def clean(self):
        cleaned_data = super().clean()
        is_staff = cleaned_data.get('is_staff')
        admin_secret = cleaned_data.get('admin_secret')

        if is_staff:
            if admin_secret != settings.ADMIN_SECRET_KEY:
                raise forms.ValidationError("Clave de administrador incorrecta.")

        return cleaned_data