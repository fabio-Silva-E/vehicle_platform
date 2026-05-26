from .models import Car, CarImage, Manufacturer, AdPlan
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

User = get_user_model()
widget=forms.Select(attrs={
    "class": "form-select form-select-sm"
})

widget=forms.TextInput(attrs={
    "class": "form-control form-control-sm"
})

class UserRegisterForm(UserCreationForm):

    def clean_cpf_cnpj(self):

        cpf_cnpj = self.cleaned_data.get(
            "cpf_cnpj"
        )

        if not cpf_cnpj:
            return cpf_cnpj

        # remove máscara
        cpf_cnpj = re.sub(r"\D", "", cpf_cnpj)

        # CPF
        if len(cpf_cnpj) == 11:

            # bloqueia sequências iguais
            if cpf_cnpj == cpf_cnpj[0] * 11:
                raise ValidationError(
                    "CPF inválido."
                )

            # primeiro dígito
            soma = sum(
                int(cpf_cnpj[i]) * (10 - i)
                for i in range(9)
            )

            digito1 = (
                              (soma * 10) % 11
                      ) % 10

            # segundo dígito
            soma = sum(
                int(cpf_cnpj[i]) * (11 - i)
                for i in range(10)
            )

            digito2 = (
                              (soma * 10) % 11
                      ) % 10

            if (
                    int(cpf_cnpj[9]) != digito1 or
                    int(cpf_cnpj[10]) != digito2
            ):
                raise ValidationError(
                    "CPF inválido."
                )

        # CNPJ
        elif len(cpf_cnpj) == 14:

            def calcular_digito(cnpj, pesos):

                soma = sum(
                    int(num) * peso
                    for num, peso in zip(cnpj, pesos)
                )

                resto = soma % 11

                return "0" if resto < 2 else str(11 - resto)

            if cpf_cnpj == cpf_cnpj[0] * 14:
                raise ValidationError(
                    "CNPJ inválido."
                )

            pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

            digito1 = calcular_digito(
                cpf_cnpj[:12],
                pesos1
            )

            digito2 = calcular_digito(
                cpf_cnpj[:12] + digito1,
                pesos2
            )

            if cpf_cnpj[-2:] != digito1 + digito2:
                raise ValidationError(
                    "CNPJ inválido."
                )

        else:

            raise ValidationError(
                "Informe um CPF ou CNPJ válido."
            )

        return cpf_cnpj

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "phone",
            "city",
            "cpf_cnpj",
            "password1",
            "password2"
        )

        labels = {
            "username": "Usuário",
            "email": "Email",
            "phone": "Telefone",
            "city": "Cidade",
            "cpf_cnpj": "CPF ou CNPJ",
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

            "placeholder": "Buscar por modelo, fabricante ou palavra-chave...",

            "class": "search-input",

            "autocomplete": "off",
        })
    )

    category = forms.ChoiceField(

        required=False,

        label="Categoria",

        choices=[("", "Todos")] + Car.CATEGORY_CHOICES,

        widget=forms.Select(attrs={

            "class": "sidebar-select",

          #  "onchange": "this.form.submit()"
        })
    )

    model = forms.ChoiceField(

        required=False,

        label="Modelo",

        choices=[],

        widget=forms.Select(attrs={

            "class": "sidebar-select",

          #  "onchange": "this.form.submit()"
        })
    )

    manufacturer = forms.ChoiceField(

        required=False,

        label="Fabricante",

        choices=[],

        widget=forms.Select(attrs={

            "class": "sidebar-select",

           # "onchange": "this.form.submit()"
        })
    )

    year = forms.ChoiceField(

        required=False,

        label="Ano",

        choices=[],

        widget=forms.Select(attrs={

            "class": "sidebar-select",

           # "onchange": "this.form.submit()"
        })
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # MODELOS
        models = Car.objects.values_list(
            "model",
            flat=True
        ).distinct()

        self.fields["model"].choices = [
            ("", "Todos")
        ] + [(m, m) for m in models if m]

        # FABRICANTES
        manufacturers = Manufacturer.objects.all()

        self.fields["manufacturer"].choices = [
            ("", "Todos")
        ] + [
            (m.id, m.name)
            for m in manufacturers
        ]

        # ANOS
        years = Car.objects.values_list(
            "year",
            flat=True
        ).distinct().order_by("-year")

        self.fields["year"].choices = [
            ("", "Todos")
        ] + [
            (y, y)
            for y in years if y
        ]
class CarForm(forms.ModelForm):

    manufacturer_name = forms.CharField(
        required=False,
        label="Novo fabricante"
    )

    plan = forms.ModelChoiceField(

        queryset=AdPlan.objects.all().order_by("priority"),

        label="Plano",

        empty_label=None,

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

    class Meta:
        model = Car

        fields = [
            "category",
            "plan",
            "model",
            "manufacturer",
            "year",
            "value",
            "description",
            "whatsapp"
        ]

        labels = {
            "model": "Modelo",
            "manufacturer": "Fabricante",
            "year": "Ano",
            "description": "Descrição",
            "whatsapp": "WhatsApp",
            "value": "Valor",
        }

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop("request", None)

        super().__init__(*args, **kwargs)

        self.fields["manufacturer"].required = False

    def clean_whatsapp(self):

        whatsapp = self.cleaned_data.get("whatsapp")

        if whatsapp:

            whatsapp = re.sub(r"\D", "", whatsapp)

            if not whatsapp.startswith("55"):
                whatsapp = "55" + whatsapp

        return whatsapp

    def clean(self):

        cleaned_data = super().clean()

        category = cleaned_data.get("category")

        manufacturer = cleaned_data.get("manufacturer")

        manufacturer_name = cleaned_data.get("manufacturer_name")

        plan = cleaned_data.get("plan")

        # 🔥 validações por categoria
        if category in ["carro", "equipamento", "caminhao"]:

            if not cleaned_data.get("model"):
                raise forms.ValidationError(
                    "Informe o modelo."
                )

            if not cleaned_data.get("year"):
                raise forms.ValidationError(
                    "Informe o ano."
                )

            if not manufacturer and not manufacturer_name:
                raise forms.ValidationError(
                    "Selecione um fabricante ou informe um novo."
                )

        # 🔥 validação de imagens
        if self.request and plan:

            images = self.request.FILES.getlist("images")

            total_images = len(images)

            # update
            if self.instance.pk:
                total_images += self.instance.images.count()

            if total_images > plan.max_images:

                raise forms.ValidationError(
                    f"O plano {plan.get_name_display()} "
                    f"permite apenas {plan.max_images} imagens."
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