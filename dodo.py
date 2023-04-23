from doit.tools import create_folder

def task_pot():
    """Пересоздать шаблон .pot ."""
    return {'actions': ['pybabel extract -o messages.pot ./'],
            'targets': ['messages.pot'], }

def task_po():
    """Обновить перевод."""
    return {'actions': ['pybabel update -D messages -d translations -i messages.pot'],
            'file_dep': ['messages.pot'],
            'targets': ['translations/ru/LC_MESSAGES/messages.po'], }

def task_mo():
    """Скомпилировать перевод."""
    return {'actions': [(create_folder,
                        ['translations/ru/LC_MESSAGES']),
                        'pybabel compile -d translations'],
            'file_dep': ['translations/ru/LC_MESSAGES/messages.po'],
            'targets': ['translations/ru/LC_MESSAGES/messages.mo'], }

def task_myclean():
    """Очистка всех генератов."""
    return {'actions': ['git clean -fdx'], }
