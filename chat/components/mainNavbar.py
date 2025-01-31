import reflex as rx
from reflex.style import set_color_mode, color_mode
from chat.auth.state import SessionState

# Constants
LOGO_SRC = "/LogoReconnect.png"
LOGO_WIDTH = "13em"
LOGO_HEIGHT = "auto"
LOGO_BORDER_RADIUS = "25%"

# Navbar Links
NAVBAR_LINKS = [
    {"text": "Posts", "url": "/post"},
    {"text": "Map", "url": "/map"},
    {"text": "Chat", "url": "/chat"},
    {"text": "About", "url": "/about"},
]

# Navbar Buttons
NAVBAR_BUTTONS = [
    {"text": "Sign Up", "url": "/register", "variant": "outline"},
    {"text": "Log In", "url": "/login", "variant": "solid"},
]

def dark_mode_toggle() -> rx.Component:
    """Dark mode toggle component."""
    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon(tag="sun", size=20),
            value="light",
        ),
        rx.segmented_control.item(
            rx.icon(tag="moon", size=20),
            value="dark",
        ),
        on_change=set_color_mode,
        variant="classic",
        radius="large",
        value=color_mode,
    )

def navbar_link(text: str, url: str) -> rx.Component:
    """Navbar link component."""
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )

def navbar_button(text: str, url: str, variant: str) -> rx.Component:
    """Navbar button component."""
    return rx.link(
        rx.button(text, size="3", variant=variant, width="auto"), href=url
    )

def navbar_log_out(text: str, url: str, variant: str) -> rx.Component:
    """Navbar log out component."""
    return rx.link(
        rx.button(text, size="3", on_click=SessionState.perform_logout,
                variant=variant, width="auto"), href=url
    )

def user_info() -> rx.Component:
    """User info component."""
    user_info_obj = SessionState.authenticated_user_info
    username_via_user_obj = rx.cond(
        SessionState.authenticated_username,
        SessionState.authenticated_username, 
        "Account"
    )
    return rx.cond(
        user_info_obj,
        rx.text(f"{username_via_user_obj}", size="4", weight="bold", color="blue.500"),
    )

def desktop_navbar() -> rx.Component:
    """Desktop navbar component."""
    return rx.hstack(
        rx.link(
            rx.image(
                src=LOGO_SRC,
                width=LOGO_WIDTH,
                height=LOGO_HEIGHT,
                border_radius=LOGO_BORDER_RADIUS,
            ),
            href="/",  
        ),
        rx.hstack(
            rx.cond(
                SessionState.is_authenticated,
                navbar_link("Add Post", "/post/add"),
            ),
            *[navbar_link(link["text"], link["url"]) for link in NAVBAR_LINKS],
            spacing="5",
        ),
        rx.hstack(
            user_info(),
            dark_mode_toggle(),
            *[rx.cond(
                ~SessionState.is_authenticated,
                navbar_button(button["text"], button["url"], button["variant"]),
            ) for button in NAVBAR_BUTTONS],
            rx.cond(
                SessionState.is_authenticated,
                navbar_log_out("Log Out", "/", variant="solid"),
            ),
            spacing="4",
            justify="end",
            align_items="center",
        ),
        justify="between",
        align_items="center",
    )

def mobile_navbar() -> rx.Component:
    """Mobile navbar component."""
    return rx.hstack(
        rx.hstack(
            rx.link(
                rx.image(
                    src=LOGO_SRC,
                    width=LOGO_WIDTH,
                    height=LOGO_HEIGHT,
                    border_radius=LOGO_BORDER_RADIUS,
                ),
                href="/",  
            ),
            align_items="center",
        ),
        rx.hstack(
            dark_mode_toggle(),
            rx.menu.root(
                rx.menu.trigger(
                    rx.icon("menu", size=30)
                ),
                rx.menu.content(
                    *[rx.menu.item(link["text"], on_click=rx.redirect(link["url"])) for link in NAVBAR_LINKS],
                    rx.menu.separator(),
                    rx.menu.item("Log in", on_click=rx.redirect("/login")),
                    rx.menu.item("Register", on_click=rx.redirect("/register")),
                ),
                justify="end",
            ),
            justify="between",
        ),
        justify="between",
        align_items="center",
    )

def mainNavbar() -> rx.Component:
    """Main navbar component."""
    return rx.box(
        rx.desktop_only(desktop_navbar()),
        rx.mobile_and_tablet(mobile_navbar()),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
    )