# LifelinesS25
Contains team's GrindMinds submission for Lifelines hackathon at CMUQ in Spring 2025

## Installation and Usage:

```bash
git clone https://github.com/Mohamed-Waiel-Shikfa/LifelinesS25.git
cd LifelinesS25
pip install -r requirements.txt
reflex init
reflex run
reflex db init  
reflex db makemigrations
reflex db migrate
```

and open localhost on the port it chooses

# Reconnect

Our platform is a digital space (website) for people missing and found people, pets and items. Users can post lost or found people/items with descriptions, images, and locations and each listing will create a community thread/channel. These public threads are hubs for information gathering, discussion, investigation, and collaboration where users contribute information, share tips, and work together to locate missing people or items. 

The platform is designed to foster a strong sense of community whether public or private, with each thread optimized for gathering clues and facilitating real-time communication between members. 

Innovative tools and features like geotagged locations, updates, interactive search maps, shared media repositories, checklists, task assignment, tracking, AI similarity lost & found search and archived success stories allow users to engage in the search process and increase the chances of recovery. 

We are not just showcasing lost items, we are helping people connect and come together as a community to assist those in need.

		
## Core Features:
1. Lost & Found Listings 
2. Community Channels/Threads for each listing item (Public/Private)
3. Geo-Location Integration
4. Collaboration Tools
5. Private Chats
6. Archive
7. Notification System

## Details:
1. **Lost & Found Listings**
-  Users can post lost or found items with descriptions, photos, and locations.
- Map tagging of items by location
- Categorize listings
- Search engine & Filters
- AI systems for similarity search to match (Lost to founds)

2. **Community Channels/Threads for each listing (Public/Private)**
- Each listing creates (is linked to) a thread for collaboration
- Features include geotagged updates, shared photos, and status flags (“last sighted”, “verified safe”).
- Users can upvote or tag useful clues to keep the thread focused.

3. **Geo-Location Integration**
- Interactive map view of reported locations, and search zones (with items pinned on the coordinates). 
- Alternative search view for lost/found in approximate map locations you select.
- Heatmaps to track areas of activity for missing items or people.

4. **Collaboration Tools**
- Shared Media Repository: 
- Checklists for tasks like calling shelters, checking lost & found offices, and volunteer gathering.
- Polls for collective decision-making
- Task Assignment and Tracking (Assign specific roles to community members, track task progress, and set deadlines for time-sensitive efforts)

5. **Private Chats**
- Connect users with individuals responsible for found items or those reporting lost items for private verification and claims.

6. **Archive**
- Success Stories: a section for archived items that were successfully found through the platform.
- User-submitted stories, how the community helped recover items.
- Case Studies: provide insights into complex recoveries as inspiration and guidance for users.
- Searchable History: browse, filter, and search.

7. **Notification System**
- Notify users via Email when descriptions of lost items match newly found items or reports.
- Alerts for updates in thread sightings, relevant information, and verified leads.

## New features that are not on existing platforms:
1. Community collaboration: dedicated thread or channels for each lost item where people share tips, and information in real-time
2. Investigation tools: geotagged updates, interactive maps, image sharing.
3. Enhanced communication: users can discuss and share advice, coordinate resources, and work together towards a shared purpose.
4. Search-based community-driven network of people.
5. Alternative search view (map view)
6. Upvote/tagging system in community threads
7. Task assignment and tracking 
8. Searchable history archive of lost & found items success stories
9. AI systems for similarity search
10. Heatmaps for activity tracking
11. Notification system for matching items
