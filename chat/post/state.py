
from typing import Optional, List
import reflex as rx 
from datetime import datetime, timezone
from chat.auth.state import SessionState
from chat.auth.models import PostModel, UserInfo
import sqlalchemy
from sqlmodel import select

class PostState(SessionState):
    posts: List['PostModel'] = []
    post: Optional['PostModel'] = None
    post_content: str = ""
    post_publish_active: bool = False

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

    def add_post(self, form_data:dict):
        with rx.session() as session:
            if 'category' not in form_data:
                form_data['category'] = '#default'  
            if 'publish_date' not in form_data:
                form_data['publish_date'] = datetime.now(timezone.utc)
            post = PostModel(**form_data)
            print("adding", post)
            session.add(post)
            session.commit()
            session.refresh(post) # post.id
            print("added", post)
            self.post = post

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
                sqlalchemy.orm.joinedload(PostModel.userinfo).joinedload(UserInfo.user)
            ).where(lookups)
            result = session.exec(sql_statement).one_or_none()
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

    def join_post(self, post_id: int):
        with rx.session() as session:
            post = session.exec(
                select(PostModel).where(
                    PostModel.id == post_id
                )
            ).one_or_none()
            if post is None:
                return
            userinfo = session.exec(
                select(UserInfo).where(
                    UserInfo.user_id == self.my_userinfo_id
                )
            ).one_or_none()
            if userinfo is None:
                return
            if userinfo not in post.members:
                post.members.append(userinfo)
                userinfo.joined_posts.append(post)
                session.add(post)
                session.add(userinfo)
                session.commit()
                session.refresh(post)
                session.refresh(userinfo)
            self.post = post

    def leave_post(self, post_id: int):
        with rx.session() as session:
            post = session.exec(
                select(PostModel).where(
                    PostModel.id == post_id
                )
            ).one_or_none()
            if post is None:
                return
            userinfo = session.exec(
                select(UserInfo).where(
                    UserInfo.user_id == self.my_userinfo_id
                )
            ).one_or_none()
            if userinfo is None:
                return
            if userinfo in post.members:
                post.members.remove(userinfo)
                userinfo.joined_posts.remove(post)
                session.add(post)
                session.add(userinfo)
                session.commit()
                session.refresh(post)
                session.refresh(userinfo)
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