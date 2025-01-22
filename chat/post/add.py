import reflex as rx 
import reflex_local_auth
from . import forms
from chat.components.mainNavbar import mainNavbar

@reflex_local_auth.require_login
def post_add_page() -> rx.Component:
    my_form = forms.post_add_form()
    my_child = rx.vstack(
        rx.heading("New Post", size="9"),
        rx.desktop_only(
            rx.box(
                my_form,
                width='50vw'
            )
        ),
        rx.tablet_only(
            rx.box(
                my_form,
                width='75vw'
            )
        ),
        rx.mobile_only(
            rx.box(
                my_form,
                width='95vw'
            )
        ),
        spacing="5",
        align="center",
        min_height="95vh",
    )
    return rx.vstack(
        mainNavbar(),
        my_child,
        align_items="center",
        spacing="8"
    )