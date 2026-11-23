import pytest

from club import Club
from errors import UnknownEventError


def make_club() -> Club:
    club = Club("Harbour.Space Bangkok club")
    club.add_event("Muay Thai basics", 2)
    return club


def test_core_add_event_stores_and_returns_the_event():
    club = Club("Harbour.Space Bangkok club")
    event = club.add_event("Board games", 6)
    assert event.title == "Board games"
    assert event.capacity == 6
    assert club.events["Board games"] is event


def test_core_add_event_rejects_a_capacity_of_zero():
    club = Club("Harbour.Space Bangkok club")
    with pytest.raises(ValueError):
        club.add_event("Board games", 0)


def test_core_add_event_rejects_a_title_that_is_taken():
    club = make_club()
    with pytest.raises(ValueError):
        club.add_event("Muay Thai basics", 10)


def test_core_event_finds_an_event_by_title():
    club = make_club()
    assert club.event("Muay Thai basics").capacity == 2


def test_core_event_raises_unknown_event_error():
    club = make_club()
    with pytest.raises(UnknownEventError):
        club.event("Chess night")


def test_core_handle_join_gives_a_seat_then_a_waitlist_place():
    club = make_club()
    assert club.handle("join, Muay Thai basics, Nino") == "Nino has a seat at Muay Thai basics."
    club.handle("join, Muay Thai basics, Aung")
    assert club.handle("join, Muay Thai basics, Tashi") == "Tashi is on the waitlist for Muay Thai basics."


def test_core_handle_leave_says_who_gets_the_seat():
    club = make_club()
    for name in ["Nino", "Aung", "Tashi"]:
        club.handle(f"join, Muay Thai basics, {name}")
    assert club.handle("leave, Muay Thai basics, Nino") == "Nino left Muay Thai basics. Tashi gets the seat."
    assert club.handle("leave, Muay Thai basics, Aung") == "Aung left Muay Thai basics."


def test_core_handle_says_sorry_for_a_sign_up_problem():
    club = make_club()
    club.handle("join, Muay Thai basics, Nino")
    assert club.handle("join, Muay Thai basics, Nino") == "Sorry, Nino is already signed up for Muay Thai basics."


def test_core_handle_says_sorry_for_a_line_it_does_not_understand():
    club = make_club()
    assert club.handle("hello") == "Sorry, I don't understand 'hello'."


def test_core_attendance_counts_seats_over_all_events():
    club = make_club()
    club.add_event("Board games", 6)
    club.events["Muay Thai basics"].sign_up("Nino")
    club.events["Muay Thai basics"].sign_up("Aung")
    club.events["Board games"].sign_up("Nino")
    assert club.attendance() == {"Nino": 2, "Aung": 1}
