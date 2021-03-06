
<div align="center">

# SocialNetworkAPI
  
</div>

---

- [API Diagrams](#api-diagrams)
- [Database Diagram](#database-diagram)
- [Accounts](#accounts)
- [API Document](#api-document)

---

## API Diagrams

```
MODULES

User
------
/api/v1/user/register                                        # POST:   Register
/api/v1/user/verify-user                                     # GET:    Verify User
/api/v1/user/login                                           # POST:   Login
/api/v1/user/change_password                                 # POST:   Change Password
/api/v1/user/reset-password                                  # POST:   Reset Password
/api/v1/user/reset-comfirm-password                          # POST:   Confirm Reset Password 
/api/v1/user/me                                              # GET:    View Current User's Profile
/api/v1/user/<user_id>                                       # GET:    View Specific User's Profile
/api/v1/user/                                                # GET:    View All Users

Post
------
/api/v1/post/create                                          # POST:   Create A New Post
/api/v1/post/<post_id>                                       # PUT:    Update A Post
/api/v1/post/<post_id>                                       # GET:    View A Post
/api/v1/post/                                                # GET:    View All Posts Current User Can
/api/v1/post/<post_id>                                       # DELETE: Delete A Post

Likepost
------------
/api/v1/like-post/<post_id>                                  # POST:   Like A Post
/api/v1/like-post/<post_id>                                  # DELETE: Unlike A Post
/api/v1/like-post/<post_id>                                  # GET:    Get All User Liked

Comment
-----------
/api/v1/comment/<post_id>                                    # POST:   Comment A Post or A Comment
/api/v1/comment/<post_id>                                    # GET:    Get All Comments
/api/v1/comment/<post_id>/sub/<comment_id>                   # GET:    Get All Subcomments  
/api/v1/comment/<comment_id>                                 # PUT:    Update A Comment
/api/v1/comment/<comment_id>                                 # DELETE: Delete A Comment

Friend
---------
/api/v1/user/friend/<user_id>                                # POST:   G???i l???i m???i k???t b???n
/api/v1/user/friend/<friend_id>/accept                       # PUT:    ?????ng ?? l???i m???i k???t b???n
/api/v1/user/friend/<friend_id>/deny                         # DELETE: T??? ch???i l???i m???i k???t b???n
/api/v1/user/friend/<friend_id>/cancel                       # DELETE: H???y l???i m???i k???t b???n
/api/v1/user/friend/<friend_id>                              # DELETE: H???y k???t b???n
/api/v1/user/friend/                                         # GET:    Xem danh s??ch b???n b??
/api/v1/user/friend/<user_id>                                # GET:    Xem danh s??ch b???n b?? c???a ng?????i kh??c
/api/v1/user/friend/send-list                                # GET:    Xem danh s??ch l???i m???i ???? g???i
/api/v1/user/friend/wait-list                                # GET:    Xem danh s??ch l???i m???i ch??? x??c nh???n

UserFollower
---------------
/api/v1/user/follower/<int:user_id>                          # POST:   Theo d??i ng?????i d??ng
/api/v1/user/follower/<int:user_id>                          # DELETE: H???y theo d??i
/api/v1/user/follower/list-follower                          # GET:    Xem danh s??ch ng?????i d??ng theo d??i
/api/v1/user/follower/list-following                         # GET:    Xem danh s??ch ng?????i d??ng ??ang theo d??i

Group
--------
/api/v1/group                                                # POST:   T???o group
/api/v1/group                                                # GET:    Xem danh s??ch group cua m??nh
/api/v1/group/joined                                         # GET:    Xem danh s??ch group m??nh tham gia
/api/v1/group/<group_id>                                     # GET:    Xem th??ng tin group
/api/v1/group/<group_id>                                     # PUT:    S???a th??ng tin group
/api/v1/group/<group_id>                                     # DELETE: X??a group
    
GroupFollower
----------------
/api/v1/group/<group_id>/follow                              # POST:   Theo d??i
/api/v1/group/<group_id>/follow                              # DELETE: H???y theo d??i
/api/v1/group/<group_id>/follow/follower                     # GET:    Xem danh s??ch ng?????i d??ng theo d??i
/api/v1/group/<group_id>/follow/following                    # GET:    Xem danh s??ch group ??ang theo d??i
    
GroupMember
---------------
/api/v1/group/<group_id>/member                              # POST:   Th??m th??nh vi??n
/api/v1/group/<group_id>/member                              # GET:    Xem th??nh vi??n
/api/v1/group/<group_id>/member/block                        # GET:    Xem th??nh vi??n b??? ch???n
/api/v1/group/<group_id>/member/<user_id>/block              # PUT:    Ch???n th??nh vi??n
/api/v1/group/<group_id>/member/<user_id>/unblock            # PUT:    H???y ch???n th??nh vi??n
/api/v1/group/<group_id>/member/<user_id>/role               # PUT:    Thay ?????i quy???n c???a th??nh vi??n
/api/v1/group/<group_id>/member/<user_id>                    # DELETE: X??a th??nh vi??n
    
GroupInvitation
------------------
/api/v1/group/<group_id>/invite                              # GET:    Xem danh s??ch l???i m???i    
/api/v1/group/<group_id>/invite/me                           # GET:    Xem danh s??ch group m??nh ???? g???i l???i m???i
/api/v1/group/<group_id>/invite/<user_id>/accept             # PUT:    X??c nh???n l???i m???i v??o group
/api/v1/group/<group_id>/invite/<user_id>/deny               # DELETE: T??? ch???i l???i m???i v??o group
/api/v1/group/<group_id>/invite                              # POST:   G???i l???i m???i v??o group
/api/v1/group/<group_id>/invite/cancel                       # DELETE: H???y g???i l???i m???i v??o group

PrivateMessage
------------------
/api/v1/message/                                             # GET:    Xem danh s??ch cu???c tr?? chuy???n c???a m??nh
/api/v1/message/user/<user_id>                               # POST:   T???o cu???c tr?? chuy???n m???i

PrivateMessageDetail
------------------
/api/v1/message/<message_id>                                 # GET:    Xem n???i dung c???a 1 cu???c tr?? chuy???n
/api/v1/message/<message_id>                                 # POST:   G???i tin nh???n

GroupMessage
--------------
/api/v1/message/group/                                       # GET:    Xem danh s??ch cu???c tr?? chuy???n c???a m??nh
/api/v1/message/group/                                       # POST:   T???o cu???c tr?? chuy???n m???i

GroupMessageDetail
---------------------
/api/v1/message/group/<group_message_id>                     # GET:    Xem n???i dung c???a 1 cu???c tr?? chuy???n
/api/v1/message/group/<group_message_id>                     # POST:   G???i tin nh???n

GroupMessageMember
---------------------
/api/v1/message/group/<group_message_id>/member              # GET:    Xem danh s??ch th??nh vi??n
/api/v1/message/group/<group_message_id>/member              # POST:   Th??m th??nh vi??n m???i
/api/v1/message/group/<group_message_id>/member/<user_id>    # DELETE: X??a th??nh vi??n
/api/v1/message/group/<group_message_id>/member/<user_id>    # PUT:    C???p quy???n th??nh vi??n

```

## Database Diagram

![](https://github.com/Merevoli-DatLuu/SocialNetworkAPI/blob/master/preview/SQLDiagram_2.png)

<!--
## Accounts

| STT | email                   | password         | note  |
|-----|-------------------------|------------------|-------|
| 1   | admin@socialnetwork.com | socialnetwork123 | admin |
| 2   | datluu.1702@gmail.com   | 12345678aa       |       |
| 3   | qan86332@zwoho.com      | 123456789a       |       |

## API Document
[API Document](https://github.com/Merevoli-DatLuu/SocialNetworkAPI/wiki/API-Documentation-V1)


## Demo
[Demo](https://replit.com/join/odwfilaepm-merevolidatluu)

> + Y??u c???u ????ng nh???p tr??n `replit`
> + Ki???m tra xem pipenv ???? ???????c c??i ?????t ch??a. N???u r???i th?? kh??ng c???n c??i ?????t g?? th??m

![](https://github.com/Merevoli-DatLuu/SocialNetworkAPI/blob/master/preview/demo.png)
-->
