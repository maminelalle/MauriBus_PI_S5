from django.urls import path
from . import views

app_name = "mauribus_app"

urlpatterns = [
    # API Authentication endpoints for mobile
    path("api/auth/register/", views.api_auth_register, name="api_auth_register"),
    path("api/auth/login/", views.api_auth_login, name="api_auth_login"),
    # Admin dashboard
    path("admin/dashboard/", views.dashboard, name="dashboard"),
    # Admin authentication
    path("login/", views.admin_login, name="login"),
    path("logout/", views.admin_logout, name="logout"),
    # API Data endpoints for mobile
    path("api/lines/", views.api_lines, name="api_lines"),
    path("api/trips/", views.api_trips, name="api_trips"),
    path("api/user/profile/", views.api_user_profile, name="api_user_profile"),
    

    # Admin views
    path("drivers/", views.driver_list, name="driver_list"),
    path("users/", views.user_list, name="user_list"),
    # Driver interface
    path("driver/login/", views.driver_login, name="driver_login"),
    path("driver/logout/", views.driver_logout, name="driver_logout"),
    path("driver/dashboard/", views.driver_dashboard, name="driver_dashboard"),
    path("driver/trips/", views.driver_trips, name="driver_trips"),
    path("driver/action/", views.driver_action, name="driver_action"),
    path("driver/buses/", views.driver_buses, name="driver_buses"),
    path("driver/lines/", views.driver_lines, name="driver_lines"),
    path("driver/profile/", views.driver_profile, name="driver_profile"),
    path("driver/notifications/", views.driver_notifications, name="driver_notifications"),
    path("driver/messages/", views.driver_messages, name="driver_messages"),
    # Citizen interface
    path("citizen/login/", views.citizen_login, name="citizen_login"),
    path("citizen/register/", views.citizen_register, name="citizen_register"),
    path("citizen/logout/", views.citizen_logout, name="citizen_logout"),
    path("citizen/dashboard/", views.citizen_dashboard, name="citizen_dashboard"),
    path("citizen/lines/", views.citizen_lines, name="citizen_lines"),
    path("citizen/trips/", views.citizen_trips, name="citizen_trips"),
    path("citizen/trips/<int:trip_id>/", views.citizen_trip_detail, name="citizen_trip_detail"),
    path("citizen/profile/", views.citizen_profile, name="citizen_profile"),
    # Admin message management
    path("admin/messages/", views.admin_messages, name="admin_messages"),
    path("admin/send_message/", views.admin_send_message, name="admin_send_message"),
    path("admin/line/set_points/", views.admin_set_line_points, name="admin_set_line_points"),
    path("buses/<int:bus_id>/delete/", views.bus_delete, name="bus_delete"),
    path("lines/<int:line_id>/delete/", views.line_delete, name="line_delete"),
    path("trips/<int:trip_id>/delete/", views.trip_delete, name="trip_delete"),
    path("drivers/<int:driver_id>/delete/", views.driver_delete, name="driver_delete"),
    path("users/<int:user_id>/delete/", views.user_delete, name="user_delete"),
    path("buses/", views.bus_list, name="bus_list"),
 
    path("lines/", views.line_list, name="line_list"),
    path("trips/", views.trip_list, name="trip_list"),
    path("messages/", views.admin_messages, name="message_list"),

]
