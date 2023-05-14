import datetime
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Autor, Gatunek, Ksiazka, InstancjaKsiazki, Wydawca, Bibliotekarz
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Max, Min

# required imports for prolongata

from katalog.forms import ProlongataForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# required for user forms

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from katalog.models import Autor

# Create your views here.


def index(request):
    num_ks = Ksiazka.objects.all().count()
    num_in = InstancjaKsiazki.objects.all().count()
    num_in_d = InstancjaKsiazki.objects.filter(status__exact='d').count()
    num_au = Autor.objects.count()
    num_wyd = Wydawca.objects.count()
    num_bib = Bibliotekarz.objects.count()

    return render(
        request,
        'index.html',
        context={
            'num_ks': num_ks,
            'num_in': num_in,
            'num_in_d': num_in_d,
            'num_au': num_au,
            'num_wyd': num_wyd,
            'num_bib': num_bib

        }
    )


class AutorListView(generic.ListView):
    model = Autor
    context_object_name = 'autor_list'
    queryset = Autor.objects.all()
    template_name = 'autor_list.html'
    paginate_by = 5


class AutorSzczegolView(generic.DetailView):
    model = Autor
    template_name = 'autor_detail.html'


class AutorCreate(CreateView):
    model = Autor
    fields = ['imie', 'nazwisko', 'data_urodzenia', 'data_smierci']
    initial = {'data_smierci': '12/30/2070'}


class AutorUpdate(UpdateView):
    model = Autor
    fields = '__all__'


class AutorDelete(DeleteView):
    model = Autor
    success_url = reverse_lazy('autorzy')


class KsiazkaListView(generic.ListView):
    model = Ksiazka
    context_object_name = 'moja_ksiazka_list'
    queryset = Ksiazka.objects.all()
    template_name = 'ksiazka_moja_list.html'
    paginate_by = 3


class KsiazkaSzczegolView(generic.DetailView):
    model = Ksiazka
    template_name = 'ksiazka_detail.html'


class KsiazkaCreate(CreateView):
    model = Ksiazka
    fields = ['tytul', 'autor', 'opis', 'isbn', 'gatunek']
    initial = {'opis': 'Twoja kolejna dodana ksiazka'}


class KsiakzaUpdate(UpdateView):
    model = Ksiazka
    fields = '__all__'


class KsiazkaDelete(DeleteView):
    model = Ksiazka
    success_url = reverse_lazy('ksiazki')


class WydawcaListView(generic.ListView):
    model = Wydawca
    context_object_name = 'wydawca_list'
    queryset = Wydawca.objects.all()
    template_name = 'wydawca_list.html'
    paginate_by = 2


class WydawcaSzczegolView(generic.DetailView):
    model = Wydawca
    template_name = 'wydawca_detail.html'


class BibliotekarzListView(generic.ListView):
    model = Bibliotekarz
    context_object_name = 'bibliotekarz_list'
    queryset = Bibliotekarz.objects.all()
    template_name = 'bibliotekarz_list.html'
    paginate_by = 1


class BibliotekarzSzczegolView(generic.DetailView):
    model = Bibliotekarz
    template_name = 'bibliotekarz_detail.html'


class KsiazkiUzytkownikaListView(LoginRequiredMixin, generic.ListView):
    model = InstancjaKsiazki
    template_name = 'KsiazkiUzytkownika.html'
    paginate_by = 2

    def get_queryset(self):
        return InstancjaKsiazki.objects.filter(wypozycza=self.request.user).filter(status__exact='w').order_by('data_zwrotu')


@login_required
def prolonguj_ksiazka_bibliotekarz(request, pk):
    instancja = get_object_or_404(InstancjaKsiazki, pk=pk)

    if request.method == 'POST':
        form = ProlongataForm(request.POST)
        if form.is_valid():
            instancja.data_zwrotu = form.cleaned_data['data_prolongaty']
            instancja.save()
            return HttpResponseRedirect(reverse('moje-pozyczone'))
    else:
        nowa_data_prolongaty = datetime.date.today() + datetime.timedelta(weeks=3)
        form = ProlongataForm(
            initial={'data_prolongaty': nowa_data_prolongaty}
        )

    context = {
        'form': form,
        'instancja': instancja,
    }

    return render(request, 'katalog/prolonguj_ksiazka_bibliotekarz.html', context)


class Zapytania(generic.ListView):
    # mozna podmienić w zaleznosci od kontekstu i dac jedna wartosc, ja dalem wszystko i query wykorzysta te, ktore potrzebuje
    model = [Ksiazka, InstancjaKsiazki, Autor, Wydawca, Bibliotekarz, Gatunek]
    # obligatorka, podajemy obiekt do ktorego zapisujemy
    context_object_name = 'zapytania'
    # templatka, w naszym przypadku Zapytania.html
    template_name = 'Zapytania.html'

    # miejsce na twoje query, may the pepe be with you

    # 2. zawiera tytuly ksiazek z litera o (chyba jak egzemplarze, to chodzi o instancje)
    # queryset = InstancjaKsiazki.objects.filter(ksiazka__tytul__icontains='o')

    # 3. autor jest ABC (ABC == dowolny)
    # queryset = InstancjaKsiazki.objects.filter(ksiazka__autor__nazwisko='Lem')

    # 4. autorzy, ktorych ksiazki zawieraja litere 'o' w nazwie
    # queryset = Ksiazka.objects.filter(
    #     tytul__icontains='o').values_list('autor__nazwisko', 'autor__imie').distinct()

    # 5. gatunki ksiazek autora abc
    # queryset = Ksiazka.objects.values_list(
    #     'gatunek__nazwa', 'autor__nazwisko').filter(autor__nazwisko='Lem').distinct()

    # 6. wszystkie egzemplarze ksiazek ktorych autorem jest ABC i gatunek to DEF
    # queryset = InstancjaKsiazki.objects.filter(
    #     ksiazka__autor__nazwisko='Lem', ksiazka__gatunek__nazwa='sci-fi')

    # 7. wyswietlic liczbe ksiazek
    # queryset = Ksiazka.objects.all().count()

    # 8. wyswietlic autora i liczbe jego ksiazek w obiekcie QuerySet
    # queryset = Autor.objects.annotate(num_books=Count("ksiazka"))

    # 9. wyswietlic date urodzenia najstarszego autora'
    # queryset = Autor.objects.values('data_urodzenia', 'imie', 'nazwisko').annotate(
    #     najstarszy=Min('data_urodzenia'))[:1]
