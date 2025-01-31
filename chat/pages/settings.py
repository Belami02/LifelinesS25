import reflex as rx
from chat.auth.state import SessionState
from chat.components.mainNavbar import mainNavbar

color = "rgb(107,99,246)"
dark_background = "rgb(30,30,30)"
light_text = "white"

def profile_photo_card():
    return rx.card(
        rx.vstack(
            rx.image(
                src=rx.cond(
                    SessionState.authenticated_user_info.profile_photo,
                    rx.get_upload_url(SessionState.authenticated_user_info.profile_photo),
                    "/BlankProfile.png"
                ),
                alt="Profile Photo",
                width="150px",
                height="150px",
                border_radius="full",
                margin_bottom="4"
            ),
            rx.text("Current Profile Photo", color=light_text, text_align="center"),
            padding="8",
            background_color=dark_background,
            box_shadow="lg",
            border_radius="md",
            max_width="200px",
            margin="auto"
        ),
        padding="8",
        border_width="1px",
        border_radius="lg",
        box_shadow="md",
        background_color=dark_background,
        _hover={'box_shadow': 'lg'},
        max_width="250px",
        margin_bottom="1em"
    )

def profile_photo_upload():
    return rx.card(
        rx.vstack(
            rx.heading("Update Profile Photo", size="4", text_align="center", margin_bottom="4", color=light_text),
            rx.upload(
                rx.vstack(
                    rx.button(
                        "Select File",
                        color=color,
                        bg=light_text,
                        border=f"1px solid {color}",
                    ),
                    rx.text(
                        "Drag and drop files here or click to select files",
                        color=light_text
                    ),
                ),
                id="upload1",
                border=f"1px dotted {color}",
                padding="5em",
                margin_bottom="4",
            ),
            rx.hstack(
                rx.foreach(
                    rx.selected_files("upload1"), lambda file: rx.text(file, color=light_text)
                )
            ),
            rx.button(
                "Upload",
                on_click=SessionState.handle_profile_photo_submit(
                    rx.upload_files(upload_id="upload1")
                ),
                margin_top="4",
                color=light_text,
                bg=color,
            ),
            rx.button(
                "Clear",
                on_click=rx.clear_selected_files("upload1"),
                margin_top="4",
                color=light_text,
                bg=color,
            ),
            padding="8",
            background_color=dark_background,
            box_shadow="lg",
            border_radius="md",
            max_width="600px",
            margin="auto"
        ),
        padding="8",
        border_width="1px",
        border_radius="lg",
        box_shadow="md",
        background_color=dark_background,
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
        background_color=dark_background,
        min_height="100vh"
    )

def SettingsPage():
    return rx.vstack(
        mainNavbar(),
        settings_page(),
        align_items="center",
        spacing="8",
        padding="8",
        background_color=dark_background,
        min_height="100vh"
    )