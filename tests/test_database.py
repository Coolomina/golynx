from tests.fixtures.golinks import GOLINK
from .fixtures.database import setup_database
from .fixtures.database import database
import copy


def test_initialize_database(setup_database):
    assert database._data != None, "Database has not been initialized"


def test_get_default_redirection(setup_database):
    assert database.get("test") == database.default_redirection


def test_get_created_redirection(setup_database):
    database.set(GOLINK)
    assert database.get(GOLINK.link) == GOLINK


def test_set(setup_database):
    database.set(GOLINK)
    assert database._data[GOLINK.link] == GOLINK


def test_set_existing(setup_database):
    updated_golink = copy.deepcopy(GOLINK)
    updated_golink.redirection = "pepe"
    database.set(GOLINK)
    database.set(updated_golink)
    assert GOLINK.times_used == updated_golink.times_used


def test_delete(setup_database):
    database._data[GOLINK.link] = GOLINK
    database.delete(GOLINK.link)
    assert database._data == {}


def test_get_all(setup_database):
    database.set(GOLINK)
    assert database.get_all() == {GOLINK.link: GOLINK.__dict__}


def test_get_all_empty(setup_database):
    assert database.get_all() == {}


def test_increment(setup_database):
    database._data[GOLINK.link] = GOLINK
    database.increment(GOLINK.link)
    assert database._data[GOLINK.link].times_used == 1
