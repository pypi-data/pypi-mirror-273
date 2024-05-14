from enum import Enum


class ApiErrorEnum(Enum):
    hit_frequency_limit = 'hit_frequency_limit'
    no_permission_to_access = 'no_permission_to_access'
    file_does_not_exist = 'file_does_not_exist'
