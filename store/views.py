from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView


def index(request):
    return HttpResponse("Hello there, e-commerce store font coming here...")


def product(request, id):
    return HttpResponse(f"Product with id: {id}")


@csrf_exempt
@cache_page(0)  # takes cache timeout
@require_http_methods(["GET"])  # will check if incomming request is in allowed method, otherwise 405
def electronics(request):
    items = ("Windows PC", "Apple Mac", "Apple Iphone", "Lenovo", "Samsung", "Google")
    paginator = Paginator(items, 2)  # Used for adding paginations, where number is a count of elements for one "page"
    pages = request.GET.get('page', 1)
    try:
        items = paginator.page(pages)
    except PageNotAnInteger:
        items = paginator.page(1)
    return render(request, "store/list.html", {"items": items})


'''Classed based views'''


class ElectronicsView(View):
    def get(self, request):
        items = ("Windows PC", "Apple Mac", "Apple Iphone", "Lenovo", "Samsung", "Google")
        paginator = Paginator(items,
                              2)  # Used for adding paginations, where number is a count of elements for one "page"
        pages = request.GET.get('page', 1)
        name = "Daniel"

        self.process()
        try:
            items = paginator.page(pages)
        except PageNotAnInteger:
            items = paginator.page(1)
        # setting customer name to the session (no cache) so its secure
        if not 'customer' in request.session:
            request.session['customer'] = name
            print('Session value set customer')
        response = render(request, "store/list.html", {"items": items})
        # adding a coockie to the response
        if request.COOKIES.get("visits"):
            value = int(request.COOKIES.get("visits"))
            print("Getting coockie.")
            response.set_cookie('visits', value + 1)
        else:
            print("Setting coockie.")
            response.set_cookie('visits', 1)
        return response

    @staticmethod
    def process():
        print("We are processing Electronics")

class LogoutView(View):
    def get(self, request):
        try:
            del request.session["customer"]
        except KeyError:
            print("Error while logging our.")
        return HttpResponse("You are logged out.")
'''Deprecated -> Not used. Just for testing different behaviors of Django views models'''

class ElectronicsViewExplTemp(TemplateView):
    template_name = 'store/list.html'

    def get_context_data(self, **kwargs):
        items = ("Windows PC", "Apple Mac", "Apple Iphone", "Lenovo", "Samsung", "Google")
        context = {"items": items}
        return context


class ElectronicsViewList(ListView):
    template_name = 'store/list.html'
    queryset = ("Windows PC", "Apple Mac", "Apple iPhone", "Lenovo", "Samsung", "Google")
    context_object_name = 'items'
    paginate_by = 2


class ComputersView(ElectronicsView):
    def process(self):
        print("We are processing Computers")


class MobileView:
    @staticmethod
    def process():
        print("We are processing phones")


# Mixit (multi-inheritance) goes every time from first parent
# if method is not in first parent, it goes to the next one
# otherwise runs the method of first parent
class EquipmentView(MobileView, ComputersView):
    pass
