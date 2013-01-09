## Getting Started

    virtualenv venv-desugaala
    source venv-desugaala/bin/activate
    git clone https://github.com/japsu/desugaala.git
    cd desugaala
    pip install -r requirements.txt
    pip install your_database_adapter # hint: psycopg2 or MySQL-python
    cp desugaala/settings.py.dist desugaala/settings.py
    vim desugaala/settings.py
    ./manage.py run_gunicorn
