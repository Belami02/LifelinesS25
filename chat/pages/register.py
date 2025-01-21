import reflex as rx
from chat.components.mainNavbar import mainNavbar
from chat.auth.state import MyRegisterState
from chat.auth.forms import register_error
from reflex_local_auth.pages.registration import RegistrationState

def signup() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.center(
                rx.heading(
                    "Create an account",
                    size="6",
                    as_="h2",
                    text_align="center",
                    width="100%",
                ),
                direction="column",
                spacing="5",
                width="100%",
            ),
            register_error(),
            rx.vstack(
                rx.text(
                    "Email address",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="Enter your Email",
                    type="email",
                    size="3",
                    id="email",
                    name="email",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
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
                    size="3",
                    id="username",
                    name="username",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Password",
                    size="3",
                    weight="medium",
                    text_align="left",
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
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.vstack(
                rx.text(
                    "Confirm Password",
                    size="3",
                    weight="medium",
                    text_align="left",
                    width="100%",
                ),
                rx.input(
                    placeholder="Confirm your password",
                    type="password",
                    size="3",
                    id="confirm password",
                    name="confirm password",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            # rx.box(
            #     rx.checkbox(
            #         "Agree to Terms and Conditions",
            #         default_checked=True,
            #         spacing="2",
            #     ),
            #     width="100%",
            # ),
            rx.button("Register", size="3", width="100%"),
            rx.center(
                rx.text("Already registered?", size="3"),
                rx.link("Sign in", href="/login", size="3"),
                opacity="0.8",
                spacing="2",
                direction="row",
            ),
            spacing="6",
            width="100%",
        ),
        on_submit=MyRegisterState.handle_registration_email,
    )

def RegistrationPage():
    return rx.vstack(
        mainNavbar(),
        # signup(),
        rx.cond(
            RegistrationState.success,
            rx.center(
                rx.vstack("Registration successful!"),
            ),
            rx.card(
                signup(),
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