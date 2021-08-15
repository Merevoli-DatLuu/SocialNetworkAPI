from django.urls import path

from .views import (group_list, group_list_joined, group_detail,
                    group_follower_change, group_follower_list_follower,
                    group_follower_list_following, group_member_list, 
                    group_member_list_blocked, group_member_delete,
                    group_member_block, group_member_unblock,
                    group_member_role, group_invitation_list_send,
                    group_invitation_list_inviting, group_invitation_accept,
                    group_invitation_deny, group_invitation_cancel)

urlpatterns = [
    path('',                                        group_list,                     name='group-list'),
    path('joined',                                  group_list_joined,              name='group-list-joined'),
    path('<int:pk>',                                group_detail,                   name='group-detail'),
    
    path('<int:pk>/follow',                         group_follower_change,          name='group-follower-change'),
    path('<int:pk>/follow/follower',                group_follower_list_follower,   name='group-follower-list-follower'),
    path('<int:pk>/follow/following',               group_follower_list_following,  name='group-follower-list-following'),
    
    path('<int:pk>/member',                         group_member_list,              name='group-member-list'),
    path('<int:pk>/member/blocked',                 group_member_list_blocked,      name='group-member-list-blocked'),
    path('<int:pk>/member/<int:user_id>',           group_member_delete,            name='group-member-delete'),
    path('<int:pk>/member/<int:user_id>/block',     group_member_block,             name='group-member-block'),
    path('<int:pk>/member/<int:user_id>/unblock',   group_member_unblock,           name='group-member-unblock'),
    path('<int:pk>/member/<int:user_id>/role',      group_member_role,              name='group-member-role'),

    path('<int:pk>/invite',                         group_invitation_list_send,     name='group-member-role'),
    path('<int:pk>/invite/me',                      group_invitation_list_inviting, name='group-member-role'),
    path('<int:pk>/invite/<int:user_id>/accept',    group_invitation_accept,        name='group-member-role'),
    path('<int:pk>/invite/<int:user_id>/deny',      group_invitation_deny,          name='group-member-role'),
    path('<int:pk>/invite/cancel',                  group_invitation_cancel,        name='group-member-role'),
]