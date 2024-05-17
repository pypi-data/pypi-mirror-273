from ..plugins.snowflake import Snowflake


try:
    __version__ = pkg_resources.get_distribution("metaflow-snowflake").version
except:
    # this happens on remote environments since the job package
    # does not have a version
    __version__ = None