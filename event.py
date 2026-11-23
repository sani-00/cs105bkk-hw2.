"""HW2 · event.py: one club event with limited seats. Practises Session 4 (a dataclass with
its own lists) and Session 6 (raising the club's exceptions)."""

from dataclasses import dataclass, field

from errors import AlreadySignedUpError, NotSignedUpError


@dataclass
class Event:
    """One event. Members in `seats` have a place; members in `waitlist` wait, first come first."""

    title: str
    capacity: int
    seats: list[str] = field(default_factory=list)
    waitlist: list[str] = field(default_factory=list)

    def seats_left(self) -> int:
        """Provided: how many seats are still free."""
        return self.capacity - len(self.seats)

    def sign_up(self, member: str) -> str:
        """Give the member a seat and return "seat", or add them to the waitlist and return "waitlist"."""
        raise NotImplementedError("core: give a seat or a waitlist place, or raise AlreadySignedUpError")

    def cancel(self, member: str) -> str | None:
        """Take the member off the event. Return who moves up from the waitlist, or None."""
        raise NotImplementedError("core: take the member off, and move the first waiting member up")

    def place(self, member: str) -> int:
        """0 for a member with a seat, or their number on the waitlist, counting from 1."""
        raise NotImplementedError("core: 0 for a seat, the waitlist number, or NotSignedUpError")
