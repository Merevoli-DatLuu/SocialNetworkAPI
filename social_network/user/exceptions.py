from rest_framework.exceptions import APIException

class FriendAlreadyAcceptException(APIException):
    status_code = 400
    default_detail = 'Bạn không thể chấp nhận lời mời khi đã là bạn bè'
    default_code = 'friend_already_accept'
    
class FriendAlreadyDenyException(APIException):
    status_code = 400
    default_detail = 'Bạn không thể từ chối lời mời khi đã là bạn bè'
    default_code = 'friend_already_deny'
    
class FriendAlreadyException(APIException):
    status_code = 400
    default_detail = 'Bạn không thể kết bạn khi chưa là bạn bè'
    default_code = 'friend_already'
    
class FriendNotYourException(APIException):
    status_code = 400
    default_detail = 'Đây không phải là lời mời của bạn'
    default_code = 'friend_not_your'