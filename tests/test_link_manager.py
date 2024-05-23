from golynx.services.link_manager import LinkManager 
from tests.fixtures.golinks import GOLINK, GOLINK_MODIFIED
from .fixtures.database import database

link_manager = LinkManager(database=database)

def test_handle_existing_redirection():
    link_manager.database._data = { GOLINK.link: GOLINK }
    assert link_manager.handle_redirection(GOLINK.link) == GOLINK.redirection

def test_handle_default_redirection():
    link_manager.database._data = {}
    assert link_manager.handle_redirection('pepe') == 'https://www.chiquitoipsum.com/'
    
def test_handle_create_redirection():
    link_manager.handle_update(GOLINK)
    assert link_manager.database._data == {GOLINK.link: GOLINK}

def test_handle_update_redirection():
    link_manager.handle_update(GOLINK)
    link_manager.handle_update(GOLINK_MODIFIED)
    assert link_manager.database._data == {GOLINK.link: GOLINK_MODIFIED}

def test_handle_delete():
    link_manager.handle_update(GOLINK)
    link_manager.handle_delete(GOLINK.link)
    assert link_manager.database._data == {}