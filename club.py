"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        raise NotImplementedError("core: check capacity and title, then store and return a new Event")

    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        raise NotImplementedError("core: look the event up, and turn a KeyError into UnknownEventError")

    def handle(self, line: str) -> str:
        """Answer one chat command, such as "join, Muay Thai basics, Nino", with one sentence."""
        raise NotImplementedError("core: answer a join or leave command, or say sorry")

    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        raise NotImplementedError("core: count each member's seats over all the events")


if __name__ == "__main__":
    # Provided: a short run of the chat bot. It runs only with `python club.py`, not on import.
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    for line in [
        "join, Muay Thai basics, Nino",
        "join, Muay Thai basics, Aung",
        "join, Muay Thai basics, Tashi",
        "leave, Muay Thai basics, Nino",
        "join, Chess night, Ploy",
    ]:
        print(club.handle(line))
