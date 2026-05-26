from django.contrib.auth import login
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, CarForm,  CarSearchForm
from .models import Car, CarImage, Favorite
from django.utils import timezone
from django.views import generic,View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AdPlan, Payment
from .services.asaas_service import AsaasService
from .utils import delete_expired_unpaid_ads
from django.template.loader import render_to_string
from django.http import JsonResponse



class CarListView( generic.ListView):
    model = Car
    template_name = "platform/car_list.html"
    context_object_name = "car_list"
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = CarSearchForm(
            self.request.GET or None
        )
        context["show_filters"] = True

        # 🔥 favoritos do usuário
        if self.request.user.is_authenticated:

            favorites_ids = Favorite.objects.filter(
                user=self.request.user
            ).values_list("car_id", flat=True)

            context["favorite_ids"] = list(favorites_ids)

        else:

            context["favorite_ids"] = []

        context["is_favorite_page"] = False

        return context

    def render_to_response(self, context, **response_kwargs):

        # 🔥 AJAX
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "includes/car_cards.html",
                context,
                request=self.request
            )

            return JsonResponse({
                "html": html
            })

        return super().render_to_response(
            context,
            **response_kwargs
        )
    def get_queryset(self):
        delete_expired_unpaid_ads()
        Car.objects.filter(
            expires_at__lt=timezone.now(),
            is_active=True
        ).update(is_active=False)

        queryset = Car.objects.filter(
            is_active=True
        ).select_related(
            "plan",
            "manufacturer",
            "owner"
        ).order_by(
            "plan__priority",
            "-id"
        )

        form = CarSearchForm(self.request.GET)

        if form.is_valid():

            q = form.cleaned_data.get("q")
            model = form.cleaned_data.get("model")
            manufacturer = form.cleaned_data.get("manufacturer")
            year = form.cleaned_data.get("year")
            category = form.cleaned_data.get("category")

            if q:
                queryset = queryset.filter(
                    Q(model__icontains=q) |
                    Q(manufacturer__name__icontains=q)
                )

            if model:
                queryset = queryset.filter(model=model)

            if manufacturer:
                queryset = queryset.filter(
                    manufacturer__id=manufacturer
                )

            if year:
                queryset = queryset.filter(year=year)

            if category:
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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["plans"] = AdPlan.objects.all()

        return context

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        kwargs["request"] = self.request

        return kwargs

    def form_valid(self, form):

        response = super().form_valid(form)

        delete_ids = self.request.POST.getlist(
            "delete_images"
        )

        if delete_ids:
            CarImage.objects.filter(
                id__in=delete_ids
            ).delete()

        images = self.request.FILES.getlist("images")

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

        form = CarForm(request=request)

        plans = AdPlan.objects.all()

        return render(request, "platform/car_form.html", {
            "form": form,
            "plans": plans,
        })

    def post(self, request):

        form = CarForm(
            request.POST,
            request.FILES,
            request=request
        )

        if form.is_valid():

            car = form.save(commit=False)

            car.owner = request.user

            if car.plan.is_basico():

                car.is_active = True
                car.is_paid = True

            else:

                car.is_active = False
                car.is_paid = False

            car.set_expiration()

            car.save()

            images = request.FILES.getlist("images")

            for img in images:
                CarImage.objects.create(
                    car=car,
                    image=img
                )

            if not car.plan.is_basico():
                return redirect(
                    "platform:payment",
                    pk=car.id
                )

            return redirect("platform:car-list")

        return render(request, "platform/car_form.html", {
            "form": form,
            "plans": AdPlan.objects.all(),
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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        payment = Payment.objects.filter(
            car=self.object
        ).first()

        if payment:


            payment_data = AsaasService.get_payment(
                payment.payment_id
            )

            status_asaas = payment_data.get("status")


            # STATUSS ACEITOS
            payment_confirmed = status_asaas in [
                "RECEIVED",
                "RECEIVED_IN_CASH",
                "CONFIRMED"
            ]

            if payment_confirmed:

                if payment.status != "paid":


                    payment.status = "paid"

                    payment.paid_at = timezone.now()

                    payment.save()

                    car = payment.car

                    car.is_paid = True
                    car.is_active = True

                    car.set_expiration()

                    car.save()

                context["payment_confirmed"] = True

            pix_data = {
                "payload": payment.pix_code
            }

        else:

            payment_response = AsaasService.create_pix_payment(
                self.object
            )

            payment_data = payment_response["payment"]

            pix_data = payment_response["pix"]

            payment = Payment.objects.create(

                car=self.object,

                payment_id=payment_data["id"],

                invoice_url=payment_data["invoiceUrl"],

                pix_code=pix_data["payload"],

                status="pending"
            )


        context["payment"] = payment_data

        context["pix"] = pix_data

        return context
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

    paginate_by = 20

    def get_queryset(self):

        return Car.objects.filter(
            owner=self.request.user
        ).order_by("-id")


from django.http import JsonResponse


class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):

        car = get_object_or_404(Car, pk=pk)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            car=car
        )

        is_favorite = True

        # remove favorito
        if not created:

            favorite.delete()

            is_favorite = False

        return JsonResponse({
            "success": True,
            "is_favorite": is_favorite,
            "car_id": car.id
        })

class FavoriteListView(LoginRequiredMixin, generic.ListView):

    model = Car

    template_name = "platform/favorite_list.html"

    context_object_name = "car_list"

    paginate_by = 20

    def get_queryset(self):

        return Car.objects.filter(
            favorites__user=self.request.user
        ).select_related(
            "manufacturer",
            "plan",
            "owner"
        ).distinct().order_by("-favorites__created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        favorites_ids = Favorite.objects.filter(
            user=self.request.user
        ).values_list("car_id", flat=True)

        context["favorite_ids"] = list(favorites_ids)

        # 🔥 informa que é página favoritos
        context["is_favorite_page"] = True

        return context