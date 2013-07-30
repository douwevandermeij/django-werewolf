__all__ = ('CHIEF_EDITORS_GROUP_NAME', 'EDITORS_GROUP_NAME', 'WRITERS_GROUP_NAME')

from news.conf import get_setting

CHIEF_EDITORS_GROUP_NAME = get_setting('CHIEF_EDITORS_GROUP_NAME')

EDITORS_GROUP_NAME = get_setting('EDITORS_GROUP_NAME')

WRITERS_GROUP_NAME = get_setting('WRITERS_GROUP_NAME')
