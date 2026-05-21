from .models import Car, CarImage, Manufacturer
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re

User = get_user_model()
widget=forms.Select(attrs={
    "class": "form-select form-select-sm"
})

widget=forms.TextInput(attrs={
    "class": "form-control form-control-sm"
})

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone", "city", "password1", "password2")

        labels = {
            "username": "Usuário",
            "email": "Email",
            "phone": "Telefone",
            "city": "Cidade",
            "password1": "Senha",
            "password2": "Confirme a senha",
        }


class CarSearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ("", "Todas"),
        ("carro", "Carros"),
        ("equipamento", "Equipamentos Pesados"),
        ("animal", "Animais"),
        ("fazenda", "Fazenda"),
    ]
    q = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Buscar por modelo ou fabricante",
            "class": "form-control",
            "style": "width: 400px;"
        })
    )
    category = forms.ChoiceField(
        required=False,
        label="Categoria",
        choices=[("", "Todos")] + Car.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-select",
            "onchange": "this.form.submit()"
        })
    )
    model = forms.ChoiceField(
        required=False,
        label="Modelo",
        choices=[]
    )

    manufacturer = forms.ChoiceField(
        required=False,
        label="Fabricante",
        choices=[]
    )

    year = forms.ChoiceField(
        required=False,
        label="Ano",
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # MODELOS únicos
        models = Car.objects.values_list("model", flat=True).distinct()
        self.fields["model"].choices = [("", "Todos")] + [(m, m) for m in models if m]

        # FABRICANTES
        manufacturers = Manufacturer.objects.all()
        self.fields["manufacturer"].choices = [("", "Todos")] + [
            (m.id, m.name) for m in manufacturers
        ]

        # ANOS únicos
        years = Car.objects.values_list("year", flat=True).distinct().order_by("-year")
        self.fields["year"].choices = [("", "Todos")] + [(y, y) for y in years if y]


class CarForm(forms.ModelForm):

    manufacturer_name = forms.CharField(required=False, label="Novo fabricante")

    plan = forms.ChoiceField(

        choices=Car.PLAN_CHOICES,

        label="Plano",

        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )

    whatsapp = forms.CharField(

        label="WhatsApp",
        widget=forms.TextInput(attrs={
            "placeholder": "(99) 99999-9999"
        })
    )


    # 👇 AQUI ESTÁ A MÁGICA
    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get("whatsapp")

        if whatsapp:
            # remove tudo que não for número
            whatsapp = re.sub(r"\D", "", whatsapp)

            # 👇 opcional: garantir que tenha DDI (55)
            if not whatsapp.startswith("55"):
                whatsapp = "55" + whatsapp

        return whatsapp



    class Meta:
        model = Car
        fields = ["category", "plan", "model", "manufacturer", "year", "value","description", "whatsapp"]
        labels = {
            "model": "Modelo",
            "manufacturer": "Fabricante",
            "year": "Ano",
            "description": "Descrição",
            "whatsapp": "WhatsApp",
            "value": "Valor",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 TORNA OPCIONAL
        self.fields["manufacturer"].required = False

    def clean(self):
        cleaned_data = super().clean()

        category = cleaned_data.get("category")

        manufacturer = cleaned_data.get("manufacturer")
        manufacturer_name = cleaned_data.get("manufacturer_name")

        # 🔥 Só exige campos de veículo
        if category in ["carro", "equipamento", "caminhao"]:

            if not cleaned_data.get("model"):
                raise forms.ValidationError("Informe o modelo.")

            if not cleaned_data.get("year"):
                raise forms.ValidationError("Informe o ano.")

            if not manufacturer and not manufacturer_name:
                raise forms.ValidationError(
                    "Selecione um fabricante ou informe um novo."
                )

        return cleaned_data

    def save(self, commit=True):

        manufacturer = self.cleaned_data.get("manufacturer")
        manufacturer_name = self.cleaned_data.get("manufacturer_name")

        if manufacturer_name:
            manufacturer, _ = Manufacturer.objects.get_or_create(
                name=manufacturer_name
            )

        self.instance.manufacturer = manufacturer

        return super().save(commit)
