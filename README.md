# A Cafe API

![License](https://img.shields.io/github/license/bbland1/sample-cafe-api?style=plastic)
![Top Language](https://img.shields.io/github/languages/top/bbland1/sample-cafe-api?style=plastic)
![Contributors](https://img.shields.io/github/contributors-anon/bbland1/sample-cafe-api?style=plastic)

A full REST API built using Flask and sample cafe data.

## Requirements

<!-- Installing from the [requirements.txt](./requirements.txt) handles most of the requirements. -->

## Built With

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [SQLAlchemy](https://www.sqlalchemy.org)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
<!-- * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) -->
<!-- * [python-dotenv](https://pypi.org/project/python-dotenv/)
* [flask-wtf](https://flask-wtf.readthedocs.io/en/1.0.x/) -->

### Local Development

1. (Optional) [Setup a virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it to install requirements into the virtual environment to run instead of your computers global environment.

2. Install the project requirements.

    ```shell
    pip install -r requirements.txt
    ```

3. Create a `.env` using the `.env.sample` file as a guide. Change `THEMOVIEDB_API_KEY`, `DB_STRING`, and `SECRET_KEY` to the proper information of your instance of the SQLite database.

    * `SECRET_KEY` can be set using this command

    ```shell  
    python -c 'import secrets; print(secrets.token_hex())'
    ```

4. Run the migrations

    ```shell
    flask db upgrade
    ```

5. Run the local server: (or use VS Code "Run" button and select "Run server")

    ```shell
    flask run
    ```

### License

See the [LICENSE](./LICENSE) file for license rights and limitations (MIT).
