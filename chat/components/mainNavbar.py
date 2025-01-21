import reflex as rx
import reflex as rx
from reflex.style import set_color_mode, color_mode


def dark_mode_toggle() -> rx.Component:
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
    return rx.link(
        rx.text(text, size="4", weight="medium"), href=url
    )

def navbar_button(text: str, url: str, variant: str) -> rx.Component:
    return rx.link(
        rx.button(text, size="3", variant=variant, width="auto"), href = url
    )

def mainNavbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.link(
                    rx.image(
                        src="/LogoReconnect.png",
                        width="13em",
                        height="auto",
                        border_radius="25%",
                    ),
                    href="/",  
                ),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("About", "/about"),
                    spacing="5",
                ),
                rx.hstack(
                    dark_mode_toggle(),
                    # rx.button("Sign Up", size="3", variant="outline", width="auto", on_click=rx.redirect('/register')),
                    navbar_button("Sign Up", "/register", variant="outline"),
                    navbar_button("Log In", "/login", variant="solid"),
                    # rx.button(
                    #     "Sign Up",
                    #     size="3",
                    #     variant="outline",
                    # ),
                    # rx.button("Log In", size="3"),
                    spacing="4",
                    justify="end",
                    align_items="center",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.link(
                        rx.image(
                            src="/LogoReconnect.png",
                            width="13em",
                            height="auto",
                            border_radius="25%",
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
                            rx.menu.item("Home"),
                            rx.menu.item("About"),
                            rx.menu.separator(),
                            rx.menu.item("Log in"),
                            rx.menu.item("Sign up"),
                        ),
                        justify="end",
                    ),
                    justify="between",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )