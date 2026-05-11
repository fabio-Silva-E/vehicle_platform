from django.contrib.auth import login
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, CarForm,  CarSearchForm
from .models import Car, CarImage
from django.utils import timezone
from django.views import generic,View
from django.contrib.auth.mixins import LoginRequiredMixin




class CarListView( generic.ListView):
    model = Car
    template_name = "platform/car_list.html"
    context_object_name = "car_list"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = CarSearchForm(
            self.request.GET or None
        )
        context["show_filters"] = True
        return context

    def get_queryset(self):
        Car.objects.filter(
            expires_at__lt=timezone.now()
        ).update(is_active=False)
        queryset = Car.objects.filter(
            is_active=True
        ).select_related("manufacturer")

        form = CarSearchForm(self.request.GET)

        if form.is_valid():

            q = form.cleaned_data.get("q")
            model = form.cleaned_data.get("model")
            manufacturer = form.cleaned_data.get("manufacturer")
            year = form.cleaned_data.get("year")
            category = form.cleaned_data.get("category")

            # 🔎 Busca geral
            if q:
                queryset = queryset.filter(
                    Q(model__icontains=q) |
                    Q(manufacturer__name__icontains=q)
                )

            # 🚗 Modelo
            if model:
                queryset = queryset.filter(model=model)

            # 🏭 Fabricante
            if manufacturer:
                queryset = queryset.filter(manufacturer__id=manufacturer)

            # 📅 Ano
            if year:
                queryset = queryset.filter(year=year)

            # 🏷️ Categoria
            if category not in [None, ""]:
                queryset = queryset.filter(category=category)

        return queryset



class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("platform:car-list")

    def form_valid(self, form):
        response = super().form_valid(form)

        # login automático após cadastro
        login(self.request, self.object)

        return response


class CarDetailView( generic.DetailView):
    model = Car
    template_name = "platform/car_detail.html"


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    template_name = "platform/car_form.html"
    success_url = reverse_lazy("platform:car-list")

    def form_valid(self, form):

        # 👇 novas imagens
        images = self.request.FILES.getlist("images")

        # 👇 imagens atuais + novas
        total_images = self.object.images.count() + len(images)

        # 🔥 valida limite
        if total_images > self.object.max_images():
            form.add_error(
                None,
                f"O plano {self.object.get_plan_display()} permite apenas {self.object.max_images()} imagens."
            )

            return self.form_invalid(form)

        # 🔥 salva formulário
        response = super().form_valid(form)

        # 👇 remover imagens
        delete_ids = self.request.POST.getlist("delete_images")

        if delete_ids:
            CarImage.objects.filter(id__in=delete_ids).delete()

        # 👇 adicionar imagens
        for img in images:
            CarImage.objects.create(
                car=self.object,
                image=img
            )

        return response
class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    template_name = "platform/car_confirm_delete.html"
    success_url = reverse_lazy("platform:my-cars")
    
class CarCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = CarForm()

        return render(request, "platform/car_form.html", {
            "form": form,
        })

    def post(self, request):
        form = CarForm(request.POST, request.FILES)

        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            print(car.plan)
            print("FORM OK")
            # 🔥 PLANO BÁSICO PUBLICA DIRETO
            if car.plan == "basico":

                car.is_active = True
                car.is_paid = True

            # 🔥 PLANOS PAGOS AGUARDAM PAGAMENTO
            else:
                print(form.errors)
                car.is_active = False
                car.is_paid = False

            # 👇 MULTI IMAGENS
            images = request.FILES.getlist("images")

            # 🔥 valida limite ANTES de salvar
            if len(images) > car.max_images():
                form.add_error(
                    None,
                    f"O plano {car.get_plan_display()} permite apenas {car.max_images()} imagens."
                )

                return render(request, "platform/car_form.html", {
                    "form": form,
                })

            # 🔥 define expiração
            car.set_expiration()

            # 🔥 salva após validar
            car.save()

            for img in images:
                CarImage.objects.create(
                    car=car,
                    image=img
                )

            # 🔥 planos pagos vão para pagamento
            if car.plan != "basico":
                return redirect(
                    "platform:payment",
                    pk=car.id
                )

            # 🔥 básico publica direto
            return redirect("platform:car-list")

        return render(request, "platform/car_form.html", {
            "form": form,
        })



class DeleteCarImageView(LoginRequiredMixin, View):
    def post(self, request, pk):
        image = get_object_or_404(CarImage, pk=pk)

        if image.car.owner != request.user:
            return redirect("platform:car-list")

        car_id = image.car.id

        # remove arquivo físico + banco
        image.image.delete(save=False)
        image.delete()

        return redirect("platform:car-update", pk=car_id)

class PaymentView(LoginRequiredMixin, generic.DetailView):

    model = Car

    template_name = "platform/payment.html"


class ApprovePaymentView(LoginRequiredMixin, View):

    def get(self, request, pk):

        car = get_object_or_404(Car, pk=pk)

        # 🔥 libera anúncio
        car.is_active = True
        car.is_paid = True
        car.set_expiration()
        car.save()

        return redirect("platform:car-list")

class MyCarsView(LoginRequiredMixin, generic.ListView):

    model = Car

    template_name = "platform/my_cars.html"

    context_object_name = "car_list"

    paginate_by = 10

    def get_queryset(self):

        return Car.objects.filter(
            owner=self.request.user
        ).order_by("-id")