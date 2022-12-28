from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Product, Category, Appointment
from datetime import datetime
from django.core.paginator import Paginator
from django.views import View
from .filters import ProductFilter
from .forms import ProductForm
from django.core.mail import send_mail

# class Products(View):
#     def get(self, request):
#         products = Product.objects.order_by('-price')
#         p = Paginator(products, 1)
#
#         products = p.get_page(request.GET.get('page', 1))
#         data = {
#             'products': products,
#         }
#         return render(request, 'products.html', data)

class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1
    # form_class = ProductForm # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())  # добавим переменную текущей даты time_now
        # context['categories'] = Category.objects.all()
        # context['form'] = ProductForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
    #
    #     if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
    #         form.save()
    #
    #     return super().get(request, *args, **kwargs)


# дженерик для получения деталей о товаре
class ProductDetailView(DetailView):
    template_name = 'sample_app/product_detail.html'
    queryset = Product.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class ProductCreateView(CreateView):
    template_name = 'sample_app/product_create.html'
    form_class = ProductForm

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
    #     context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
    #     return context


# class ProductDetail(DetailView):
#     model = Product
#     template_name = 'product.html'
#     context_object_name = 'product'


# дженерик для редактирования объекта
class ProductUpdateView(UpdateView):
    template_name = 'sample_app/product_create.html'
    form_class = ProductForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


# дженерик для удаления товара
class ProductDeleteView(DeleteView):
    template_name = 'sample_app/product_delete.html'
    queryset = Product.objects.all()
    success_url = '/products/'


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='vachrameev.oleg@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['ZigulatNatria@yandex.ru']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointments:make_appointment')