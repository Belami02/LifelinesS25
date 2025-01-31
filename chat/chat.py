"""The main Chat app."""

import reflex as rx
import reflex_chakra as rc
import reflex_local_auth # s00n I'll add this
from chat.auth.models import UserInfo

from chat.components import chat, navbar
from chat.components.mainNavbar import mainNavbar
from chat.pages.register import RegistrationPage
from chat.pages.login import LoginPage
from chat.pages.about import AboutPage
from chat.auth.state import SessionState
from chat.pages.map import MapPage
from chat.post.add import post_add_page
from chat.post.detail import post_detail_page
from chat.post.edit import post_edit_page
from chat.post.post import post_page
from chat.post.state import PostState
from chat.pages.settings import SettingsPage

def ChatPage() -> rx.Component:
    """The main app."""
    return rc.vstack(
        mainNavbar(),
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )

# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)

app.add_page(
    post_page, 
    route="/",
    on_load=PostState.load_all_posts,
    title="All Posts",
)
app.add_page(ChatPage, route="/chat", title="Chat")
app.add_page(AboutPage, route="/about", title = "About")
app.add_page(RegistrationPage, route="/register", title="Sign Up")  
app.add_page(LoginPage, route="/login", title="Sign In")  
app.add_page(MapPage, route="/map", title="Map")
app.add_page(
    post_add_page, 
    route="/post/add",
    title="Add Post",
)

app.add_page(
    post_detail_page, 
    route="/post/[post_id]",
    on_load=PostState.get_post_detail,
    title="Post",
)

app.add_page(
    post_edit_page, 
    route="/post/[post_id]/edit",
    on_load=PostState.get_post_detail,
    title="Edit Post",
)

app.add_page(
    post_page, 
    route="/post",
    on_load=PostState.load_all_posts,
    title="All Posts",
)

app.add_page(
    SettingsPage,
    route="/settings",
    title="Settings",
    on_load=SessionState.on_load
)