import reflex as rx 

from chat.components.mainNavbar import mainNavbar
from chat.post.state import PostState, editFormState

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

def post_detail_page() -> rx.Component:
	is_owner = editFormState.is_owner
	edit_link = rx.link("Edit", href=f"{PostState.post_edit_url}")
	edit_link_el = rx.cond(
		is_owner,
		edit_link,
		rx.fragment("")
	)
	my_child = rx.cond(
		PostState.post, 
		rx.vstack(
			rx.hstack(
				rx.heading(PostState.post.title, size="9"),
				edit_link_el,
				align='end'
			),
			
			# rx.text("User info id ", PostState.post.userinfo_id),
			# rx.text("User info: ", PostState.post.userinfo.to_string()),
			# rx.text("User: ", PostState.post.userinfo.user.to_string()),
			# rx.text(PostState.post.publish_date),
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
				# width='850px'
			),
			data_list(),
			spacing="5",
			align="center",
			min_height="85vh"
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
		min_height="100vh"
	)