
from typing import Optional, List
import reflex as rx 
from datetime import datetime, timezone
from chat.auth.state import SessionState
from chat.auth.models import PostModel, ImageModel, UserInfo
import sqlalchemy
from sqlmodel import select
from chat.pages.map import map
import base64

class PostState(SessionState):
    posts: List['PostModel'] = []
    post: Optional['PostModel'] = None
    post_content: str = ""
    post_publish_active: bool = False
    current_post_id: Optional[int] = None
    post_images: List[ImageModel] = []
    loading_images: bool = False

    def set_current_post(self, post_id: int):
        """Set the current post and navigate to it."""
        self.current_post_id = post_id
        return rx.redirect(f"/post/{post_id}")

    @rx.var
    def state_post_id(self):
        return self.router.page.params.get("post_id", "")

    @rx.var
    def post_url(self):
        if not self.post:
            return "/post"
        return f"/post/{self.post.id}"

    @rx.var
    def post_edit_url(self):
        if not self.post:
            return "/post"
        return f"/post/{self.post.id}/edit"
    
    @rx.var
    def is_member(self) -> bool:
        """Check if the current user is a member of the post."""
        try:
            if self.post is None or self.my_user_id is None:
                return False

            with rx.session() as session:
                post = session.exec(
                    select(PostModel)
                    .options(sqlalchemy.orm.joinedload(PostModel.members))
                    .where(PostModel.id == self.post.id)
                ).unique().one_or_none()
                
                if post is None or not post.members:
                    return False
                
                member_ids = [member.user_id for member in post.members]
                return self.my_user_id in member_ids
        except Exception as e:
            print(f"Error checking membership: {e}")
            return False
    
    def post_info(self, post_id: int) -> Optional[PostModel]:
        """Retrieve the post information by post_id."""
        with rx.session() as session:
            return session.exec(
                select(PostModel).where(PostModel.id == post_id)
            ).one_or_none()

    def load_post_images(self, post_id: int):
        """Load all images associated with the post with proper error handling."""
        try:
            self.loading_images = True
            with rx.session() as session:
                # Use joinedload to prevent N+1 queries
                query = (
                    select(ImageModel)
                    .options(
                        sqlalchemy.orm.joinedload(ImageModel.post)
                    )
                    .where(ImageModel.post_id == post_id)
                    .order_by(ImageModel.id.desc())  # Latest images first
                )
                self.post_images = session.exec(query).all()
        except Exception as e:
            print(f"Error loading images: {e}")
            self.post_images = []
        finally:
            self.loading_images = False

    def load_all_images(self):
        """Load all images from the database with proper error handling."""
        try:
            self.loading_images = True
            with rx.session() as session:
                # Direct query to get all images with their binary data
                query = (
                    select(ImageModel)
                    .options(
                        sqlalchemy.orm.joinedload(ImageModel.post)  # Join with post to get post details
                    )
                    .order_by(ImageModel.id.desc())  # Latest images first
                )
                self.post_images = session.exec(query).all()  # Get all images as ImageModel objects
                
                print(f"Loaded {len(self.post_images)} images from database")
                
        except Exception as e:
            print(f"Error loading images: {e}")
            self.post_images = []
        finally:
            self.loading_images = False

    async def handle_post_images_submit(self, files: list[rx.UploadFile]):
        """Handles image upload for a post and stores images as binary data in the database."""
        if not files or not self.post:
            return

        try:
            # Read image data
            image_data_list = []
            for file in files:
                image_data = await file.read()  # Read each image as bytes
                image_data_list.append(image_data)

            # Update the database
            with rx.session() as session:
                # Create ImageModel instances for each image
                for image_data in image_data_list:
                    image = ImageModel(
                        post_id=self.post.id,
                        image_data=image_data
                    )
                    session.add(image)
                
                session.commit()
                print(f"Images updated for Post {self.post.id}")
                
                # Refresh post images
                self.load_post_images(self.post.id)
        except Exception as e:
            print(f"Error uploading images: {e}")

    def image_base64(self, image_data: bytes) -> str:
        """Convert binary image data to a base64 string for display."""
        return "data:image/png;base64," + base64.b64encode(image_data).decode("utf-8")

    def load_posts(self, *args, **kwargs):
        with rx.session() as session:
            result = session.exec(
                select(PostModel).options(
                    sqlalchemy.orm.joinedload(PostModel.userinfo)
                ).where(PostModel.userinfo_id == self.my_userinfo_id)
                .order_by(PostModel.publish_date.desc())
            ).all()
            self.posts = result

    def load_all_posts(self, *args, **kwargs):
        with rx.session() as session:
            result = session.exec(
                select(PostModel).options(
                    sqlalchemy.orm.joinedload(PostModel.userinfo).joinedload(UserInfo.user)
                ).order_by(PostModel.publish_date.desc())
            ).all()
            self.posts = result

    def add_post(self, form_data: dict):
        with rx.session() as session:
            try:
                if 'title' not in form_data or 'content' not in form_data:
                    print("Missing required fields: 'title' or 'content'")
                    return

                if 'category' not in form_data:
                    form_data['category'] = '#default'
                if 'publish_date' not in form_data:
                    form_data['publish_date'] = datetime.now(timezone.utc)

                post_data = form_data.copy()
                if 'members' in post_data:
                    del post_data['members']
                
                post = PostModel(**post_data)
                post.members = []  
                
                if self.my_userinfo_id is not None:
                    post.userinfo_id = self.my_userinfo_id
                
                session.add(post)
                session.commit()
                session.refresh(post)
                self.post = post
                print("Added post:", post)
                return post
            except Exception as e:
                print(f"Error adding post: {e}")
                session.rollback()
                return None

    def delete_post(self, post_id: int):
        """Dekete the post and all its associated data from the database."""
        try:
            with rx.session() as session:
                post = session.exec(
                    select(PostModel).where(
                        PostModel.id == post_id
                    )
                ).one_or_none()

                print("Hm?")
                if post is None:
                    print(f"Post {post_id} not found.")
                    return rx.redirect("/post")
                
                print("joined_posts?")
                # Remove all associations
                for member in post.members:
                    member.joined_posts = [p for p in member.joined_posts.copy() if p.id != post_id]
                    session.add(member)

                print("What?")
                
                session.delete(post)
                session.commit()
                print(f"Post {post_id} and all its associated data have been removed.")
                return rx.redirect("/post")
        except Exception as e:
            print(f"Error removing post: {e}")
            return rx.redirect("/post")
        
    def delete_post(self, post_id: int):
        """Delete the post and all its associated data from the database."""
        try:
            with rx.session() as session:
                post = session.exec(
                    select(PostModel)
                    .options(
                        sqlalchemy.orm.joinedload(PostModel.members)
                        .joinedload(UserInfo.joined_posts)
                    )
                    .where(PostModel.id == post_id)
                ).unique().one_or_none()

                if post is None:
                    print(f"Post {post_id} not found.")
                    return rx.redirect("/post")
                
                member_ids = [member.user_id for member in post.members]
                print(f"Removing post {post_id} with members: {member_ids}")
                
                affected_users = post.members.copy()
                
                post.members = []
                session.add(post)
                
                for user in affected_users:
                    fresh_user = session.exec(
                        select(UserInfo)
                        .options(sqlalchemy.orm.joinedload(UserInfo.joined_posts))
                        .where(UserInfo.id == user.id)
                    ).unique().one_or_none()
                    
                    if fresh_user:
                        fresh_user.joined_posts = [p for p in fresh_user.joined_posts if p.id != post_id]
                        session.add(fresh_user)
                
                session.commit()
                
                session.delete(post)
                session.commit()
                
                print(f"Post {post_id} and all its associated data have been removed successfully")
                return rx.redirect("/post")
                
        except Exception as e:
            print(f"Error removing post: {e}")
            session.rollback()
            return rx.redirect(f"/post/{post_id}")

    def to_post(self, edit_page=False):
        if not self.post:
            return rx.redirect("/post")
        if edit_page:
             return rx.redirect(f"{self.post_edit_url}")
        return rx.redirect(f"{self.post_url}")
    
    def get_post_detail(self):
        if self.state_post_id is None:
            self.post = None
            self.post_content = ""
            self.post_publish_active = False
            return 
        lookups = (
            PostModel.id == self.state_post_id
            # (PostModel.userinfo_id == self.my_userinfo_id) &
            # (PostModel.id == self.state_post_id)
        )
        with rx.session() as session:
            if self.state_post_id == "":
                self.post = None
                return
            sql_statement = select(PostModel).options(
                sqlalchemy.orm.joinedload(PostModel.userinfo).joinedload(UserInfo.user),
                sqlalchemy.orm.joinedload(PostModel.members)
            ).where(lookups)
            result = session.exec(sql_statement).unique().one_or_none()
            if result:
                print("Members:")
                for member in result.members:
                    print(f"Member ID: {member.user_id}, Username: {member.user.username}, Email: {member.email}")
            if result is None:
                self.post_content = ""
                self.post = None
                self.post_publish_active = False
                return
            
            if result.userinfo:  # DB lookup
                print('working')
                result.userinfo.user  # DB lookup
            self.post = result
            if result is None:
                self.post_content = ""
                return
            self.post_content = self.post.content
            self.post_publish_active = self.post.publish_active

    def save_post_edits(self, post_id : int, updated_data : dict):
        with rx.session() as session:
            post = session.exec(
                select(PostModel).where(
                    PostModel.id == post_id
                )
            ).one_or_none()
            if post is None:
                return
            for key, value in updated_data.items():
                setattr(post, key, value)
            if 'publish_date' not in updated_data:
                post.publish_date = datetime.now(timezone.utc)
            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post

class addPostFormState(PostState):
    form_data: dict = {}

    def handle_submit(self, form_data):
        data = form_data.copy()
        if self.my_userinfo_id is not None:
            data['userinfo_id'] = self.my_userinfo_id
        self.form_data = data
        self.add_post(data)
        return self.to_post(edit_page=True)

class editFormState(PostState):
    form_data: dict = {}
    # post_content: str = ""

    @rx.var
    def is_owner(self) -> bool:
        return self.post and self.post.userinfo_id == self.my_userinfo_id

    @rx.var
    def publish_display_date(self) -> str:
        if not self.post:
            return datetime.now().strftime("%Y-%m-%d")
        if not self.post.publish_date:
            return datetime.now().strftime("%Y-%m-%d")
        return self.post.publish_date.strftime("%Y-%m-%d")
    
    @rx.var
    def publish_display_time(self) -> str:
        if not self.post:
            return datetime.now().strftime("%H:%M:%S")
        if not self.post.publish_date:
            return datetime.now().strftime("%H:%M:%S")
        return self.post.publish_date.strftime("%H:%M:%S")

    def handle_submit(self, form_data):
        self.form_data = form_data
        post_id = form_data.pop('post_id')
        publish_date = None
        if 'publish_date' in form_data:
            publish_date = form_data.pop('publish_date')
        publish_time = None
        if 'publish_time' in form_data:
            publish_time = form_data.pop('publish_time')
        publish_input_string = f"{publish_date} {publish_time}"
        try:
            final_publish_date = datetime.strptime(publish_input_string, '%Y-%m-%d %H:%M:%S')
        except:
            final_publish_date = None
        publish_active = False
        if 'publish_active' in form_data:
            publish_active = form_data.pop('publish_active') == "on"
        updated_data = {**form_data}
        updated_data['publish_active'] = publish_active
        updated_data['publish_date'] = final_publish_date
        self.save_post_edits(post_id, updated_data)
        return self.to_post()