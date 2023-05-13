from django.contrib import admin

# Register your models here.

from .models import Autor, Gatunek, Ksiazka, InstancjaKsiazki, Bibliotekarz, Wydawca

# admin.site.register(Autor)
# admin.site.register(Gatunek)
# admin.site.register(Ksiazka)
# admin.site.register(InstacjaKsiazki)
# admin.site.register(Bibliotekarz)
# admin.site.register(Wydawca)


# admin.site.register(Autor, AutorAdmin)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nazwisko', 'imie', 'data_urodzenia', 'data_smierci')


@admin.register(Gatunek)
class GatunekAdmin(admin.ModelAdmin):
    display = 'nazwa'


@admin.register(Ksiazka)
class KsiazkaAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'display_gatunek')


@admin.register(InstancjaKsiazki)
class InstancjaKsiazkiAdmin(admin.ModelAdmin):
    list_filter = ('status', 'data_zwrotu')


@admin.register(Bibliotekarz)
class BibliotekarzAdmin(admin.ModelAdmin):
    list_display = ('nazwisko', 'imie', 'data_zatrudnienia', 'stanowisko')


@admin.register(Wydawca)
class WydawcaAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'miasto', 'data_zalozenia', 'krs')
#
