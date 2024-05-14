#   Copyright (c) 2022 Push Technology Ltd., All Rights Reserved.
#
#   Use is subject to license terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of Push Technology. The intellectual and technical
#  concepts contained herein are proprietary to Push Technology and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

#
#   Use is subject to license terms.
#
from diffusion import DiffusionError
from diffusion.internal.protocol import ProtocolError


class SessionError(DiffusionError):
    pass


class IncompatibleTopicError(SessionError):
    """
    The topic is incompatible.
    """


class UpdateFailedError(SessionError):
    pass


class NoSuchTopicError(SessionError):
    """
    There is no such topic.
    """


class NoTopicFoundError(SessionError):
    pass


class NoSuchEventError(SessionError):
    """
    The exception used to report a time series topic does not have an original
    event with the sequence number provided by an

    See Also:
        [timeseries.edit][diffusion.features.timeseries.TimeSeries.edit] operation.

    Notes:
        Added in version 6.9.
    """


class ExistingTopicError(SessionError):
    pass


class InvalidTopicPathError(SessionError):
    pass


class InvalidTopicSpecificationError(SessionError):
    pass


class TopicLicenseLimitError(SessionError):
    pass


class IncompatibleExistingTopicError(SessionError):
    """
    This differs from ExistingTopicError as the reason is that
    the existing topic is owned by something that prevents the caller
    managing. The specification of the existing topic may be the same.
    """


class AddTopicError(SessionError):
    pass


class UnsatisfiedConstraintError(SessionError):
    """
    The exception to report a constraint was not satisfied.

    """


class ExclusiveUpdaterConflictError(SessionError):
    """
    The exception to indicate an update could not be applied because an exclusive update source
    is registered for the path.

    """


class InvalidPatchError(SessionError):
    """
    The exception to report that a JSON Patch was invalid.

    """


class FailedPatchError(SessionError):
    """
    The exception to report that applying a JSON Patch failed.

    Notes:
        This can happen if the topic's current value is not valid CBOR. See
        [VALIDATE_VALUES][diffusion.features.topics.details.topic_specification.TopicSpecification.VALIDATE_VALUES].

    """


class InvalidUpdateStreamError(SessionError):
    """
    The exception used to report an operation was performed with an invalid
    [UpdateStream][diffusion.UpdateStream].

    """


class NotATimeSeriesTopicError(SessionError):
    pass


class IncompatibleTopicStateError(SessionError):
    """
    The exception that indicates that an operation could not be performed because the topic is
    managed by a component (such as fan-out) that prohibits updates from the caller.

    """


class HandlerConflictError(SessionError):
    pass


class UnhandledMessageError(SessionError):
    pass


class NoSuchSessionError(SessionError):
    pass


class CancellationError(SessionError):
    pass


class RejectedRequestError(SessionError):
    pass


class InvalidQueryError(SessionError):
    """
    Exception used to report a query that is invalid for the time series.
    Notes:

        An example invalid query is one where the anchor is a sequence number
        beyond the end of the time series (for example, it is specified using
        <see cref="IRangeQuery{VT}.From(long)"/> with a sequence number
        greater than the latest sequence number, or <see cref="IRangeQuery{VT}.FromLast(long)"/>
        with a `count` greater than the number of events in the time series),
        and the span is a relative time. Since no timestamp is associated
        with the anchor, the range is meaningless.

    Added in version 6.9.
    """


class SessionClosedError(SessionError):
    """
    The exception indicating a [ISession][diffusion.session.Session] closure.

    Notes:
        No further operations are possible when this exception has been thrown.

    Added in 6.9
    """


class SessionSecurityError(SessionError):
    """
    The exception indicating that a [ISession][diffusion.session.Session] operation failed
    due to a security constraint.

    Notes:
        Repeating the operation with the same security credentials is likely to fail.

    Added in 6.9
    """


class FatalConnectionError(ProtocolError):
    """
    The exception indicating a connection has been rejected
    and should not be retried.

    Notes:
        This exception is never thrown directly
        but might be the cause of a
        [SessionError][diffusion.session.exceptions.SessionError]

    Added in 6.9
    """


class AuthenticationError(FatalConnectionError):
    """
    The connection exception representing an authentication failure.

    Notes:
        This exception is never thrown directly
        but might be the cause of a
        [SessionError][diffusion.session.exceptions.SessionError]

    Added in 6.9
    """


class ProxyAuthenticationError(ProtocolError):
    """
    The exception indicating that there was a problem during authentication
    with a proxy server.

    Notes:
        This exception is never thrown directly
        but might be the cause of a
        [SessionError][diffusion.session.exceptions.SessionError]


    Added in 6.9.
    """
