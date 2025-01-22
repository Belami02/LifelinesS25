import reflex as rx
import reflex_local_auth
from chat.auth.models import PostModel
from chat.post.state import PostState
from . import state
from chat.components.mainNavbar import mainNavbar

def post_detail_link(child: rx.Component, post: PostModel):
    if post is None:
        return rx.fragment(child)
    post_id = post.id
    if post_id is None:
        return rx.fragment(child)
    root_path = "/post"
    post_detail_url = f"{root_path}/{post_id}"
    return rx.link(
        child,
        href=post_detail_url
    )

def button_link(text: str, url: str, size: str, color_scheme: str) -> rx.Component:
    return rx.link(
        rx.button(text, size=size, color_scheme=color_scheme), href=url
    )

def post_item(post: PostModel):
    return rx.card(
        rx.vstack(
            post_detail_link(
                rx.heading(post.title, size="4"),  # Changed size to a valid value
                post
            ),
            rx.text(f"by {post.userinfo.user.username}", font_size="sm", color="gray.500"),
            rx.text(post.content[:100] + "...", white_space='pre-wrap', font_size="sm"),
            button_link("Read More", url=f"/post/{post.id}", size="2", color_scheme="teal"),
            spacing="3",
            align="start"
        ),
        padding='1em',
        border_width='1px',
        border_radius='lg',
        box_shadow='md',
        background_color="var(--gray-2)",
        _hover={'box_shadow': 'lg'},
        width='100%',
        # max_width='850px',
        margin_bottom='1em',
        # width='850px'
    )

def post_page() -> rx.Component:
    my_child = rx.vstack(
        rx.heading("Posts", size="5"),
        rx.link(
            rx.button("New Post", color_scheme="teal", size="2"),  # Changed size to a valid value
            href="/post/add"
        ),
        rx.foreach(state.PostState.posts, post_item),
        spacing="5",
        align="center",
        min_height="85vh",
    )
    return rx.vstack(
        mainNavbar(),
        my_child,
        align_items="center",
        spacing="8"
    )