from errors import AlreadySignedUpError, SignupError, UnknownEventError


def test_core_already_signed_up_error_message():
    error = AlreadySignedUpError("Nino", "Muay Thai basics")
    assert str(error) == "Nino is already signed up for Muay Thai basics"


def test_core_already_signed_up_error_keeps_member_and_event():
    error = AlreadySignedUpError("Nino", "Muay Thai basics")
    assert error.member == "Nino"
    assert error.event == "Muay Thai basics"
    assert isinstance(error, SignupError)


def test_core_unknown_event_error_message_and_title():
    error = UnknownEventError("Chess night")
    assert str(error) == "there is no event called 'Chess night'"
    assert error.title == "Chess night"
    assert isinstance(error, SignupError)
