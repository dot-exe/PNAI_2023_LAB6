# PNAI_2023_LAB6
A simple Python + Django project carried out as a part of the subject "Programowanie Nowoczesnych Aplikacji Internetowych"

## Visual Studio Code addons
### Python pack
_NOTE: make sure you install the proper package. Correct one should contain Pylance, Linting, Jupyter Notebooks etc._
```
Name: Python
Id: ms-python.python
Description: IntelliSense (Pylance), Linting, Debugging (multi-threaded, remote), Jupyter Notebooks, code formatting, refactoring, unit tests, and more.
Version: 2022.20.2
Publisher: Microsoft
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=ms-python.python
```

### Django snippets
```
Name: Djaneiro - Django Snippets
Id: thebarkman.vscode-djaneiro
Description: A collection of snippets for django templates, models, views, fields & forms. Ported from Djaneiro for SublimeText
Version: 1.4.2
Publisher: Scott Barkman
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=thebarkman.vscode-djaneiro
```

### Jinja
_NOTE: usefull for creating blocks in HTML templates_
```
Name: Jinja
Id: wholroyd.jinja
Description: Jinja template language support for Visual Studio Code
Version: 0.0.8
Publisher: wholroyd
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=wholroyd.jinja
```

## Install required dependencies 
### Python
This project is based on Python 3.10.7. Please consider to use mentioned version or higher.
### Django
Use `pip install django` in your terminal to install the newest version of Django. If you want to install the one used in this project (4.2.1) use `pip install django=4.2.1` to specify.
### Check setup
Make sure, that Python and Django are installed. Run `python --version` and `python -m django --version` to check that.
## Run project
To run this project:
+ Open terminal and go to the directory with `manage.py` script
  + `cd biblioteka`
+ Make migration of your models to a database
  + `python manage.py makemigrations`
  + then `python manage.py migrate`
+ If migration ended succesfully (you should have `migrations` folder in your `katalog` app)
  + `python manage.py runserver`

After running your app, the main part will be available at `https:localhost:8000/katalog/`, the admin panel is running at `https:localhost:8000/admin/`

## Tasks - Queries

Example solution:
***for /biblioteka/katalog/views.py***
```
# 2. zawiera tytuly ksiazek z litera o
queryset = InstancjaKsiazki.objects.filter(ksiazka__tytul__icontains='o')

# 3. autor jest ABC (ABC == dowolny)
queryset = InstancjaKsiazki.objects.filter(ksiazka__autor__nazwisko='Lem')

# 4. autorzy, ktorych ksiazki zawieraja litere 'o' w nazwie
queryset = Ksiazka.objects.filter(tytul__icontains='o').values_list('autor__nazwisko', 'autor__imie').distinct()

# 5. gatunki ksiazek autora abc
queryset = Ksiazka.objects.values_list('gatunek__nazwa', 'autor__nazwisko').filter(autor__nazwisko='Lem').distinct()

# 6. wszystkie egzemplarze ksiazek ktorych autorem jest ABC i gatunek to DEF
queryset = InstancjaKsiazki.objects.filter(ksiazka__autor__nazwisko='Lem', ksiazka__gatunek__nazwa='sci-fi')

# 7. wyswietlic liczbe ksiazek
queryset = Ksiazka.objects.all().count()

# 8. wyswietlic autora i liczbe jego ksiazek w obiekcie QuerySet
queryset = Autor.objects.annotate(num_books=Count("ksiazka"))

# 9. wyswietlic date urodzenia najstarszego autora'
queryset = Autor.objects.values('data_urodzenia', 'imie', 'nazwisko').annotate(
        najstarszy=Min('data_urodzenia'))[:1]
```

***for /biblioteka/katalog/templates/Zapytania.html***
_How to display queries_
```
<ul>
  <!-- {% for z in zapytania %} -->
  <li>
    <!-- 2 -->
    <!-- {{ z.ksiazka.tytul }}, ({{ z.ksiazka.autor.imie }} {{ z.ksiazka.autor.nazwisko }}) -->
    <!-- 3 -->
    <!-- {{ z.ksiazka.tytul }}, ({{ z.ksiazka.autor.imie }} {{ z.ksiazka.autor.nazwisko }}) -->
    <!-- 4 -->
    <!-- {{ z }} -->
    <!-- 5 -->
    <!-- {{ z }} -->
    <!-- 6 -->
    <!-- {{ z }} -->
    <!-- 7 -->
    <!-- Ilosc zarejestrowanych tytulow ksiazek: {{ zapytania }} -->
    <!-- 8 -->
    <!-- {{ z }}: {{ z.num_books }} -->
    <!-- 9 -->
    <!-- Najstarszym autorem ksiazki w naszej bazie jest: {{ z.imie }} {{ z.nazwisko }} ({{ z.najstarszy }}) -->
  </li>
  <!-- {% endfor %} -->
</ul>
```

