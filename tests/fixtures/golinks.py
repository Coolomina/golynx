from golynx.models.domain.golink import Golink

GOLINK = Golink(
    link="lol",
    redirection="http://lol.com",
    created_by="pepe",
)

GOLINK_MODIFIED = Golink(
    link="lol",
    redirection="http://lolaso.com",
    created_by="pepe",
)

ANOTHER_GOLINK = Golink(
    link="pepino",
    redirection="http://pepsis.com",
    created_by="pepe",
)

DEFAULT_GOLINK = Golink(
    link="lol",
    redirection="lolo",
    created_by="default@default",
    times_used=0,
)
