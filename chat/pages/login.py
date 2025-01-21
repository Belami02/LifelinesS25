import reflex as rx
from chat.components.mainNavbar import mainNavbar
from reflex_local_auth.pages.login import LoginState, login_error

def login() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.center(
                # rx.image(
                #     src="/logo.jpg",
                #     width="2.5em",
                #     height="auto",
                #     border_radius="25%",
                # ),
                rx.heading(
                    "Sign in to your account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                
                direction="column",
                spacing="5",
                width="100%",
            ),
            login_error(),
            rx.vstack(
                rx.text(
                    "Username",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your username",
                    id="username",
                    name="username",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Password",
                        size="3",
                        weight="medium",
                    ),
                    # rx.link(
                    #     "Forgot password?",
                    #     href="#",
                    #     size="3",
                    # ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your password",
                    type="password",
                    size="3",
                    id="password",
                    name="password",
                    width="100%",
                ),
                spacing="2",
                width="100%",
            ),
            rx.button("Sign in", size="3", width="100%"),
            rx.center(
                rx.text("New here?", size="3"),
                rx.link("Sign up", href="/register", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
            ),
            spacing="6",
            width="100%",
        ),
        on_submit=LoginState.on_submit,
    )

def LoginPage():
    return rx.vstack(
        mainNavbar(),
        rx.cond(
            LoginState.is_hydrated,
            rx.card(
                login(),
                size="4",
                max_width="28em",
                width="100%",
            ),
        ),
        #flex="1",  
        #width="100%",
        align_items="center",
        #justify_content="center",
        #background_color="gray.100",
        spacing="8"
    )