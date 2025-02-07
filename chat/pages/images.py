''' TESTING PURPOSES '''

import reflex as rx
from chat.components.mainNavbar import mainNavbar
from chat.post.state import PostState
from chat.auth.models import ImageModel
import base64

def image_card(image: ImageModel) -> rx.Component:
    """Generate a card for each image in the gallery."""
    try:
        # image_url = f"data:image/png;base64,{base64.b64encode(image.image_data).decode('utf-8')}"
        return rx.card(
            rx.vstack(
                # rx.image(
                #     src=image_url,
                #     height="200px",
                #     width="100%",
                #     object_fit="cover",
                #     border_radius="md",
                # ),
                rx.text(
                    f"Post {image.post_id}",
                    size="4",
                    color="gray.500",
                    text_align="center",
                ),
                rx.text(
                    f"Post {image.image_data}",
                    size="4",
                    color="gray.500",
                    text_align="center",
                ),
                padding="2",
                spacing="2",
            ),
            height="250px",
            width="100%",
            _hover={"transform": "scale(1.02)", "transition": "transform 0.2s"},
        )
    except Exception as e:
        print(f"Error creating image card: {e}")
        return rx.card(
            rx.text("Error loading image", color="red.500"),
            height="250px",
            width="100%",
        )

def images_gallery() -> rx.Component:
    """Generate a grid of all images in the database."""
    # PostState.load_all_images()
    return rx.card(
        rx.vstack(
            rx.heading("Images Gallery", size="4", margin_bottom="4"),
            rx.grid(
                rx.foreach(
                    PostState.post_images,
                    lambda image: image_card(image)  # Pass the entire image object
                ),
                columns="3",
                spacing="4",
                width="100%",
            ),
        ),
        margin_top="3em",
        margin_left="1em",
        padding="6",
        height="auto",
        width="100%",
        overflow_y="auto",
        align_items='center'
    )

def ImagesPage():
    return rx.vstack(
        mainNavbar(),
        images_gallery(),
        align_items="center",
        spacing="8",
        padding="8",
        background_color="gray.100",
        min_height="100vh"
    )