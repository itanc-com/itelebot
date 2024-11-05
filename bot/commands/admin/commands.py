import logging
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes

from bot.jobs.delete_jobs import DeleteJobs


logger = logging.getLogger(__name__)


class Commands:
    def __init__(self, delete_job: DeleteJobs) -> None:
        self.delete_job = delete_job

    async def start(self, update: Update, context):
        await update.message.reply_text("Bot started. Only admins can send messages now.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Write valid command ")

    async def restrict_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        user = update.effective_user

        admins = await context.bot.get_chat_administrators(chat_id)
        if user.id in [admin.user.id for admin in admins]:
            await context.bot.set_chat_permissions(
                chat_id=chat_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                ),
            )
            warning = await update.message.reply_text("The group is now restricted. Only admins can send messages.")
            context.job_queue.run_once(
                self.delete_job.delete_warning,
                10,
                chat_id=chat_id,
                data=warning.message_id,
                name=f"delete_warning_{warning.message_id}",
            )
        else:
            warning = await update.message.reply_text("You don't have permission to restrict the group.")
            context.job_queue.run_once(
                self.delete_job.delete_warning,
                10,
                chat_id=chat_id,
                data=warning.message_id,
                name=f"delete_warning_{warning.message_id}",
            )

    # Command to remove restrictions and open the group
    async def open_group(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id
        user = update.effective_user

        # Check if the user is an admin
        admins = await context.bot.get_chat_administrators(chat_id)
        if user.id in [admin.user.id for admin in admins]:
            await context.bot.set_chat_permissions(
                chat_id=chat_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
            warning = await update.message.reply_text("The group is now open. Everyone can send messages.")

            context.job_queue.run_once(
                self.delete_job.delete_warning,
                10,
                chat_id=chat_id,
                data=warning.message_id,
                name=f"delete_warning_{warning.message_id}",
            )
        else:
            warning = await update.message.reply_text("You don't have permission to restrict the group.")
            context.job_queue.run_once(
                self.delete_job.delete_warning,
                10,
                chat_id=chat_id,
                data=warning.message_id,
                name=f"delete_warning_{warning.message_id}",
            )
