"""The main Chat app."""

import reflex as rx
import reflex_chakra as rc

from chat.components import chat, navbar
from chat.pages.register import RegistrationPage
from chat.pages.login import LoginPage

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
app.add_page(about)
app.add_page(RegistrationPage, route="/register", title="Sign Up")  
app.add_page(LoginPage, route="/login", title="Sign In")  
