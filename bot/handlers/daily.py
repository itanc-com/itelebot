from datetime import timedelta, datetime
import logging
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes
from bot.core.pydantic.config import settings
from bot.utils.read_json import load_messages
from bot.jobs.delete_jobs import DeleteJobs
from bot.repo.users import UserRepo
from sqlalchemy.orm import Session
from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest


logger = logging.getLogger(__name__)


class DailyHanlder:
    def __init__(self, delete_job: DeleteJobs, db_session: Session) -> None:
        self.messages = load_messages("daily_messages.json")
        self.delete_job = delete_job
        self.users_repo = UserRepo(db=db_session)

    async def open_group(self, context: ContextTypes.DEFAULT_TYPE):
        chat_id = settings.CHAT_ID

        chat_permissions = ChatPermissions(
            can_send_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False,
        )
        await context.bot.set_chat_permissions(
            chat_id=chat_id, permissions=chat_permissions
        )
        await context.bot.send_message(
            chat_id=chat_id, text=self.messages["morning_message"]
        )

    async def close_group(self, context: ContextTypes.DEFAULT_TYPE):
        chat_id = settings.CHAT_ID

        chat_permissions = ChatPermissions(
            can_send_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        await context.bot.set_chat_permissions(
            chat_id=chat_id, permissions=chat_permissions
        )
        await context.bot.send_message(
            chat_id=chat_id, text=self.messages["night_message"]
        )

    async def welcome_new_member(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        chat = update.effective_chat
        message = update.effective_message
        for member in update.message.new_chat_members:
            message = self.messages["welcome_message"].format(
                user=member.first_name, group=update.effective_chat.title
            )
            try:
                self.users_repo.add_user(tg_id=member.id, username=member.username)
            except ValueError as e:
                logger.error(f"Failed to insert user in databse: {e}")
            warning = await context.bot.send_message(
                chat_id=update.effective_chat.id, text=message
            )

            context.job_queue.run_once(
                self.delete_job.delete_warning,
                30,
                data=warning.message_id,
                chat_id=chat.id,
            )

    async def check_invited_user(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        user = update.effective_user
        chat = update.effective_chat
        message = update.effective_message

        if chat.type == "private":
            return

        try:
            member = await chat.get_member(user.id)
            is_admin = member.status in [
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            ]
            try:
                user = self.users_repo.get_user_by_telegram_id(user.id)
                print(f"Added user: {user}")
            except ValueError as e:
                print(f"Error: {e}")

            if not is_admin and user["invited_person"] != 1:
                try:
                    # Try to delete the message
                    await message.delete()
                    logger.info(
                        f"Deleted message from non-admin user in chat {chat.id}"
                    )
                except BadRequest as e:
                    logger.error(f"Failed to delete message: {e}")

                try:
                    # Try to send a warning message
                    warning = await chat.send_message(
                        "برای ارسال پیام شما باید یک نفر دیگر رو نیز به گروه اضافه نمایید ",
                        parse_mode="HTML",
                    )
                    logger.info(
                        f"Sent warning to non-admin user {user.id} in chat {chat.id}"
                    )

                    context.job_queue.run_once(
                        self.delete_job.delete_warning,
                        10,
                        chat_id=chat.id,
                        data=warning.message_id,
                        name=f"delete_warning_{warning.message_id}",
                    )

                except BadRequest as e:
                    logger.error(f"Failed to send warning message: {e}")
        except Exception as e:
            logger.error(f"Error in restrict_non_admins: {e}", exc_info=True)

    async def silence_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        chat = update.effective_chat
        message = update.effective_message
        text = message.text

        member = await chat.get_member(user.id)
        is_admin = member.status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ]
        if not is_admin:
            warning = await update.message.reply_text(
                "This command is only available to admins."
            )
            await message.delete()

            context.job_queue.run_once(
                self.delete_job.delete_warning,
                10,
                chat_id=chat.id,
                data=warning.message_id,
                name=f"delete_warning_{warning.message_id}",
            )

            return

        silence_time = int(text[8:])

        target_user = update.message.reply_to_message.from_user
        target_user_id = target_user.id

        user = self.users_repo.silent_user(target_user_id, silence_time)

        try:
            # Create a ChatMemberBanned object
            # banned_member = ChatMemberBanned(
            #     user=target_user,
            #     until_date=until_date
            # )

            # Apply the ban
            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=target_user_id,
                permissions=ChatPermissions(can_send_messages=False),
                until_date=datetime.now() + timedelta(minutes=silence_time),
            )

            reply_message = await update.message.reply_text(
                f"User {target_user.first_name} has been silenced."
            )

            context.job_queue.run_once(
                self.delete_job.delete_warning,
                10,
                chat_id=chat.id,
                data=reply_message.message_id,
                name=f"delete_warning_{reply_message.message_id}",
            )

        except Exception as e:
            logger.error(f"Failed to silence user: {str(e)}", exc_info=True)
