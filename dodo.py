from doit.tools import create_folder

def task_pot():
    """Пересоздать шаблон .pot ."""
    return {'actions': ['pybabel extract -F babel.cfg -o messages.pot .'],
            'targets': ['messages.pot'], }

def task_po():
    """Обновить перевод."""
    return {'actions': ['pybabel update -D messages -d ./app/translations -i messages.pot'],
            'file_dep': ['messages.pot'],
            'targets': ['app/translations/ru/LC_MESSAGES/messages.po'], }

def task_mo():
    """Скомпилировать перевод."""
    return {'actions': [(create_folder,
                        ['app/translations/ru/LC_MESSAGES']),
                        'pybabel compile -d app/translations'],
            'file_dep': ['app/translations/ru/LC_MESSAGES/messages.po'],
            'targets': ['app/translations/ru/LC_MESSAGES/messages.mo'], }

def task_myclean():
    """Очистка всех генератов."""
    return {'actions': ['git clean -fdx'], }


def task_test():
    """Запустить тесты."""
    return {'actions': ['python3 -m unittest -v'], }


def task_sdist():
    """Сборка архива с исходниками."""
    return {'actions': ['python3 -m build -s'],
            'task_dep': ['myclean'], }


def task_wheel():
    """Сборка wheel."""
    return {'actions': ['pyproject-build -w -n'],
            'task_dep': ['mo'], }


def task_html():
    """Создание HTML документации."""
    return {'actions': ['sphinx-build -M html doc build'], }


def task_style():
    """Проверка стиля кода согласно flake8."""
    return {'actions': ['flake8 app']}


def task_docstyle():
    """Проверка стиля кода согласно pydocstyle."""
    return {'actions': ['pydocstyle app']}