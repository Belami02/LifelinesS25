import reflex as rx

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
                rx.hstack(
                    # rx.image(
                    #     src="/logo.jpg",
                    #     width="2.25em",
                    #     height="auto",
                    #     border_radius="25%",
                    # ),
                    rx.heading(
                        "Welcome!", size="7", weight="bold"
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link("About", "/about"),
                    spacing="5",
                ),
                rx.hstack(
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
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    # rx.image(
                    #     src="/logo.jpg",
                    #     width="2em",
                    #     height="auto",
                    #     border_radius="25%",
                    # ),
                    rx.heading(
                        "Welcome!", size="6", weight="bold"
                    ),
                    align_items="center",
                ),
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