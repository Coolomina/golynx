import logging
import supabase

from golynx.config import Config
from golynx.infrastructure.database.base import BaseDatabase
from golynx.models.domain.golink import Golink

logger = logging.getLogger("infrastructure/supabase")


class SupabaseDatabase(BaseDatabase):
    default_redirection = Golink(
        link="default",
        redirection=Config.DEFAULT_REDIRECTION,
        created_by=Config.DEFAULT_USER,
    )

    def __init__(self):
        self.client = supabase.create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

    def initialize(self, storage):
        pass

    def get(self, link: str) -> Golink:
        response = self.client.table("golynx").select("*").eq("link", link).execute()
        if len(response.data) == 0:
            return self.default_redirection
        golink = response.data[0]
        self.client.table("golynx").update({"times_used": golink["times_used"] + 1}).eq(
            "link", golink["link"]
        ).execute()

        return Golink(
            link=golink["link"],
            redirection=golink["redirection"],
            created_by=golink["created_by"],
            times_used=golink["times_used"] + 1,
        )

    def increment(self, link: str):
        pass

    def set(self, golink: Golink):
        self.client.table("golynx").upsert(
            golink.__dict__,
            on_conflict="link"
        ).execute()

    def delete(self, link: str):
        self.client.table("golynx").delete().eq("link", link).execute()

    def update(self, link: str, golink: Golink):
        pass

    def get_all(self, as_dict=True):
        response = self.client.table("golynx").select("*").order("times_used", desc=True).execute()
        raw_golinks = response.data
        golinks = {}
        for raw_golink in raw_golinks:
            if as_dict:
                golinks[raw_golink["link"]] = raw_golink
            else:
                golinks[raw_golink["link"]] = Golink(
                    link=raw_golink["link"],
                    redirection=raw_golink["redirection"],
                    created_by=raw_golink["created_by"],
                    times_used=raw_golink["times_used"],
                )
        return golinks

    def truncate(self):
        self.client.table("golynx").delete().neq("link", "").execute()

    def flush(self):
        pass
