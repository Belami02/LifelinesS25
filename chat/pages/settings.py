import reflex as rx
from chat.auth.state import SessionState
from chat.components.mainNavbar import mainNavbar

def get_color_scheme():
    return {
        "primary": "rgb(107,99,246)",
        "background": {
            "light": "white",
            "dark": "rgb(30,30,30)",
        },
        "card": {
            "light": "white",
            "dark": "rgb(30,30,30)",  # Changed to match background in dark mode
        },
        "text": {
            "light": "rgb(0,0,0)",
            "dark": "white",
        },
        "border": {
            "light": "rgb(229,231,235)",
            "dark": "rgb(55,55,55)",
        }
    }

colors = get_color_scheme()

def profile_photo_card():
    return rx.card(
        rx.vstack(
            rx.image(
                src=SessionState.profile_photo_base64,
                alt="Profile Photo",
                max_height="500px",
                width="200px",
                height="auto",
                border_radius="full",
                margin_bottom="4"
            ),
            rx.text(
                "Profile Photo",
                color=rx.color_mode_cond(
                    light=colors["text"]["light"],
                    dark=colors["text"]["dark"]
                ),
                text_align="center"
            ),
            padding="8",
            box_shadow="lg",
            border_radius="md",
            max_width="200px",
            margin="auto",
            # background=rx.color_mode_cond(
            #     light=colors["card"]["light"],
            #     dark="var(--gray-2)"
            # ),
            border_color=rx.color_mode_cond(
                light=colors["border"]["light"],
                dark=colors["border"]["dark"]
            ),
            align_items="center",
            justify_content="center",
            border_width="1px",
        )
    )

def profile_photo_upload():
    return rx.card(
        rx.vstack(
            rx.heading(
                "Update Profile Photo",
                size="4",
                text_align="center",
                margin_bottom="4",
                color=rx.color_mode_cond(
                    light=colors["text"]["light"],
                    dark=colors["text"]["dark"]
                )
            ),
            rx.upload(
                rx.vstack(
                    rx.button(
                        "Select File",
                        color=colors["primary"],
                        bg=rx.color_mode_cond(
                            light=colors["card"]["light"],
                            dark=colors["card"]["dark"]
                        ),
                        border=f"1px solid {colors['primary']}",
                        _hover={
                            "bg": colors["primary"],
                            "color": "white"
                        }
                    ),
                    rx.text(
                        "Drag and drop files here or click to select files",
                        color=rx.color_mode_cond(
                            light=colors["text"]["light"],
                            dark=colors["text"]["dark"]
                        )
                    ),
                ),
                id="upload1",
                border=f"1px dotted {colors['primary']}",
                padding="5em",
                margin_bottom="4",
            ),
            rx.hstack(
                rx.foreach(
                    rx.selected_files("upload1"),
                    lambda file: rx.text(
                        file,
                        color=rx.color_mode_cond(
                            light=colors["text"]["light"],
                            dark=colors["text"]["dark"]
                        )
                    )
                )
            ),
            rx.hstack(
                rx.button(
                    "Upload",
                    on_click=SessionState.handle_profile_photo_submit(
                        rx.upload_files(upload_id="upload1")
                    ),
                    margin_top="4",
                    color="white",
                    bg=colors["primary"],
                    _hover={"opacity": 0.8}
                ),
                rx.button(
                    "Clear",
                    on_click=rx.clear_selected_files("upload1"),
                    margin_top="4",
                    variant="outline",
                    border_color=colors["primary"],
                    color=rx.color_mode_cond(
                        light=colors["text"]["light"],
                        dark=colors["text"]["dark"]
                    ),
                    _hover={
                        "bg": colors["primary"],
                        "color": "white"
                    }
                ),
                spacing="4"
            ),
            padding="8",
            # background=rx.color_mode_cond(
            #     light=colors["card"]["light"],
            #     dark=colors["card"]["dark"]
            # ),
            box_shadow="lg",
            border_radius="md",
            max_width="600px",
            margin="auto",
            border_color=rx.color_mode_cond(
                light=colors["border"]["light"],
                dark=colors["border"]["dark"]
            ),
            border_width="1px",
        ),
        padding="8",
        border_width="1px",
        border_radius="lg",
        # border_color=rx.color_mode_cond(
        #     light=colors["border"]["light"],
        #     dark=colors["border"]["dark"]
        # ),
        background=rx.color_mode_cond(
            light=colors["card"]["light"],
            dark=colors["card"]["dark"]
        ),
        _hover={'box_shadow': 'lg'},
        max_width="850px",
        margin_bottom="1em"
    )

def settings_page() -> rx.Component:
    return rx.hstack(
        profile_photo_card(),
        profile_photo_upload(),
        spacing="8",
        align_items="start",
        padding="8",
        background=rx.color_mode_cond(
            light=colors["background"]["light"],
            dark=colors["background"]["dark"]
        ),
        min_height="100vh"
    )

def SettingsPage():
    return rx.vstack(
        mainNavbar(),
        settings_page(),
        align_items="center",
        spacing="8",
        padding="8",
        background=rx.color_mode_cond(
            light=colors["background"]["light"],
            dark=colors["background"]["dark"]
        ),
        min_height="100vh"
    )