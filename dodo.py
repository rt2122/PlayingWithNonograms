"""Doit file."""

DOIT_CONFIG = {'default_tasks': ['all']}


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -xdf'],
           }


def task_html():
    """Make HTML documentationi."""
    return {
            'actions': ['sphinx-build -b html docs/source docs/_build'],
            'task_dep': ['mo']
           }


def task_test():
    """Preform tests."""
    yield {'actions': ['pytest --cov=PlayingWithNonograms'], 'task_dep':['mo'], 'name': "run"}
    yield {'actions': ['coverage report'], 'task_dep': ['test:run'], 'verbosity': 2, 'name': "report"}


def task_mo():
    """Compile translations."""
    yield {
        'actions': ['pybabel compile -i PlayingWithNonograms/po/ru/LC_MESSAGES/messages.po -o PlayingWithNonograms/po/ru/LC_MESSAGES/PWN.mo'],
        'file_dep': ['PlayingWithNonograms/po/ru/LC_MESSAGES/messages.po'],
        'targets': ['PlayingWithNonograms/po/ru/LC_MESSAGES/PWN.mo'],
        'name': 'mo_ru'
    }
    yield {
        'actions': ['pybabel compile -i PlayingWithNonograms/po/en/LC_MESSAGES/en.po -o PlayingWithNonograms/po/en/LC_MESSAGES/PWN.mo'],
        'file_dep': ['PlayingWithNonograms/po/en/LC_MESSAGES/en.po'],
        'targets': ['PlayingWithNonograms/po/en/LC_MESSAGES/PWN.mo'],
        'name': 'mo_en'
    }


def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s'],
            'task_dep': ['gitclean'],
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -w'],
            'task_dep': ['mo'],
           }


def task_app():
    """Run application."""
    return {
            'actions': ['python -m PlayingWithNonograms'],
            'task_dep': ['mo'],
           }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 PlayingWithNonograms']
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle PlayingWithNonograms']
           }


def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle', 'test']
           }


def task_all():
    """Perform all build task."""
    return {
            'actions': None,
            'task_dep': ['check', 'html', 'wheel']
           }


def task_req():
    """Generate runtime requirements."""
    return {
            'actions': ['pipreqs --savepath requirements.txt PlayingWithNonograms'],
            'targets': ['requirements.txt'],
            'clean': True,
           }


# def task_buildreq():
#     """Try to calculate build requirements."""
#     return {
#             'actions': ['python BuildReq.py doit all'],
#             'task_dep': ['gitclean']
#            }


# def task_publish():
#     """Publish distros on test.pypi.org"""
#     return {
#             'task_dep': ['sdist', 'wheel'],
#             'actions': ['twine upload -u __token__ --repository testpypi dist/*'],
#             'verbosity': 2
#            }