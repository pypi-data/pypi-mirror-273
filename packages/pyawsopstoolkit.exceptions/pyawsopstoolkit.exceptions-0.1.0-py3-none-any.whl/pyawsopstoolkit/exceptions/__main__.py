from typing import Optional, Union

from pyawsopstoolkit.exceptions.__validations__ import Validation


class AssumeRoleError(Exception):
    """
    The AssumeRoleError exception class is specifically designed for the AWS Ops Toolkit.
    It's raised when the assume role session fails.
    """

    def __init__(
            self,
            role_arn: str,
            exception: Optional[Exception] = None
    ) -> None:
        """
        Constructor for the AssumeRoleError class.
        :param role_arn: The Amazon Resource Name (ARN) of the role.
        :type role_arn: str
        :param exception: The exception that occurred, if any.
        :type exception: Exception
        """
        Validation.validate_type(role_arn, str, 'role_arn should be a string.')
        Validation.validate_type(exception, Union[Exception, None], 'exception should be of Exception type.')

        self._role_arn = role_arn
        self._exception = exception
        self._message = f'ERROR: Unable to assume role "{role_arn}".{f" {exception}." if exception else ""}'
        super().__init__(self._message)

    @property
    def role_arn(self) -> str:
        """
        Getter for role_arn attribute.
        :return: The Amazon Resource Name (ARN) of the role.
        :rtype: str
        """
        return self._role_arn

    @property
    def exception(self) -> Optional[Exception]:
        """
        Getter for exception attribute.
        :return: The exception that occurred, if any.
        :rtype: Exception
        """
        return self._exception

    @property
    def message(self) -> str:
        """
        Getter for message attribute.
        :return: The error message.
        :rtype: str
        """
        return self._message
