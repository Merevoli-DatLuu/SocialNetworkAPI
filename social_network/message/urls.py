from django.urls import path

from .views import (private_message_detail_list_send, private_message_list, private_message_create,
                    group_message_list_create, group_message_detail_list_send,
                    group_message_member_list_create, group_message_member_update_delete)

urlpatterns = [
    path('',                                                        private_message_list,                   name='private-message-detail-list-send'),
    path('user/<int:user_id>',                                      private_message_create,                 name='private-message-list'),
    path('<int:message_id>',                                        private_message_detail_list_send,       name='private-message-create'),
    
    path('group/',                                                  group_message_list_create,              name='group-message-list-create'),
    path('group/<int:group_message_id>',                            group_message_detail_list_send,         name='group-message-detail-list-send'),
    path('group/<int:group_message_id>/member',                     group_message_member_list_create,       name='group-message-member-list-create'),
    path('group/<int:group_message_id>/member/<int:user_id>',       group_message_member_update_delete,     name='group-message-member-update-delete'),
]