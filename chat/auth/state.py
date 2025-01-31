import reflex as rx
import reflex_local_auth
from .models import UserInfo
from chat.auth.models import PostModel, UserInfo
import sqlalchemy
from sqlmodel import select
from typing import Optional
import sqlmodel
import base64

class SessionState(reflex_local_auth.LocalAuthState):
    @rx.var(cache=True)
    def my_userinfo_id(self) -> str | None:
        if self.authenticated_user_info is None:
            return None
        return self.authenticated_user_info.id

    @rx.var(cache=True)
    def my_user_id(self) -> str | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.id

    @rx.var(cache=True)
    def authenticated_username(self) -> str | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username

    @rx.var(cache=True)
    def authenticated_user_info(self) -> UserInfo | None:
        if self.authenticated_user.id < 0:
            return None
        with rx.session() as session:
            result = session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()
            if result is None:
                return None
            # print(result)
            return result
        
    @rx.var
    def profile_photo_base64(self) -> str:
        """Convert binary profile photo to a base64 string for display."""
        with rx.session() as session:
            user_info = session.exec(
                sqlmodel.select(UserInfo).where(UserInfo.user_id == self.authenticated_user.id)
            ).one_or_none()
            if user_info and user_info.profile_photo:
                return "data:image/png;base64," + base64.b64encode(user_info.profile_photo).decode("utf-8")
        return "/BlankProfile.png"

    def on_load(self):
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir
        # print(self.authenticated_user_info)

    def perform_logout(self):
        self.do_logout()
        return rx.redirect("/login")
    
    @property
    def username(self) -> Optional[str]:
        user_info = self.authenticated_user.username
        return user_info if user_info else None
    
    async def handle_profile_photo_submit(self, files: list[rx.UploadFile]):
        """Handles profile photo upload and stores it as binary data in the database."""

        if not files:
            return

        file = files[0]
        image_data = await file.read()  # Read image as bytes

        # Update database
        with rx.session() as session:
            userinfo = session.exec(
                sqlmodel.select(UserInfo).where(UserInfo.user_id == self.authenticated_user.id)
            ).one_or_none()
            if userinfo:
                userinfo.profile_photo = image_data  # Store binary data
                session.add(userinfo)
                session.commit()
                session.refresh(userinfo)
                self.authenticated_user_info = userinfo  # Update state
                print(f"Profile photo updated in DB")
            else:
                print(f"No UserInfo found for user_id: {self.my_userinfo_id}")

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
                    UserInfo.user_id == self.authenticated_user.id
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
        
class MyRegisterState(reflex_local_auth.RegistrationState):
    def handle_registration(
        self, form_data
    ) -> rx.event.EventSpec | list[rx.event.EventSpec]:
        """Handle registration form on_submit.

        Set error_message appropriately based on validation results.

        Args:
            form_data: A dict of form fields and values.
        """
        username = form_data["username"]
        password = form_data["password"]
        validation_errors = self._validate_fields(
            username, password, form_data["confirm_password"]
        )
        if validation_errors:
            self.new_user_id = -1
            return validation_errors
        self._register_user(username, password)
        return self.new_user_id
    
    def handle_registration_email(self, form_data):
        new_user_id = self.handle_registration(form_data)
        print(new_user_id)
        if new_user_id >= 0:
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=form_data["email"],
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return type(self).successful_registration