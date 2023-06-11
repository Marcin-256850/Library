from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)

# Połączenie z bazą danych MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='matysiakowie',
    db='newlibrary'
)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Wykonanie zapytania do bazy danych w celu weryfikacji danych logowania
        cursor = connection.cursor()
        query = "SELECT * FROM user WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        # Zamknięcie kursora
        cursor.close()

        if user:
            # Jeśli dane logowania są poprawne, przekieruj na stronę wyszukiwarki książek
            session['user_id'] = user[0]
            return redirect('/menu')
        else:
            # Jeśli dane logowania są niepoprawne, wyświetl komunikat o błędzie
            error_message = "Nieprawidłowy email lub hasło"
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Pobranie danych z formularza rejestracji
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        phone = request.form['phone']

        # Sprawdzenie czy hasła są identyczne
        if password != password_confirm:
            error_message = "Hasła nie są identyczne"
            return render_template('register.html', error_message=error_message)

        # Sprawdzenie długości hasła
        if len(password) < 8 or len(password) > 45:
            error_message = "Hasło musi mieć od 8 do 45 znaków"
            return render_template('register.html', error_message=error_message)

        # Wykonanie zapytania do bazy danych w celu zapisania danych użytkownika
        cursor = connection.cursor()
        query = "INSERT INTO user (name, surname, email, password, telephone) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (firstname, lastname, email, password, phone))
        connection.commit()

        # Zamknięcie kursora
        cursor.close()

        # Przekierowanie na stronę logowania po zarejestrowaniu
        return render_template('login.html')

    return render_template('register.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


# Główna strona aplikacji
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Pobranie wartości z formularza wyszukiwania
        search_value = request.form['search_value']

        # Wykonanie zapytania do bazy danych
        cursor = connection.cursor()
        query = """
                SELECT book.title, GROUP_CONCAT(author.authorname SEPARATOR ', ') AS author_names, book.category, book.amount, book.publication, book.bookid
                FROM book
                INNER JOIN bookauthors ON book.bookid = bookauthors.bookid
                INNER JOIN author ON bookauthors.authorid = author.authorid
                WHERE book.title LIKE %s OR book.bookid IN (
                    SELECT bookauthors.bookid
                    FROM bookauthors
                    INNER JOIN author ON bookauthors.authorid = author.authorid
                    WHERE author.authorname LIKE %s
                ) OR book.category LIKE %s
                GROUP BY book.bookid
                """

        cursor.execute(query, (f'%{search_value}%', f'%{search_value}%', f'%{search_value}%'))
        books = cursor.fetchall()

        # Zamknięcie kursora
        cursor.close()

        return render_template('search.html', books=books, search_value=search_value)

    return render_template('search.html')


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    # Sprawdź, czy użytkownik jest zalogowany
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Pobierz identyfikator użytkownika z sesji
    user_id = session['user_id']

    if request.method == 'POST':
        # Pobierz identyfikator książki z formularza
        book_id = request.form.get('book_id')

        # Pobierz obecną datę i godzinę
        current_date = datetime.now()

        # Dodaj nowy rekord do tabeli borrow
        cursor = connection.cursor()
        insert_query = "INSERT INTO borrow (borrowdate, bookid, userid) VALUES (%s, %s, %s)"
        values = (current_date, book_id, user_id)
        cursor.execute(insert_query, values)
        connection.commit()

        # Zamknij kursor
        cursor.close()

        return redirect(url_for('borrow'))
    # Pobierz historię wypożyczeń dla użytkownika
    cursor = connection.cursor()
    query = """
        SELECT borrow.borrowid, borrow.borrowdate, borrow.returndate, book.title
        FROM borrow
        INNER JOIN book ON borrow.bookid = book.bookid
        WHERE borrow.userid = %s
    """
    cursor.execute(query, (user_id,))
    history = cursor.fetchall()

    # Zamknięcie kursora
    cursor.close()

    return render_template('borrow.html', history=history)


@app.route('/return_book/<int:borrow_id>', methods=['POST'])
def return_book(borrow_id):
    # Pobierz obecną datę i godzinę
    current_date = datetime.now()

    cursor = connection.cursor()

    # Aktualizuj rekord wypożyczenia o podanym borrow_id
    update_query = "UPDATE borrow SET returndate = %s WHERE borrowid = %s"
    values = (current_date, borrow_id)
    cursor.execute(update_query, values)
    connection.commit()

    # Zamknij kursor
    cursor.close()

    return redirect(url_for('borrow'))


app.secret_key = 'unikalnyklucz'
if __name__ == '__main__':
    app.run()