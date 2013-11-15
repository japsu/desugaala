# DesuGaala voting system

A web app for voting stuff. Will be used to select the winners in DesuGaala 2012.

Copyright 2012-2013 Santtu Pajukanta. Licensed under the MIT license.

Includes Bootstrap v2.2.2, Copyright 2012 Twitter, Inc. Licensed under the Apache License v2.0.

## Getting Started

    virtualenv venv-desugaala
    source venv-desugaala/bin/activate
    git clone https://github.com/japsu/desugaala.git
    cd desugaala
    pip install git+https://github.com/japsu/phpbb-python.git
    pip install -r requirements.txt
    pip install your_database_adapter # hint: psycopg2 or MySQL-python
    cp desugaala/settings.py.dist desugaala/settings.py
    vim desugaala/settings.py
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py loaddata vote desugaala2012
    ./manage.py run_gunicorn
