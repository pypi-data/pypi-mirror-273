#   Copyright (c) 2023 Push Technology Ltd., All Rights Reserved.
#
#   Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.
import enum


class StreamStructure(enum.IntEnum):
    """
    The structure of the event stream.
    """

    EDIT_EVENT_STREAM = enum.auto()
    """
    The stream contains edit events
    """

    VALUE_EVENT_STREAM = enum.auto()
    """
    The stream contains value events
    """
