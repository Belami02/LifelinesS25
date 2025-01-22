import reflex as rx
from chat.components.mainNavbar import mainNavbar

def about() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.box(
                rx.hstack(
                    rx.card(
                        rx.section(
                            rx.inset(
                                rx.heading("Reconnect", text_align="center"),
                                side="top",
                                pb="current",
                            ),
                            rx.text("   Our platform is a digital space (website) for people missing and found people, pets and items. Users can post lost or found people/items with descriptions, images, and locations and each listing will create a community thread/channel. These public threads are hubs for information gathering, discussion, investigation, and collaboration where users contribute information, share tips, and work together to locate missing people or items. The platform is designed to foster a strong sense of community whether public or private, with each thread optimized for gathering clues and facilitating real-time communication between members. Innovative tools and features like geotagged locations, updates, interactive search maps, shared media repositories, checklists, task assignment, tracking, AI similarity lost & found search and archived success stories allow users to engage in the search process and increase the chances of recovery. We are not just showcasing lost items, we are helping people connect and come together as a community to assist those in need."),
                            padding_left="12px",
                            padding_right="12px",
                            # background_color="var(--gray-2)",
                        ),
                        max_width="850px",
                    ),
                    justify_content="center",
                    align_items="center",
                    width="100%"
                ),
                rx.hstack(
                    rx.card(
                        rx.section(
                            rx.inset(
                                rx.heading("Core Features", text_align="center"),
                                side="top",
                                pb="current",
                            ),
                            rx.list.ordered(
                                rx.list.item("Lost & Found Listings "),
                                rx.list.item("Community Channels/Threads for each listing (Public/Private)"),
                                rx.list.item("Geo-Location Integration"),
                                rx.list.item("Collaboration Tools"),
                                rx.list.item("Private Chats"),
                                rx.list.item("Archive"),
                                rx.list.item("Notification System")
                            ),
                            padding_left="12px",
                            padding_right="12px",
                            # background_color="var(--gray-2)",
                        ),
                        width="850px",
                    ),
                    justify_content="center",
                    align_items="center",
                    width="100%"
                ),
                rx.hstack(
                    rx.card(
                        rx.section(
                            rx.inset(
                                rx.heading("Details", text_align="center"),
                                side="top",
                                pb="current",
                            ),
                            rx.list.ordered(
                                rx.list.item("Lost & Found Listings", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Users can post lost or found items with descriptions, photos, and locations."),
                                    rx.list.item("Map tagging of items by location"),
                                    rx.list.item("Categorize listings"),
                                    rx.list.item("Search engine & Filters"),
                                    rx.list.item("AI systems for similarity search to match (Lost to founds)"),
                                ),
                                rx.list.item("Community Channels/Threads for each listing (Public/Private)", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Each listing creates (is linked to) a thread for collaboration"),
                                    rx.list.item("Features include geotagged updates, shared photos, and status flags (“last sighted”, “verified safe”)."),
                                    rx.list.item("Users can upvote or tag useful clues to keep the thread focused."),
                                ),
                                rx.list.item("Geo-Location Integration", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Interactive map view of reported locations, and search zones (with items pinned on the coordinates)."),
                                    rx.list.item("Alternative search view for lost/found in approximate map locations you select."),
                                    rx.list.item("Heatmaps to track areas of activity for missing items or people."),
                                ),
                                rx.list.item("Collaboration Tools", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Shared Media Repository"),
                                    rx.list.item("Checklists for tasks like calling shelters, checking lost & found offices, and volunteer gathering"),
                                    rx.list.item("Polls for collective decision-making"),
                                    rx.list.item("Task Assignment and Tracking (Assign specific roles to community members, track task progress, and set deadlines for time-sensitive efforts)"),
                                ),
                                rx.list.item("Private Chats", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Connect users with individuals responsible for found items or those reporting lost items for private verification and claims."),
                                ),
                                rx.list.item("Archive", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Success Stories: a section for archived items that were successfully found through the platform. User-submitted stories, how the community helped recover items."),
                                    rx.list.item("Case Studies: provide insights into complex recoveries as inspiration and guidance for users."),
                                    rx.list.item("Searchable History: browse, filter, and search."),
                                ),
                                rx.list.item("Notification System", font_weight="bold"),
                                rx.list.unordered(
                                    rx.list.item("Notify users via Email when descriptions of lost items match newly found items or reports."),
                                    rx.list.item("Alerts for updates in thread sightings, relevant information, and verified leads."),
                                ),
                            ),
                            padding_left="12px",
                            padding_right="12px",
                            # background_color="var(--gray-2)",
                        ),
                        width="850px",
                    ),
                    justify_content="center",
                    align_items="center",
                    width="100%"
                ),
                rx.hstack(
                    rx.card(
                        rx.section(
                            rx.inset(
                                rx.heading("New features that we'll have that are not on existing platforms", text_align="center", margin_bottom="4"),
                                side="top",
                                pb="current",
                            ),
                            rx.list.ordered(
                                rx.list.item("Community collaboration: dedicated thread or channels for each lost item where people share tips, and information in real-time."),
                                rx.list.item("Investigation tools: geotagged updates, interactive maps, image sharing."),
                                rx.list.item("Enhanced communication: users can discuss and share advice, coordinate resources, and work together towards a shared purpose."),
                                rx.list.item("Search-based community-driven network of people."),
                                rx.list.item("Alternative search view (map view)."),
                                rx.list.item("Upvote/tagging system in community threads."),
                                rx.list.item("Task assignment and tracking."),
                                rx.list.item("Searchable history archive of lost & found items success stories."),
                                rx.list.item("AI systems for similarity search."),
                                rx.list.item("Heatmaps for activity tracking."),
                                rx.list.item("Notification system for matching items."),
                            ),
                            padding_left="12px",
                            padding_right="12px",
                            # background_color="var(--gray-2)",
                        ),
                        width="850px",
                    ),
                    justify_content="center",
                    align_items="center",
                    width="100%"
                ),
            ),

            align_items="start",
            spacing="4",
            padding="4",
            max_width="1000px",
            margin="auto",
            background_color="var(--gray-2)",
            box_shadow="lg",
            border_radius='lg',
        ),
        padding="8",
        background_color="gray.100",
        min_height="100vh"
    )

def AboutPage():
    return rx.vstack(
        mainNavbar(),
        about(),
        align_items="center",
        spacing="8"
    )