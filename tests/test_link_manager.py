from golynx.infrastructure.database import Database
from golynx.services.link_manager import LinkManager 
from golynx.models.domain.golink import Golink
from .fixtures.database import database

link_manager = LinkManager(database=database)

def test_handle_existing_redirection():
    link_manager.database._data = {'pepe':'pepito'}
    assert link_manager.handle_redirection('pepe') == 'pepito'

def test_handle_default_redirection():
    link_manager.database._data = {}
    assert link_manager.handle_redirection('pepe') == 'https://www.chiquitoipsum.com/'
    
def test_handle_create_redirection():
    golink = Golink(link='lolo', redirection='lola')
    link_manager.handle_update(golink)
    assert link_manager.database._data == {'lolo': 'lola'}

def test_handle_update_redirection():
    golink1 = Golink(link='lolo', redirection='lola')
    golink2 = Golink(link='lolo', redirection='chill')
    link_manager.handle_update(golink1)
    link_manager.handle_update(golink2)
    assert link_manager.database._data == {'lolo': 'chill'}

def test_handle_delete():
    golink = Golink(link='lolo', redirection='lola')
    link_manager.handle_update(golink)
    link_manager.handle_delete(golink.link)
    assert link_manager.database._data == {}