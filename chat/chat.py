"""The main Chat app."""

import reflex as rx
import reflex_chakra as rc
import reflex_local_auth # s00n I'll add this
from chat.auth.models import UserInfo

from chat.components import chat, navbar
from chat.pages.register import RegistrationPage
from chat.pages.login import LoginPage
from chat.auth.state import SessionState

def index() -> rx.Component:
    """The main app."""
    return rc.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )

@reflex_local_auth.require_login
def about():
    return rx.text("About Page")

# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)
app.add_page(index)
app.add_page(about, route="/about", title = "About", on_load=SessionState.on_load)
app.add_page(RegistrationPage, route="/register", title="Sign Up")  
app.add_page(LoginPage, route="/login", title="Sign In")  