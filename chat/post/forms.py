import reflex as rx
from chat.post.state import addPostFormState, editFormState

def post_add_form() -> rx.Component:
    return rx.form(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        name="title",
                        placeholder="Title",
                        required=True,
                        type='text',
                        width='100%',
                    ),
                    width='100%'
                ),
                rx.text_area(
                    name='content',
                    placeholder="Your message",
                    required=True,
                    height='50vh',
                    width='100%',
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=addPostFormState.handle_submit,
            reset_on_submit=True,
    )

def post_edit_form() -> rx.Component:
    post = editFormState.post
    title = post.title
    publish_active = post.publish_active
    post_content = editFormState.post_content
    return rx.form(
            rx.box(
                rx.input(
                    type='hidden',
                    name='post_id',
                    value=post.id
                ),
                display='none'
            ), 
            rx.vstack(
                rx.hstack(
                    rx.input(
                        default_value=title,
                        name="title",
                        placeholder="Title",
                        required=True,
                        type='text',
                        width='100%',
                    ),
                    width='100%'
                ),
                rx.text_area(
                    value = post_content,
                    on_change = editFormState.set_post_content,
                    name='content',
                    placeholder="Your message",
                    required=True,
                    height='50vh',
                    width='100%',
                ),
                rx.flex(
                    rx.switch(
                        default_checked=editFormState.post_publish_active,
                        on_change=editFormState.set_post_publish_active,
                        name='publish_active',          
                    ),
                    rx.text("Publish Active"),
                    spacing="2",
                ),
                rx.cond(
                    editFormState.post_publish_active,
                    rx.box(
                        rx.hstack(
                            rx.input(
                                default_value=editFormState.publish_display_date,
                                type='date',
                                name='publish_date',
                                width='100%'
                            ),
                            rx.input(
                                default_value=editFormState.publish_display_time,
                                type='time',
                                 name='publish_time',
                                width='100%'
                            ),
                        width='100%'
                        ),
                        width='100%'
                    )
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=editFormState.handle_submit,
    )