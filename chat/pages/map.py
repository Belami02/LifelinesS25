import reflex as rx
from chat.components.mainNavbar import mainNavbar

def map():
    return rx.html(
        """
        <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d205933.51120404797!2d51.34683944977115!3d25.284227640951382!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e45c534ffdce87f%3A0x44d9319f78cfd4b1!2sDoha!5e1!3m2!1sen!2sqa!4v1737446728461!5m2!1sen!2sqa"
            width="600"
            height="450"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
        ></iframe>
        """
    )

def MapPage():
    return rx.vstack(
        mainNavbar(),
        map(),
        align_items="center",
        spacing="8"
    )
