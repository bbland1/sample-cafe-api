# A Cafe API

![License](https://img.shields.io/github/license/bbland1/sample-cafe-api?style=plastic)
![Top Language](https://img.shields.io/github/languages/top/bbland1/sample-cafe-api?style=plastic)
![Contributors](https://img.shields.io/github/contributors-anon/bbland1/sample-cafe-api?style=plastic)

A full REST API built using Flask and sample cafe data.

## Requirements

Install from the [requirements.txt](./requirements.txt), or use Poetry Method.

## Built With

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [SQLAlchemy](https://www.sqlalchemy.org)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
<!-- * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/) -->
<!-- 
* [flask-wtf](https://flask-wtf.readthedocs.io/en/1.0.x/) -->

### Local Development

#### Poetry Method
1. Install [Poetry](https://python-poetry.org/docs/)
2. Using poerty install all dependencies from the `poetry.lock` and `pyproject.toml`

    ```shell
    poetry install
    ```

#### Requirements.txt Method
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
    
### Deployment
This API is not currently deployed, but the documentation created using [Postman](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiX3oPTr__-AhV1TTABHfCTCkEQFnoECCIQAQ&url=https%3A%2F%2Fwww.postman.com%2F&usg=AOvVaw05sjAjE_hbftSn2Ii8YG6N) to show how the routes and API would be used can be found [here](https://documenter.getpostman.com/view/21696355/2s93kz768G).

### License

See the [LICENSE](./LICENSE) file for license rights and limitations (MIT).
