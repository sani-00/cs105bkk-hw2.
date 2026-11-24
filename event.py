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
        if member in self.seats or member in self.waitlist:
            raise AlreadySignedUpError(member, self.title)

        if self.capacity > len(self.seats):
            self.seats.append(member)

            return "seat"
        else:
            self.waitlist.append(member)

            return "waitlist"

    def cancel(self, member: str) -> str | None:
        """Take the member off the event. Return who moves up from the waitlist, or None."""
        if member in self.waitlist:
            self.waitlist.remove(member)

            return

        if member in self.seats:
            self.seats.remove(member)

            if self.waitlist:
                seat_replaced_by = self.waitlist.pop(0)
                self.seats.append(seat_replaced_by)

                return seat_replaced_by

            return

        raise NotSignedUpError(member, self.title)

    def place(self, member: str) -> int:
        """0 for a member with a seat, or their number on the waitlist, counting from 1."""
        if member in self.seats:
            return 0

        try:
            return self.waitlist.index(member) + 1
        except ValueError:
            raise NotSignedUpError(member, self.title)