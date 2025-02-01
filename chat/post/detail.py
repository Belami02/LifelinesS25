import reflex as rx 

from chat.components.mainNavbar import mainNavbar
from chat.post.state import PostState, editFormState
from . import state

from chat.auth.state import SessionState
from chat.pages.map import map
import base64

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

def data_list() -> rx.Component:
	is_owner = editFormState.is_owner
	return rx.card(
			rx.data_list.root(
				rx.data_list.item(
					rx.data_list.label("Status"),
					rx.data_list.value(
						rx.cond(
							is_owner,
							rx.badge(
								"Authorized to Edit",
								variant="soft",
								radius="full",
							),
							rx.badge(
								"Not Authorized to Edit",
								variant="soft",
								radius="full",
							),
						)
					),
					align="center",
				),
				rx.data_list.item(
					rx.data_list.label("user_ID"),
					rx.data_list.value(PostState.post.userinfo_id),
				),
				rx.data_list.item(
					rx.data_list.label("Username"),
					rx.data_list.value(PostState.post.userinfo.user.username),
					align="center",
				),
				rx.data_list.item(
					rx.data_list.label("Email"),
					rx.data_list.value(PostState.post.userinfo.email),
				),
				rx.data_list.item(
					rx.data_list.label("Created At"),
					rx.data_list.value(PostState.post.userinfo.created_at),
				),
				
			),
			padding='1em',
			border_width='1px',
			border_radius='lg',
			box_shadow='md',
			background_color="var(--gray-2)",
			_hover={'box_shadow': 'lg'},
			# max_width='850px',
            height='237px',
			margin_bottom='1em'
			# width='850px'
		)

def photo_upload():
    return rx.card(
        rx.vstack(
            rx.heading(
                "Upload Photo",
                size="4",
                text_align="center",
                margin_bottom="4",
                padding_top="0.5em",  # Add padding to the top
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
                padding="1em",
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
                    
                    margin_top="1",
                    color="white",
                    bg=colors["primary"],
                    _hover={"opacity": 0.8}
                ),
                rx.button(
                    "Clear",
                    on_click=rx.clear_selected_files("upload1"),
                    margin_top="1",
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
                padding_bottom="0.5em",  # Add padding to the bottom
                spacing="4"
            ),
            padding="8",
            # background=rx.color_mode_cond(
            #     light=colors["card"]["light"],
            #     dark=colors["card"]["dark"]
            # ),
            box_shadow="lg",
            border_radius="md",
            max_width="400px",
            margin="auto",
            align_items="center",
            justify_content="center",
            border_color=rx.color_mode_cond(
                light=colors["border"]["light"],
                dark=colors["border"]["dark"]
            ),
            border_width="1px",
        ),
        # padding="8",
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

def member_card(member) -> rx.Component:
    """Generate a styled card for each member."""
    return rx.hstack(
        rx.icon_button(
            rx.icon("user"),
            size="3",
            radius="full",
        ),
        rx.vstack(
            rx.box(
                rx.text(
                    member.user.username,
                    size="3",
                    weight="bold",
                ),
                rx.text(
                    member.email,
                    size="2",
                    weight="medium",
                ),
                width="100%",
            ),
            spacing="0",
            justify="start",
            width="100%",
        ),
        padding_x="0.5rem",
        padding_y="0.75rem",
        align="center",
        width="100%",
        style={
            "_hover": {
                "bg": rx.color("accent", 4),
                "color": rx.color("accent", 11),
            },
            "border-radius": "0.5em",
        },
    )

def members_sidebar() -> rx.Component:
    """Generate a sidebar with members list."""
    return rx.desktop_only(
        rx.vstack(
            rx.hstack(
                rx.heading(
                    "Members",
                    size="4",
                ),
                padding_x="0.5rem",
                align="center",
                width="100%",
            ),
            rx.cond(
                state.PostState.post.members,
                rx.vstack(
                    rx.foreach(
                        state.PostState.post.members,
                        lambda member: member_card(member)
                    ),
                    width="100%",
                    spacing="1",
                ),
                rx.text(
                    "No members yet",
                    size="2",
                    weight="medium",
                    padding="4",
                ),
            ),
            spacing="5",
            margin_top="3em",
            padding_x="1em",
            padding_y="1.5em",
            bg=rx.color("accent", 3),
            align="start",
            height="650px",
            width="22em",
        )
    )

def image_card(image_data: dict, title: str) -> rx.Component:
    """Generate a card for each image in the gallery."""
    try:
        # Now we expect a dictionary with the necessary data
        image_url = f"data:image/png;base64,{base64.b64encode(image_data['image_data']).decode('utf-8')}"
        return rx.card(
            rx.vstack(
                rx.image(
                    src=image_url,
                    height="200px",
                    width="100%",
                    object_fit="cover",
                    border_radius="md",
                ),
                rx.text(
                    f"Uploaded: {image_data['created_at']}",
                    size="sm",
                    color="gray.500"
                ),
                rx.button(
                    "Delete",
                    on_click=PostState.delete_image(image_data['id']),
                    size="sm",
                    color_scheme="red",
                    variant="ghost"
                ),
                padding="2",
                spacing="2",
            ),
            height="300px",
            width="100%",
            _hover={"transform": "scale(1.02)", "transition": "transform 0.2s"},
        )
    except Exception as e:
        return rx.card(
            rx.text("Error loading image", color="red.500"),
            height="300px",
            width="100%",
        )

def community_gallery() -> rx.Component:
    """Generate a grid of community images."""
    return rx.cond(
        PostState.post,
        rx.card(
            rx.vstack(
                rx.heading("Community Gallery", size="5", margin_bottom="9"),
                rx.grid(
                    rx.foreach(
                        PostState.post_images,
                        lambda image: image_card(image, "Image Title")  # Replace "Image Title" with actual title if available
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
            ),
            margin_top="3em",
            margin_left="1em",
            padding="6",
            height="620px",  # Match the height of members_sidebar
            width="25em",    # Appropriate width for 2-column grid
            overflow_y="auto",  # Enable scrolling for many images
            align_items='center'
        ),
        rx.text("No images available.")
    )

def sample_image_card(image_url: str, title: str) -> rx.Component:
    """Generate a card for each sample image in the gallery."""
    return rx.card(
        rx.image(
            src=image_url,
            height="200px",
            width="100%",
            object_fit="cover",
        ),
        rx.text(title),
        height="250px",
        width="100%",
        _hover={"transform": "scale(1.02)", "transition": "transform 0.2s"},
    )

def sample_community_gallery() -> rx.Component:
    """Generate a grid of sample community images."""
    # Sample data - replace with actual image data from your backend
    sample_images = [
        {"url": "/MissingSon.png", "title": "Find Omar"},
        {"url": "/yilmaz_family.png", "title": "Missing Father"},
        {"url": "/Sarah.png", "title": "Sarah"},
        {"url": "/MaxDog.png", "title": "Max Dog"},
    ]
    
    return rx.card(
        rx.vstack(
            rx.heading("Community Gallery", size="4", margin_bottom="4"),
            rx.grid(
                rx.foreach(
                    sample_images,
                    lambda image: sample_image_card(image["url"], image["title"])
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),
        ),
        margin_top="3em",
        margin_left="1em",
        padding="6",
        height="620px",  # Match the height of members_sidebar
        width="24em",    # Appropriate width for 2-column grid
        overflow_y="auto",  # Enable scrolling for many images
        align_items='center'
    )

def post_detail_page() -> rx.Component:
    is_owner = editFormState.is_owner
    is_member = PostState.is_member
    edit_link = rx.link("Edit", href=f"{PostState.post_edit_url}")
    delete_link = rx.link("Delete", on_click=lambda: PostState.delete_post(PostState.post.id), color_scheme="red")
    join_button = rx.button("Join", on_click=lambda: PostState.join_post(PostState.post.id), color_scheme="green")
    leave_button = rx.button("Leave", on_click=lambda: PostState.leave_post(PostState.post.id), color_scheme="red")
    edit_link_el = rx.cond(
        is_owner,
        edit_link,
        rx.fragment("")
    )
    delete_link_el = rx.cond(
        is_owner,
        delete_link,
        rx.fragment("")
    )
    join_button_el = rx.cond(
        ~is_member,
        join_button,
        rx.fragment("")
    )
    leave_button_el = rx.cond(
        is_member,
        leave_button,
        rx.fragment("")
    )
    
    content = rx.cond(
        PostState.post,
        rx.box(
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.heading(PostState.post.title, size="7"),
                        join_button_el,
                        leave_button_el,
                        edit_link_el,
                        delete_link_el,
                        align='end'
                    ),
                    rx.card(
                        rx.text(
                            PostState.post.content,
                            white_space='pre-wrap'
                        ),
                        # padding='0.5em',
                        border_width='1px',
                        border_radius='lg',
                        box_shadow='md',
                        background_color="var(--gray-2)",
                        _hover={'box_shadow': 'lg'},
                        width='100%',
                        max_width='780px',
                        # margin_bottom='1em',
                    ),
                    align_items="center",
                    justify="between"
                ),
                map(),
                rx.hstack(
                    data_list(),
                    rx.spacer(),
                    photo_upload(),
                    align="center",
                    #align_items="start",
                    justify="center",
                    spacing="3",
                ),
                spacing="3",
                align="center",
                min_height="85vh",
            ),
            align_items="center",
            justify="between"
        )
    )
    
    my_child = rx.hstack(
        # community_gallery(),
        sample_community_gallery(),
        rx.spacer(),
        content,
        rx.spacer(),
        members_sidebar(),
        width="100%",
        align_items="start",
        justify="between"
    )

    return rx.vstack(
        mainNavbar(),
        my_child,
        align_items="center",
        spacing="8",
        padding="8",
        background_color="gray.100",
        min_height="100vh",
        width="100%",
    )