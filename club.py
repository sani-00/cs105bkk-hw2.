"""HW2 · club.py: the club and its chat bot. Practises Session 4 (each class has one job),
Session 5 (importing your own modules and the standard library) and Session 6 (catching only
the errors you expect)."""

from errors import SignupError, UnknownEventError
from event import Event
from collections import Counter


class Club:
    """A student club. It finds events by title; each Event looks after its own seats."""

    def __init__(self, name: str):
        """Provided: a club with no events yet."""
        self.name = name
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, capacity: int) -> Event:
        """Make a new Event, store it under its title, and return it."""
        if title in self.events.keys() or capacity <= 0:
            raise ValueError

        event = Event(title, capacity)
        self.events[title] = event

        return event

    def event(self, title: str) -> Event:
        """Return the event with this title, or raise UnknownEventError."""
        try:
            return self.events[title]
        except KeyError:
            raise UnknownEventError(title)
        
    def handle(self, line: str) -> str:
        """Answer one chat command, such as "join, Muay Thai basics, Nino", with one sentence."""
        try:
            command, title, member = [x.strip() for x in line.split(",")]
        except ValueError:
            return f"Sorry, I don't understand {line!r}."

        command = command.lower()
        event = self.event(title)

        if command == "join":
            try:
                sign_up_result = event.sign_up(member)
            except SignupError as e:
                return f"Sorry, {e}."

            if sign_up_result == "seat":
                return f"{member} has a seat at {title}."
            elif sign_up_result == "waitlist":
                return f"{member} is on the waitlist for {title}."

        elif command == "leave":
            cancel_result = event.cancel(member)

            return f"{member} left {event.title}.{f' {cancel_result} gets the seat.' if cancel_result else ''}"

        raise RuntimeError
    
    def attendance(self) -> dict[str, int]:
        """How many events each member has a seat at. The waitlist does not count."""
        return dict(Counter(member for event in self.events.values() for member in event.seats))

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
