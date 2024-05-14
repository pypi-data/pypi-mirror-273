# /*******************************************************************************
#  * Copyright (c) 2021 - 2022 Push Technology Ltd., All Rights Reserved.
#  *
#  * Use is subject to license terms.
#  *
#  * NOTICE: All information contained herein is, and remains the
#  * property of Push Technology. The intellectual and technical
#  * concepts contained herein are proprietary to Push Technology and
#  * may be covered by U.S. and Foreign Patents, patents in process, and
#  * are protected by trade secret or copyright law.
#  *******************************************************************************/
try:
    from typing import TypeAlias  # type: ignore
except ImportError:
    from typing_extensions import TypeAlias  # type: ignore

from diffusion import DiffusionError


class InvalidBranchMappingError(DiffusionError):
    """
    Exception indicating an invalid BranchMapping or
    BranchMappingTable.

    See Also: SessionTrees
    """


InvalidBranchMappingException: TypeAlias = InvalidBranchMappingError
