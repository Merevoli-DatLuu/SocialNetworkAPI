
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
/api/v1/user/friend/<user_id>                                # POST:   Gửi lời mời kết bạn
/api/v1/user/friend/<friend_id>/accept                       # PUT:    Đồng ý lời mời kết bạn
/api/v1/user/friend/<friend_id>/deny                         # DELETE: Từ chối lời mời kết bạn
/api/v1/user/friend/<friend_id>/cancel                       # DELETE: Hủy lời mời kết bạn
/api/v1/user/friend/<friend_id>                              # DELETE: Hủy kết bạn
/api/v1/user/friend/                                         # GET:    Xem danh sách bạn bè
/api/v1/user/friend/<user_id>                                # GET:    Xem danh sách bạn bè của người khác
/api/v1/user/friend/send-list                                # GET:    Xem danh sách lời mời đã gửi
/api/v1/user/friend/wait-list                                # GET:    Xem danh sách lời mời chờ xác nhận

UserFollower
---------------
/api/v1/user/follower/<int:user_id>                          # POST:   Theo dõi người dùng
/api/v1/user/follower/<int:user_id>                          # DELETE: Hủy theo dõi
/api/v1/user/follower/list-follower                          # GET:    Xem danh sách người dùng theo dõi
/api/v1/user/follower/list-following                         # GET:    Xem danh sách người dùng đang theo dõi

Group
--------
/api/v1/group                                                # POST:   Tạo group
/api/v1/group                                                # GET:    Xem danh sách group cua mình
/api/v1/group/joined                                         # GET:    Xem danh sách group mình tham gia
/api/v1/group/<group_id>                                     # GET:    Xem thông tin group
/api/v1/group/<group_id>                                     # PUT:    Sửa thông tin group
/api/v1/group/<group_id>                                     # DELETE: Xóa group
    
GroupFollower
----------------
/api/v1/group/<group_id>/follow                              # POST:   Theo dõi
/api/v1/group/<group_id>/follow                              # DELETE: Hủy theo dõi
/api/v1/group/<group_id>/follow/follower                     # GET:    Xem danh sách người dùng theo dõi
/api/v1/group/<group_id>/follow/following                    # GET:    Xem danh sách group đang theo dõi
    
GroupMember
---------------
/api/v1/group/<group_id>/member                              # POST:   Thêm thành viên
/api/v1/group/<group_id>/member                              # GET:    Xem thành viên
/api/v1/group/<group_id>/member/block                        # GET:    Xem thành viên bị chặn
/api/v1/group/<group_id>/member/<user_id>/block              # PUT:    Chặn thành viên
/api/v1/group/<group_id>/member/<user_id>/unblock            # PUT:    Hủy chặn thành viên
/api/v1/group/<group_id>/member/<user_id>/role               # PUT:    Thay đổi quyền của thành viên
/api/v1/group/<group_id>/member/<user_id>                    # DELETE: Xóa thành viên
    
GroupInvitation
------------------
/api/v1/group/<group_id>/invite                              # GET:    Xem danh sách lời mời    
/api/v1/group/<group_id>/invite/me                           # GET:    Xem danh sách group mình đã gửi lời mời
/api/v1/group/<group_id>/invite/<user_id>/accept             # PUT:    Xác nhận lời mời vào group
/api/v1/group/<group_id>/invite/<user_id>/deny               # DELETE: Từ chối lời mời vào group
/api/v1/group/<group_id>/invite                              # POST:   Gửi lời mời vào group
/api/v1/group/<group_id>/invite/cancel                       # DELETE: Hủy gửi lời mời vào group

PrivateMessage
------------------
/api/v1/message/                                             # GET:    Xem danh sách cuộc trò chuyện của mình
/api/v1/message/user/<user_id>                               # POST:   Tạo cuộc trò chuyện mới

PrivateMessageDetail
------------------
/api/v1/message/<message_id>                                 # GET:    Xem nội dung của 1 cuộc trò chuyện
/api/v1/message/<message_id>                                 # POST:   Gửi tin nhắn

GroupMessage
--------------
/api/v1/message/group/                                       # GET:    Xem danh sách cuộc trò chuyện của mình
/api/v1/message/group/                                       # POST:   Tạo cuộc trò chuyện mới

GroupMessageDetail
---------------------
/api/v1/message/group/<group_message_id>                     # GET:    Xem nội dung của 1 cuộc trò chuyện
/api/v1/message/group/<group_message_id>                     # POST:   Gửi tin nhắn

GroupMessageMember
---------------------
/api/v1/message/group/<group_message_id>/member              # GET:    Xem danh sách thành viên
/api/v1/message/group/<group_message_id>/member              # POST:   Thêm thành viên mới
/api/v1/message/group/<group_message_id>/member/<user_id>    # DELETE: Xóa thành viên
/api/v1/message/group/<group_message_id>/member/<user_id>    # PUT:    Cấp quyền thành viên

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

> + Yêu cầu đăng nhập trên `replit`
> + Kiểm tra xem pipenv đã được cài đặt chưa. Nếu rồi thì không cần cài đặt gì thêm

![](https://github.com/Merevoli-DatLuu/SocialNetworkAPI/blob/master/preview/demo.png)
-->
