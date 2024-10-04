from datetime import datetime, timedelta
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from bot.models.users import User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, tg_id: int, username: str):
        """Inserts a new user into the database."""
        new_user = User(telegram_id=tg_id, username=username)
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("User with this username or email already exists.")

    def get_user_by_username(self, username: str):
        """Fetches a user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_telegram_id(self, tg_id: int):
        """Fetches a user by ID."""
        user_record = self.db.query(User).filter_by(telegram_id=tg_id).first()
        if user_record:
            return {
                "id": user_record.id,
                "telegram_id": user_record.telegram_id,
                "username": user_record.username,
                "joined_at": user_record.joined_at,
                "invited_person": user_record.invited_person,
            }
        else:
            return None

    def get_all_users(self):
        """Fetches all users from the database."""
        return self.db.query(User).all()

    def silent_user(self, tg_id: int, duration: int):
        try:
            # Calculate the new silence_for time
            new_silence_for = datetime.now() + timedelta(minutes=duration)

            # Create an update statement
            stmt = (
                update(User)
                .where(User.telegram_id == tg_id)
                .values(silence_for=new_silence_for)
            )

            # Execute the update statement
            self.db.execute(stmt)

            # Commit the transaction
            self.db.commit()

        except Exception as e:
            # Rollback in case of an error
            self.db.rollback()
            print(f"An error occurred: {e}")
