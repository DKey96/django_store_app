from django.urls import path, re_path

from store import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.product, name='detail'),
    #re_path('^electronics', views.electronics, name='electronics'),
    re_path('^electronics', views.ElectronicsView.as_view(), name='electronics'),
    re_path('listeletronics', views.ElectronicsViewList.as_view(), name='electronicslist'),
    path('equipment', views.EquipmentView.as_view()),
]
