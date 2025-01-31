import reflex as rx
import reflex_local_auth
from .models import UserInfo

from typing import Optional
import sqlmodel

from fastapi import UploadFile
import shutil
import os


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
            print(result)
            return result
        
    def on_load(self):
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir
        print(self.authenticated_user_info)

    def perform_logout(self):
        self.do_logout()
        return rx.redirect("/login")
    
    @property
    def username(self) -> Optional[str]:
        user_info = self.authenticated_user.username
        return user_info if user_info else None
    
    async def handle_profile_photo_submit(self, files: list[rx.UploadFile]):
        if not files:
            return
        file = files[0]
        upload_data = await file.read()
        upload_dir = rx.get_upload_dir()
        file_path = upload_dir / file.filename
        
        with file_path.open("wb") as buffer:
            buffer.write(upload_data)
        
        with rx.session() as session:
            userinfo = session.exec(
                sqlmodel.select(UserInfo).where(UserInfo.user_id == self.my_userinfo_id)
            ).one_or_none()
            if userinfo is None:
                return
            userinfo.profile_photo = file.filename
            session.add(userinfo)
            session.commit()
            session.refresh(userinfo)
            self.authenticated_user_info = userinfo
            print(f"Profile photo updated: {userinfo.profile_photo}")
        
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