Technologie: Python 3.10+, Django, DRF, PostgreSQL, Celery, Git

Opis zadania
Zaprojektuj i zaimplementuj REST API umożliwiające wysyłkę wiadomości e-mail:
na dowolne adresy,
o treści i temacie zdefiniowanych w szablonie ( Template ),
z wcześniej zdefiniowanej skrzynki nadawczej ( Mailbox ).

Wymagania techniczne
1. Architektura REST – endpointy zgodne z konwencją RESTful.
2. Konfiguracja bazy danych przechowywana przez django-environ.
3. Wysyłka tylko z aktywnej skrzynki – skrzynka musi mieć status is_active=True .
4. Wysyłka asynchroniczna – realizowana jako task Celery w obrębie tej samej aplikacji.
5. Retry policy – maksymalnie 3 próby wysyłki wiadomości.
6. Logowanie błędów – skonfigurowany logganie (z użyciem django-filter ):
według statusu wysłania (czy sent_date jest uzupełnione),
według daty utworzenia.
7. Filtrowp. drf-spectacular lub drf-yasg ).
8. Dokumentacja API – Swagger (ner zapisujący do logs/email.log .
9. Workflow Git – projekt rozwijany zgodnie z GitHub Flow.
10. README – instrukcja uruchomienia projektu.