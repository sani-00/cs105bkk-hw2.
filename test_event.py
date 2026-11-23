import pytest

from errors import AlreadySignedUpError, NotSignedUpError
from event import Event


def test_core_sign_up_gives_seats_then_waitlist_places():
    event = Event("Muay Thai basics", 2)
    assert event.sign_up("Nino") == "seat"
    assert event.sign_up("Aung") == "seat"
    assert event.sign_up("Tashi") == "waitlist"
    assert event.seats == ["Nino", "Aung"]
    assert event.waitlist == ["Tashi"]


def test_core_sign_up_twice_raises():
    event = Event("Muay Thai basics", 2)
    event.sign_up("Nino")
    with pytest.raises(AlreadySignedUpError):
        event.sign_up("Nino")


def test_core_cancel_a_seat_moves_the_first_waiting_member_up():
    event = Event("Muay Thai basics", 1)
    event.sign_up("Nino")
    event.sign_up("Aung")
    event.sign_up("Tashi")
    assert event.cancel("Nino") == "Aung"
    assert event.seats == ["Aung"]
    assert event.waitlist == ["Tashi"]


def test_core_cancel_with_nobody_waiting_returns_none():
    event = Event("Board games", 4)
    event.sign_up("Ploy")
    assert event.cancel("Ploy") is None
    assert event.seats == []


def test_core_cancel_someone_not_signed_up_raises():
    event = Event("Board games", 4)
    with pytest.raises(NotSignedUpError):
        event.cancel("Ploy")


def test_core_place_counts_the_waitlist_from_one():
    event = Event("Muay Thai basics", 1)
    event.sign_up("Nino")
    event.sign_up("Aung")
    event.sign_up("Tashi")
    assert event.place("Nino") == 0
    assert event.place("Aung") == 1
    assert event.place("Tashi") == 2


def test_core_place_of_someone_not_signed_up_raises():
    event = Event("Muay Thai basics", 1)
    with pytest.raises(NotSignedUpError):
        event.place("Ploy")
