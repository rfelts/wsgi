#!/usr/bin/env python3

# Russell Felts
# Exercise 04 Book Server

import traceback

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    return "<h1>a book with id %s</h1>" % book_id


def books():
    """
    Creates a list of all the books in the db
    :return: A string containing html representing a list of the books in the db
    """
    all_books = DB.titles()
    body = ['<h1>My Bookshelf</h1>', '<ul>']
    item_template = '<li><a href="/book/{id}">{title}</a></li>'
    for book in all_books:
        body.append(item_template.format(**book))
    body.append('</ul>')
    return '\n'.join(body)


def resolve_path(path):
    """
    Take the request and determine the function to call
    :param path: string representing the requested page
    :return: func - the name of the requested function,
            args - the arguments required for the requested function
    """
    funcs = {
        '': books,
        'book': book
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """
    Handle incoming requests and route them to the appropriate function
    :param environ: dictionary that contains all of the variables from the WSGI server's environment
    :param start_response: the start response method
    :return: the response body
    """
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
