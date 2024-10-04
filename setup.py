from telegram.ext import Application, MessageHandler, CommandHandler, filters


from bot.commands.admin.commands import Commands
from bot.handlers.daily import DailyHanlder
from bot.handlers.restrictions import Restriction
from bot.jobs.delete_jobs import DeleteJobs
from sqlalchemy.orm import Session


async def setup_application(application: Application, db_session: Session) -> None:
    delete_job_obj = DeleteJobs()

    commands_obj = Commands(delete_job_obj)

    restriction_obj = Restriction(delete_job=delete_job_obj, commands=commands_obj)

    daily_handler_obj = DailyHanlder(delete_job=delete_job_obj, db_session=db_session)

    application.add_handler(
        MessageHandler(
            filters.Regex(r"^silence \d+$") & filters.REPLY,
            daily_handler_obj.silence_user,
        )
    )

    application.add_handler(CommandHandler("start", commands_obj.start))
    application.add_handler(CommandHandler("help", commands_obj.help_command))

    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, daily_handler_obj.welcome_new_member
        )
    )

    # application.add_handler(
    #     MessageHandler(
    #         filters.TEXT & ~filters.COMMAND, daily_handler_obj.check_invited_user
    #     )
    # )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, restriction_obj.close_or_open_group_handler
        )
    )
