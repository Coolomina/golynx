class ApiRoutes:
    base = "/api"
    golinks = base + "/golinks"
    golink_update = base + "/golink"
    golink_delete = base + "/golink/{link}"


class GoRoutes:
    base = "/go"
    link = base + "/{link}"


class ConfigRoutes:
    base = "/config"
