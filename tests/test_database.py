import pytest

from golinks.infrastructure.database import Database 
from .fixtures.database import setup_database
from .fixtures.database import database

def test_initialize_database(setup_database):
    assert database._data != None, "Database has not been initialized"
    
def test_get_default_redirection(setup_database):
    assert database.get('test') == database.default_redirection

def test_get_created_redirection(setup_database):
    database.set('lol', 'lel')
    assert database.get('lol') == 'lel'

def test_set(setup_database):
    database.set('lol', 'lol.com')
    assert database._data['lol'] == 'lol.com'

def test_delete(setup_database):
    database._data['lol'] = 'lol.com'
    database.delete('lol')
    assert database._data == {}
    