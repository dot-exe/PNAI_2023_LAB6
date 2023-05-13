from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    # autorzy
    path('autorzy/', views.AutorListView.as_view(), name='autorzy'),
    path('autor/<int:pk>/', views.AutorSzczegolView.as_view(), name='autor-detail'),
    path('autor/create/', views.AutorCreate.as_view(), name='autor-create'),
    path('autor/<int:pk>/update/', views.AutorUpdate.as_view(), name='autor-update'),
    path('autor/<int:pk>/delete/', views.AutorDelete.as_view(), name='autor-delete'),

    # wydawcy
    path('wydawcy/', views.WydawcaListView.as_view(), name='wydawcy'),
    path('wydawca/<int:pk>', views.WydawcaSzczegolView.as_view(),
         name='wydawca-detail'),

    # ksiazki
    path('ksiazki/', views.KsiazkaListView.as_view(), name='ksiazki'),
    path('ksiazki/<uuid:pk>/prolonguj/', views.prolonguj_ksiazka_bibliotekarz,
         name='prolonguj-ksiazka-bibliotekarz'),
    path('ksiazka/<int:pk>', views.KsiazkaSzczegolView.as_view(),
         name='ksiazka-detail'),
    path('ksiazka/create/', views.KsiazkaCreate.as_view(), name='ksiazka-create'),
    path('ksiazka/<int:pk>/update/',
         views.KsiakzaUpdate.as_view(), name='ksiazka-update'),
    path('ksiazka/<int:pk>/delete/',
         views.KsiazkaDelete.as_view(), name='ksiazka-delete'),

    # bibliotekarze
    path('bibliotekarze/', views.BibliotekarzListView.as_view(), name='bibliotekarze'),
    path('bibliotekarz/<int:pk>', views.BibliotekarzSzczegolView.as_view(),
         name='bibliotekarz-detail'),

    # ksiazki uzytkownika
    path('mojeksiazki/', views.KsiazkiUzytkownikaListView.as_view(),
         name='moje-pozyczone'),

    # template pod zapytania
    path('zapytania/', views.Zapytania.as_view(), name='zapytania'),
]
