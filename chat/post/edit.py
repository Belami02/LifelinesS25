import reflex as rx 
import reflex_local_auth
from chat.post.forms import post_edit_form
from chat.post.state import editFormState
from chat.components.mainNavbar import mainNavbar

@reflex_local_auth.require_login
def post_edit_page() -> rx.Component:
    my_form = post_edit_form()
    post = editFormState.post
    is_owner = editFormState.is_owner
    my_child = rx.cond(post, 
            rx.cond(
                is_owner,
                rx.vstack(
                    rx.heading("Editing ", post.title, size="9"),
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
                ), 
                rx.text("Post Not Found"),
            )
        )
    
    return rx.vstack(
        mainNavbar(),
        my_child,
        align_items="center",
        spacing="8"
    )