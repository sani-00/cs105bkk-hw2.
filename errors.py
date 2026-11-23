"""HW2 · errors.py: the club's own exceptions. Practises Session 6: custom exception classes
that share one parent and carry the details for whoever catches them."""


class SignupError(Exception):
    """Provided: the parent of every sign-up problem, so one except can catch them all."""


class NotSignedUpError(SignupError):
    """Provided: the member has no seat and is not on the waitlist."""

    def __init__(self, member: str, event: str):
        """Provided: give the parent the message, then keep member and event."""
        super().__init__(f"{member} is not signed up for {event}")
        self.member = member
        self.event = event


class AlreadySignedUpError(SignupError):
    """The member already has a seat, or is already on the waitlist."""

    def __init__(self, member: str, event: str):
        """Give the parent the message, then keep member and event for whoever catches it."""
        raise NotImplementedError("core: AlreadySignedUpError's message, member and event")


class UnknownEventError(SignupError):
    """The club has no event with this title."""

    def __init__(self, title: str):
        """Give the parent the message, then keep the title for whoever catches it."""
        raise NotImplementedError("core: UnknownEventError's message and title")
