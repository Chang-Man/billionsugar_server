from rest_framework import exceptions, status


class BaseError(exceptions.APIException):
    pass


class FieldError(BaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '입력이 잘못 되었습니다.'
    default_code = 'E201'

class DuplicationError(BaseError):
    status_code = status.HTTP_409_CONFLICT
    default_detail = '이미 존재하는 값입니다.'
    default_code = 'E202'