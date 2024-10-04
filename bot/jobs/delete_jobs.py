import logging
from telegram.ext import ContextTypes
from telegram.error import BadRequest


logger = logging.getLogger(__name__)


class DeleteJobs:
    async def delete_warning(self, context: ContextTypes.DEFAULT_TYPE):
        job = context.job
        try:
            await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
            logger.info(f"Deleted warning message {job.data} in chat {job.chat_id}")
        except BadRequest as e:
            logger.error(f"Failed to delete warning message: {e}")
