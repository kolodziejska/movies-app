## REST API aplikacji filmowej

### Funkcjonalności aplikacji
- tworzenie nowego użytkownika na podstawie adresu email
- logowanie użytkownika (email + hasło) - autoryzacja za pomocą tokena
- edytowanie hasła i nazwy użytkownika przez panel użytkownika
- listowanie filmów
- filtrowanie filmów po tytule lub gatunku
- sortowanie filmów po tytule lub średniej ocenie
- dodawanie filmów i aktorów przez adminów strony
- wyświetlanie filmu wraz z jego ocenami
- dodawanie oceny przez zalogowanego użytkownika
- edycja ocen przez panel użytkownika
- wyświetlanie aktora i reżysera wraz z listą filmów

### Użyte narzędzia i technologie
- Docker
- Python 3.9
- Django 3.2.4
- Django REST framework 3.12.4
- Postgres 13

### Diagram ERD

### API

| Endpoint | metoda | opis | uprawnienie |
|----------|--------|------|-------------|
| api/user/signup/ | POST | *tworzenie użytkownika* | - |
| api/user/token/ | GET | *uwierzytelnianie* | - |
| api/user/me/ | GET | *wyświetlanie zalogowanego użytkownika* | `IS_AUTHORIZED` |
| api/user/ratings/ | GET | *listowanie ocen zalogowanego użytkownika* | `IS_AUTHORIZED` |
| api/user/ratings/{id}/ | GET | *wyświetlanie oceny zalogowanego użytkownika* | `IS_AUTHORIZED` |
| api/user/ratings/{id}/ | PATCH | *edycja oceny zalogowanego użytkownika* | `IS_AUTHORIZED` |
| api/movie/movies/ | GET | *listowanie filmów* | - |
| api/movie/movies?order_by={value}/ | GET | *sortowanie filmów; możliwe wartości to title lub rating* | - |
| api/movie/movies?title={value}/ | GET | *filtrowanie filmów po tytule* | - |
| api/movie/movies?genre={value}/ | GET | *filtrowanie filmów po gatunku* | - |
| api/movie/movies/{slug}/ | GET | *wyświetlanie filmu* | - |
| api/movie/movies/{slug}/add_rating/ | POST | *dodawanie oceny dla filmu o danym slug przez zalogowanego użytkownika* | `IS_AUTHORIZED` |
| api/movie/artist/{slug}/ | GET | *wyświetlanie aktora lub reżysera" | - |

### Jak uruchomić

W terminalu przejść do folderu zawierającego projekt i wykonać komendę:

```
docker-compose up --build
```
Po uruchomieniu kontenerów API dostępne jest w przeglądarce pod adresem `http://localhost:8000`.

Aby zalogować się do panelu administracyjnego Django należy stworzyć superusera:
```
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
Aby załadować przykładowe dane należy:
1. Pobrać plik csv z: https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows
2. Umieścić plik w folderze app/example_data
3. Uruchomić komendę:
```
docker-compose run --rm app sh -c "python manage.py runscript example_data.import_data"
```