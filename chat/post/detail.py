import reflex as rx 

from chat.components.mainNavbar import mainNavbar
from chat.post.state import PostState, editFormState
from . import state

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
			margin_bottom='1em'
			# width='850px'
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
            padding_x="1em",
            padding_y="1.5em",
            bg=rx.color("accent", 3),
            align="start",
            height="650px",
            width="16em",
        )
    )

def post_detail_page() -> rx.Component:
    is_owner = editFormState.is_owner
    is_member = PostState.is_member
    edit_link = rx.link("Edit", href=f"{PostState.post_edit_url}")
    join_button = rx.button("Join", on_click=lambda: PostState.join_post(PostState.post.id))
    edit_link_el = rx.cond(
        is_owner,
        edit_link,
        rx.fragment("")
    )
    join_button_el = rx.cond(
        ~is_owner & ~is_member,
        join_button,
        rx.fragment("")
    )
    
    content = rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(PostState.post.title, size="9"),
                edit_link_el,
                join_button_el,
                align='end'
            ),
            rx.card(
                rx.text(
                    PostState.post.content,
                    white_space='pre-wrap'
                ),
                padding='1em',
                border_width='1px',
                border_radius='lg',
                box_shadow='md',
                background_color="var(--gray-2)",
                _hover={'box_shadow': 'lg'},
                width='100%',
                max_width='850px',
                margin_bottom='1em',
            ),
            data_list(),
            spacing="5",
            align="center",
            min_height="85vh",
            margin_left="2.5em",
        ),
        align_items="center",
        justify="between"
    )
    
    my_child = rx.cond(
        PostState.post,
        rx.hstack(
            content,
            rx.spacer(),
            members_sidebar(),
            width="100%",
            align_items="start",
            justify="between"
        ),
        rx.text("Post Not Found"),
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