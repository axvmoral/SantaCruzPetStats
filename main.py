""" Module to run daily. """

__author__ = "Axel V. Morales Sanchez"

if __name__ == "__main__":
    with open("get_links.py") as file:
        exec(file.read())

    with open("update_database.py") as file:
        exec(file.read())
