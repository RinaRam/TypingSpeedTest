Подготовка
==========

Предлагается запускать приложение из-под виртуального окружения с помощью pipenv (гарантируется, что указаны все необходимы установки). Однако и без виртуального окружения приложение тоже будет работать.

Выполните следующие команды::

    mkdir TestApp
    cd TestApp
    pip3 install pipenv
    pipenv shell
    git clone git@github.com:CatherineFish/TypingSpeedTest.git
    cd TypingSpeedTest
    pip3 install doit build babel # основные модули
    pip3 install sphinx flake8 pydocstyle # дополнительные модули
    doit wheel
    cd ..
    mkdir test_wheel
    cd test_wheel
    TODO

Запуск
======

Для запуска приложения на английском языке выполните::

    LC_ALL="en_US.UTF-8" python3 app/main.py

Для запуска приложения на русском языке выполните::

    LC_ALL="ru_RU.UTF-8" python3 app/TypingSpeedTest

Для выхода из виртуального окружения необходимо выполнить команду::

    exit

Задачи doit
===========

Задача pot
----------

.. code-block:: bash

    doit pot

Эта задача пересоздает шаблон .pot. Она выполняет следующую команду:

.. code-block:: bash

    pybabel extract -F babel.cfg -o messages.pot .

Задача po
---------

.. code-block:: bash

    doit po

Эта задача обновляет перевод. Она выполняет следующую команду:

.. code-block:: bash

    pybabel update -D messages -d ./app/translations -i messages.pot

Задача mo
----------

.. code-block:: bash

    doit mo

Эта задача компилирует перевод. Она создает необходимые папки и выполняет следующую команду:

.. code-block:: bash

    pybabel compile -d app/translations

Задача myclean
---------------

.. code-block:: bash

    doit myclean

Эта задача очищает все генерированные файлы. Она выполняет следующую команду:

.. code-block:: bash

    git clean -fdx

Задача test
-----------

.. code-block:: bash

    doit test

Эта задача запускает все тесты. Она выполняет следующую команду:

.. code-block:: bash

    python3 -m unittest -v

