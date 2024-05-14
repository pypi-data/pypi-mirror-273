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


class SessionLockScope(enum.IntEnum):
    """
    Values for the `scope` parameter of
    [Session.lock][diffusion.session.Session.lock]

    Since:
        6.10
    """

    UNLOCK_ON_SESSION_LOSS = 0
    """
    The lock will be released when the acquiring session loses its
    current connection to the server.
    """

    UNLOCK_ON_CONNECTION_LOSS = 1
    """
    The lock will be released when the acquiring session is closed.
    """

    def __str__(self):
        return self.name
