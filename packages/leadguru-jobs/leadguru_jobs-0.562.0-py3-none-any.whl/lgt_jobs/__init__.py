name = "lgt_jobs"

from .jobs.user_balance_update import UpdateUserBalanceJob, UpdateUserBalanceJobData
from .jobs.send_slack_message import SendSlackMessageJob, SendSlackMessageJobData
from .jobs.analytics import (TrackAnalyticsJob, TrackAnalyticsJobData)
from .jobs.connect_sources import (ConnectSourceJobData, ConnectSourceJob)
from .jobs.bot_stats_update import (BotStatsUpdateJob, BotStatsUpdateJobData)
from .jobs.chat_history import (LoadChatHistoryJob, LoadChatHistoryJobData)
from .jobs.update_slack_profile import (UpdateExternalUserProfileJob, UpdateExternalUserProfileJobData)
from .jobs.mass_message import SendMassMessageSlackChannelJob, SendMassMessageSlackChannelJobData
from .basejobs import (BaseBackgroundJobData, BaseBackgroundJob, InvalidJobTypeException)
from .smtp import (SendMailJob, SendMailJobData)
from .runner import (BackgroundJobRunner)
from .simple_job import (SimpleTestJob, SimpleTestJobData)

jobs_map = {
    "SimpleTestJob": SimpleTestJob,
    "BotStatsUpdateJob": BotStatsUpdateJob,
    "SendMailJob": SendMailJob,
    "TrackAnalyticsJob": TrackAnalyticsJob,
    "LoadChatHistoryJob": LoadChatHistoryJob,
    "UpdateExternalUserProfileJob": UpdateExternalUserProfileJob,
    "SendSlackMessageJob": SendSlackMessageJob,
    "UpdateUserBalanceJob": UpdateUserBalanceJob,
    "SendMassMessageSlackChannelJob": SendMassMessageSlackChannelJob,
    "ConnectSourceJob": ConnectSourceJob
}
__all__ = [
    # Jobs
    SimpleTestJob,
    BotStatsUpdateJob,
    SendMailJob,
    SimpleTestJob,
    LoadChatHistoryJob,
    UpdateExternalUserProfileJob,
    TrackAnalyticsJob,
    SendSlackMessageJob,
    UpdateUserBalanceJob,
    SendMassMessageSlackChannelJob,
    ConnectSourceJob,

    # module classes
    BackgroundJobRunner,
    BaseBackgroundJobData,
    BaseBackgroundJob,
    InvalidJobTypeException,
    BotStatsUpdateJobData,
    SendMailJobData,
    SimpleTestJobData,
    LoadChatHistoryJobData,
    UpdateExternalUserProfileJobData,
    TrackAnalyticsJobData,
    SendSlackMessageJobData,
    UpdateUserBalanceJobData,
    SendMassMessageSlackChannelJobData,
    ConnectSourceJobData,
    # mapping
    jobs_map
]
