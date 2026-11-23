# HW2: club events with limited seats

**Worth 10% of your grade.** HW2 covers Sessions 4 to 6. You will build the sign-up part of a student club's app: events with a limited number of seats, a waitlist for when an event is full, the club's own exceptions, and a small chat bot that answers members.

**Released:** Tue 17 Nov. **Due:** Tue 24 Nov, 23:59. You have one week.

**Late work:** each day late costs 10% of the mark. You can hand in up to 3 days late; after that, HW2 is not accepted.

## 1. Get your own copy

1. On this repository's GitHub page, click **Use this template** → **Create a new repository**.
2. Owner: your own account. Name: `cs105bkk-hw2`. Click **Create repository**.
3. Clone **your** new repository and open the folder in VS Code:

   ```
   git clone https://github.com/<your-username>/cs105bkk-hw2.git
   ```

## 2. Set up and see red

From the repository folder:

```
python -m venv .venv
```

Activate it. On macOS: `source .venv/bin/activate`. On Windows: `.venv\Scripts\activate`.

```
python -m pip install pytest
python -m pytest
```

Every test fails with `NotImplementedError`. That is the starting point. Each error message names the part you still have to write.

## 3. The story

Your student club runs events with a limited number of seats: a Muay Thai class, a board games evening, a hackathon night. Members sign up for a seat. When an event is full, they go on a waitlist, first come first served. When someone with a seat cancels, the first person on the waitlist gets that seat.

The code is split into three modules, as in Session 5. Each one has one job:

| Module | Its job |
|---|---|
| `errors.py` | The club's own exceptions. |
| `event.py` | One `Event`: its seats and its waitlist. |
| `club.py` | The `Club`: finds events by title, and answers chat commands. It imports the other two. |

Every function whose body is `raise NotImplementedError(...)` is yours to write. Parts marked **Provided** are already done; read them, but don't change them. Don't change any names or signatures either, because the tests use them.

## 4. Write the code

Work through the parts in this order. Run `python -m pytest` after each one.

### `errors.py`: the club's own exceptions

All the club's exceptions inherit from `SignupError`, so code that wants to handle any sign-up problem can catch `SignupError` alone. `SignupError` and `NotSignedUpError` are provided. Read `NotSignedUpError` first: the two below follow the same pattern.

1. **`AlreadySignedUpError.__init__(self, member, event)`** passes its message to the parent class with `super().__init__(...)`, then keeps `member` and `event` as attributes, so whoever catches the error can use them.

   ```python
   >>> error = AlreadySignedUpError("Nino", "Muay Thai basics")
   >>> str(error)
   'Nino is already signed up for Muay Thai basics'
   >>> error.member, error.event
   ('Nino', 'Muay Thai basics')
   ```

2. **`UnknownEventError.__init__(self, title)`** does the same with one attribute, `title`. The message puts the title in quotes; `{title!r}` in an f-string does that for you.

   ```python
   >>> str(UnknownEventError("Chess night"))
   "there is no event called 'Chess night'"
   ```

### `event.py`: one event

`Event` is a dataclass (Session 4) with a `title`, a `capacity`, and two lists of member names: `seats` and `waitlist`. Each event gets its own two new lists, because the fields use `field(default_factory=list)`. `seats_left()` is provided.

3. **`sign_up(self, member)`**:
   - if the member is already in `seats` or in `waitlist`, it raises `AlreadySignedUpError` and changes nothing;
   - if a seat is left, the member goes to the end of `seats`, and it returns `"seat"`;
   - otherwise the member goes to the end of `waitlist`, and it returns `"waitlist"`.

   ```python
   >>> muay_thai = Event("Muay Thai basics", 2)
   >>> muay_thai.sign_up("Nino"), muay_thai.sign_up("Aung"), muay_thai.sign_up("Tashi")
   ('seat', 'seat', 'waitlist')
   >>> muay_thai.seats, muay_thai.waitlist
   (['Nino', 'Aung'], ['Tashi'])
   ```

4. **`cancel(self, member)`** takes the member off the event:
   - a member on the waitlist is removed from it, nobody moves, and it returns `None`;
   - a member with a seat gives it up. If anyone is waiting, the **first** member on the waitlist moves to the end of `seats`, and it returns that member's name. If nobody is waiting, it returns `None`;
   - a member on neither list makes it raise `NotSignedUpError` and change nothing.

   ```python
   >>> muay_thai.cancel("Nino")
   'Tashi'
   >>> muay_thai.seats, muay_thai.waitlist
   (['Aung', 'Tashi'], [])
   ```

5. **`place(self, member)`** returns `0` for a member with a seat, `1` for the first member on the waitlist, `2` for the second, and so on. For a member on neither list, it raises `NotSignedUpError`.

   Try it the EAFP way from Session 6: `self.waitlist.index(member)` raises `ValueError` when the member isn't there. Catch that `ValueError`, and raise the club's own `NotSignedUpError` instead.

   ```python
   >>> board_games = Event("Board games", 1)
   >>> for name in ["Ploy", "Nino", "Aung"]:
   ...     board_games.sign_up(name)
   >>> board_games.place("Ploy"), board_games.place("Aung")
   (0, 2)
   ```

### `club.py`: the club and its chat bot

A `Club` keeps its events in a dict, `self.events`, which maps each title to its `Event`. The club finds events; each `Event` looks after its own seats. Keep it that way: `Club` never changes `seats` or `waitlist` itself.

6. **`add_event(self, title, capacity)`** makes a new `Event`, stores it under its title and returns it. It raises `ValueError`, and stores nothing, if the capacity is less than 1 or if the club already has an event with that title.

   ```python
   >>> club = Club("Harbour.Space Bangkok club")
   >>> club.add_event("Muay Thai basics", 2)
   Event(title='Muay Thai basics', capacity=2, seats=[], waitlist=[])
   >>> club.add_event("Board games", 0)
   ValueError: capacity must be at least 1, got 0
   ```

7. **`event(self, title)`** returns the event with that title. Look it up with `self.events[title]` inside `try`, and turn the `KeyError` into an `UnknownEventError`, so the rest of the program only has to know the club's own exceptions.

   ```python
   >>> club.event("Chess night")
   UnknownEventError: there is no event called 'Chess night'
   ```

8. **`handle(self, line)`** answers one command from the club's chat and always returns one sentence. A command has three parts split by commas: the command (`join` or `leave`), the event title, and the member's name. Ignore spaces around each part, and capitals in the command word.

   | The member types | `handle` returns |
   |---|---|
   | `join, Muay Thai basics, Nino` (a seat is left) | `Nino has a seat at Muay Thai basics.` |
   | `join, Muay Thai basics, Tashi` (the event is full) | `Tashi is on the waitlist for Muay Thai basics.` |
   | `leave, Muay Thai basics, Nino` (nobody moves up) | `Nino left Muay Thai basics.` |
   | `leave, Muay Thai basics, Nino` (Tashi was waiting) | `Nino left Muay Thai basics. Tashi gets the seat.` |
   | a command that raises a `SignupError` | `Sorry, ` + the error's message + `.`, for example `Sorry, Nino is already signed up for Muay Thai basics.` |
   | anything that is not three parts with `join` or `leave` first, such as `hello` | `Sorry, I don't understand 'hello'.` |

   Catch `SignupError` and nothing else. A bare `except:` or `except Exception:` would also hide real bugs, which is the Session 6 rule: never swallow errors you didn't expect.

9. **`attendance(self)`** returns a dict that maps each member to the number of events where they have a **seat**. The waitlist doesn't count, and a club where nobody has a seat gives `{}`.

   `Counter`, from the standard library's `collections` module (Session 5), does most of this for you. Import it at the top of `club.py`. A plain dict works too.

   ```python
   >>> club.event("Muay Thai basics").sign_up("Nino")
   'seat'
   >>> club.add_event("Board games", 6).sign_up("Nino")
   'seat'
   >>> club.attendance()
   {'Nino': 2}
   ```

When you are done, run `python club.py`. Its provided `if __name__ == "__main__":` block plays a short chat with the bot. `import club` doesn't run it: that is what the `if` is for.

Run `python -m pytest` until every test passes. The tests you see are not all the tests: grading also runs more tests on cases these rules describe, such as the limits, the empty cases, and an error that `handle` must not hide. Read each rule above carefully, and try those cases yourself.

## 5. Fill in NOTES.md

Answer the three questions in `NOTES.md`. A few honest sentences each are enough.

## 6. Commit, push, and check Actions

Commit as you go, not only at the end. When you are done:

```
git add errors.py event.py club.py NOTES.md
git commit -m "Finish HW2"
git push
```

On your repository's GitHub page, open the **Actions** tab. GitHub runs the tests on every push. A green tick means the visible tests passed there too. That result is feedback for you, not your grade. Don't change the test files or the workflow file: changes to them are flagged.

## 7. Upload to Google Classroom

Upload a `.zip` of your repository and paste its link in the HW2 assignment on Google Classroom. Your GitHub repository at the deadline is the copy that is graded. *(Proposal O13)*
