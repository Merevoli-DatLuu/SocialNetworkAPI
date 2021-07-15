
<div align="center">

# SocialNetworkAPI
  
</div>

## API Diagrams

```
MODULES

User
------
/api/v1/user/register                        # POST: Register
/api/v1/user/verify-user                     # GET:  Verify User
/api/v1/user/login                           # POST: Login
/api/v1/user/change_password                 # POST: Change Password
/api/v1/user/reset-password                  # POST: Reset Password
/api/v1/user/reset-comfirm-password          # POST: Confirm Reset Password 
/api/v1/user/me                              # GET:  View Current User's Profile
/api/v1/user/<user_id>                       # GET:  View Specific User's Profile
/api/v1/user/                                # GET:  View All Users

Post
------
/api/v1/post/create                          # POST: Create A New Post
/api/v1/post/<post_id>                       # PUT: Update A Post
/api/v1/post/<post_id>                       # GET: View A Post
/api/v1/post/                                # GET: View All Posts Current User Can
/api/v1/post/<post_id>                       # DELETE: Delete A Post

Likepost
------------
/api/v1/like-post/<post_id>                  # POST: Like A Post
/api/v1/like-post/<post_id>                  # DELETE: Unlike A Post
/api/v1/like-post/<post_id>                  # GET: Get All User Liked

Comment
-----------
/api/v1/comment/<post_id>                    # POST: Comment A Post or A Comment
/api/v1/comment/<comment_id>                 # PUT: Update A Comment
/api/v1/comment/<comment_id>                 # DELETE: Delete A Comment
/api/v1/comment/<post_id>                    # GET: Get All Comments
/api/v1/comment/<post_id>/sub/<comment_id>   # GET: Get All Subcomments  
```
