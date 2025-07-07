import functools
import logging
from telegram.ext import Application, AIORateLimiter
from bot.core.db.init_db import get_db, init_db
from bot.core.pydantic.config import settings
from bot.handlers.daily import DailyHanlder
from bot.jobs.daily_jobs import DailyJobsManager
from bot.jobs.delete_jobs import DeleteJobs
from setup import setup_application


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting the bot application...")

        init_db()  # Initialize the database

        db_session = next(get_db())

        rate_limiter = AIORateLimiter(
            settings.RATE_LIMIT_REQUESTS, settings.RATE_LIMIT_PERIOD
        )

        application = (
            Application.builder()
            .token(settings.TOKEN)
            .rate_limiter(rate_limiter)
            .pool_timeout(settings.TIMEOUT)
            .connection_pool_size(settings.POOL_SIZE)
            .post_init(
                functools.partial(setup_application, db_session=db_session)
            )  # Pass the db_session
            .build()
        )
        #delete_job_obj = DeleteJobs()

        #daily_hanlder_obj = DailyHanlder(
        #   delete_job=delete_job_obj, db_session=db_session
        #)
        #daily_jobs_manager = DailyJobsManager(application.job_queue, daily_hanlder_obj)
        #daily_jobs_manager.schedule_close_group(hours=2, minute=0)
        #daily_jobs_manager.schedule_open_group(hours=8, minitue=0)

        application.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
