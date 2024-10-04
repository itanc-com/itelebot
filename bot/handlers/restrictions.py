import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus
from telegram.error import BadRequest
from bot.commands.admin.commands import Commands
from bot.jobs.delete_jobs import DeleteJobs


logger = logging.getLogger(__name__)


class Restriction:
    def __init__(self, delete_job: DeleteJobs, commands: Commands) -> None:
        self.delete_job = delete_job
        self.commands = commands

    async def restrict_non_admins(
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

            if not is_admin:
                try:
                    # Try to delete the message
                    await message.delete()
                    logger.info(
                        f"Deleted message from non-admin user {user.id} in chat {chat.id}"
                    )
                except BadRequest as e:
                    logger.error(f"Failed to delete message: {e}")

                try:
                    # Try to send a warning message
                    warning = await chat.send_message(
                        f"Sorry {user.mention_html()}, only admins can send messages in this group.",
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

    async def close_or_open_group_handler(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        text = update.message.text
        if text == "$close":
            await self.commands.restrict_group(update, context)
        elif text == "$open":
            await self.commands.open_group(update, context)
