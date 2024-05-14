#   Copyright (c) 2022 Push Technology Ltd., All Rights Reserved.
#
#   Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.
from diffusion import DiffusionError


class ClusterRoutingError(DiffusionError):
    pass


class ClusterRepartitionError(DiffusionError):
    pass


class InvalidOperationError(DiffusionError):
    pass


class ArgumentOutOfRangeError(DiffusionError):
    pass


class ArgumentNoneError(DiffusionError):
    pass
