from django.urls import path
from . import views


urlpatterns = [

    # =========================================================
    # HOME
    # =========================================================

    path(
        '',
        views.home,
        name='home'
    ),


    # =========================================================
    # GENERAL ACCOUNT
    # =========================================================

    path(
        'register/',
        views.site_register,
        name='site_register'
    ),

    path(
        'login/',
        views.site_login,
        name='site_login'
    ),

    path(
        'logout/',
        views.site_logout,
        name='site_logout'
    ),


    # =========================================================
    # GENERAL ACCOUNT DASHBOARD
    # =========================================================

    path(
        'account/dashboard/',
        views.marketplace_dashboard,
        name='marketplace_dashboard'
    ),

    path(
        'marketplace/sell/',
        views.marketplace_create,
        name='marketplace_create'
    ),


    # =========================================================
    # ACCOUNT SETTINGS
    # =========================================================

    path(
        'account/settings/',
        views.account_settings,
        name='account_settings'
    ),

    path(
        'account/password/change/',
        views.AccountPasswordChangeView.as_view(),
        name='password_change'
    ),


    # =========================================================
    # CUSTOMER PROFILE
    # =========================================================

    path(
        'account/customer/',
        views.customer_profile_edit,
        name='customer_profile_edit'
    ),


    # =========================================================
    # BECOME SKILLED WORKER
    # =========================================================

    path(
        'account/become-worker/',
        views.become_skilled_worker,
        name='become_skilled_worker'
    ),


    # =========================================================
    # MY WORKER PROFILE
    # =========================================================

    path(
        'account/worker-profile/',
        views.my_worker_profile,
        name='my_worker_profile'
    ),


    # =========================================================
    # MARKETPLACE
    # =========================================================

    path(
        'marketplace/',
        views.marketplace,
        name='marketplace'
    ),

    path(
        'marketplace/my-listing/<int:listing_id>/edit/',
        views.marketplace_edit,
        name='marketplace_edit'
    ),
    # =========================================================
    # MARKETPLACE LISTING DETAIL
    # =========================================================

    path(
        'marketplace/<int:listing_id>/',
        views.marketplace_detail,
        name='marketplace_detail'
    ),


    # =========================================================
    # MY MARKETPLACE LISTING
    # =========================================================

    path(
        'marketplace/my-listing/<int:listing_id>/',
        views.my_listing_detail,
        name='my_listing_detail'
    ),


    # =========================================================
    # PROPERTIES / ESTATES
    # =========================================================

    path(
        'properties/',
        views.estate_list,
        name='property_list'
    ),

    path(
        'properties/estate/<int:estate_id>/',
        views.estate_detail,
        name='estate_detail'
    ),

    path(
        'properties/estate/<int:estate_id>/type/<int:estate_type_id>/',
        views.estate_type_detail,
        name='estate_type_detail'
    ),

    path(
        'properties/<int:property_id>/',
        views.property_detail,
        name='property_detail'
    ),


    # =========================================================
    # ABOUT
    # =========================================================

    path(
        'about/',
        views.about,
        name='about'
    ),


    # =========================================================
    # OUR SERVICES
    # =========================================================

    path(
        'our-services/',
        views.our_services,
        name='our_services'
    ),


    # =========================================================
    # JOBS
    # =========================================================

    path(
        'jobs/',
        views.jobs,
        name='jobs'
    ),

    path(
        'jobs/<int:job_id>/',
        views.job_detail,
        name='job_detail'
    ),

    path(
        'jobs/<int:job_id>/apply/',
        views.job_apply,
        name='job_apply'
    ),


    # =========================================================
    # CONTACT
    # =========================================================

    path(
        'contact/',
        views.contact,
        name='contact'
    ),


    # =========================================================
    # PUBLIC SKILLED WORKERS
    # =========================================================

    path(
        'skilled-workers/',
        views.skilled_workers,
        name='skilled_workers'
    ),

    path(
        'skilled-workers/<int:worker_id>/',
        views.skilled_worker_profile,
        name='skilled_worker_profile'
    ),

    path(
        'skilled-workers/<int:worker_id>/hire/',
        views.worker_hire,
        name='worker_hire'
    ),


    # =========================================================
    # WORKER DASHBOARD
    # =========================================================

    path(
        'skilled-workers/dashboard/',
        views.worker_dashboard,
        name='worker_dashboard'
    ),


    # =========================================================
    # CUSTOMER PROFILE VIEWED BY WORKER
    # =========================================================

    path(
        'skilled-workers/customer/<int:customer_id>/',
        views.customer_profile,
        name='customer_profile'
    ),


    # =========================================================
    # WORKER HIRE ACTIONS
    # =========================================================

    path(
        'skilled-workers/hire/<int:hire_id>/accept/',
        views.accept_worker_hire,
        name='accept_worker_hire'
    ),

    path(
        'skilled-workers/hire/<int:hire_id>/decline/',
        views.decline_worker_hire,
        name='decline_worker_hire'
    ),

    path(
        'skilled-workers/hire/<int:hire_id>/complete/',
        views.complete_worker_hire,
        name='complete_worker_hire'
    ),


    # =========================================================
    # CUSTOMER REVIEWS WORKER
    # =========================================================

    path(
        'worker-hire/<int:hire_id>/review/',
        views.worker_review,
        name='worker_review'
    ),

    path(
        'worker-hire/<int:hire_id>/review/create/',
        views.worker_review,
        name='worker_review_create'
    ),


    # =========================================================
    # WORKER REVIEWS CUSTOMER
    # =========================================================

    path(
        'skilled-workers/hire/<int:hire_id>/review-customer/',
        views.customer_review,
        name='customer_review'
    ),


    # =========================================================
    # OLD CUSTOMER ROUTES
    # =========================================================

    path(
        'customer/register/',
        views.customer_register,
        name='customer_register'
    ),

    path(
        'customer/login/',
        views.customer_login,
        name='customer_login'
    ),

    path(
        'customer/logout/',
        views.customer_logout,
        name='customer_logout'
    ),

    path(
        'customer/dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

    path(
        'customer/hire/<int:hire_id>/cancel/',
        views.cancel_worker_hire,
        name='cancel_worker_hire'
    ),


    # =========================================================
    # OLD SKILLED WORKER ROUTES
    # =========================================================

    path(
        'skilled-workers/register/',
        views.skilled_worker_register,
        name='skilled_worker_register'
    ),

    path(
        'skilled-workers/login/',
        views.skilled_worker_login,
        name='skilled_worker_login'
    ),

    path(
        'skilled-workers/logout/',
        views.skilled_worker_logout,
        name='skilled_worker_logout'
    ),


    # =========================================================
    # SKILLED WORKER PASSWORD RESET
    # =========================================================

    path(
        'skilled-workers/password-reset/',
        views.SkilledWorkerPasswordResetView.as_view(),
        name='worker_password_reset'
    ),

    path(
        'skilled-workers/password-reset/done/',
        views.SkilledWorkerPasswordResetDoneView.as_view(),
        name='worker_password_reset_done'
    ),

    path(
        'skilled-workers/password-reset/confirm/<uidb64>/<token>/',
        views.SkilledWorkerPasswordResetConfirmView.as_view(),
        name='worker_password_reset_confirm'
    ),

    path(
        'skilled-workers/password-reset/complete/',
        views.SkilledWorkerPasswordResetCompleteView.as_view(),
        name='worker_password_reset_complete'
    ),


    # =========================================================
    # GENERAL MARKETPLACE USER DASHBOARD
    # =========================================================

    path(
        'marketplace/user-dashboard/',
        views.marketplace_dashboard,
        name='marketplace_seller_dashboard'
    ),


    # =========================================================
    # MARKETPLACE SELLER DASHBOARD
    # =========================================================

    path(
        'marketplace/seller-dashboard/',
        views.marketplace_seller_dashboard,
        name='seller_dashboard'
    ),


    # =========================================================
    # MARKETPLACE SELLER REVIEW
    # =========================================================

    path(
        'marketplace/<int:listing_id>/review-seller/',
        views.marketplace_review_seller,
        name='marketplace_review_seller'
    ),


    # =========================================================
    # MARKETPLACE SELLER PROFILE
    # =========================================================

    path(
        'marketplace/seller/<int:seller_id>/',
        views.marketplace_seller_profile,
        name='marketplace_seller_profile'
    ),


    # =========================================================
    # MARKETPLACE CHAT
    # =========================================================

    # ---------------------------------------------------------
    # BUYER CHAT
    #
    # Example:
    # /marketplace/1/chat/
    #
    # A buyer uses this to chat with the seller of listing #1.
    # ---------------------------------------------------------

    path(
        'marketplace/<int:listing_id>/chat/',
        views.marketplace_chat,
        name='marketplace_chat'
    ),


    # ---------------------------------------------------------
    # SELLER CHAT WITH SPECIFIC BUYER
    #
    # Example:
    # /marketplace/1/chat/7/
    #
    # Seller of listing #1 is chatting with buyer/user #7.
    # ---------------------------------------------------------

    path(
        'marketplace/<int:listing_id>/chat/<int:buyer_id>/',
        views.marketplace_chat,
        name='marketplace_chat_with_buyer'
    ),


    # =========================================================
    # UNIFIED MARKETPLACE MESSAGES
    # =========================================================

    path(
        'marketplace/messages/',
        views.marketplace_messages,
        name='marketplace_messages'
    ),
    path(
        'marketplace/my-listing/<int:listing_id>/edit/',
        views.marketplace_edit,
        name='marketplace_edit'
    ),

   path(
        'my-listing/<int:listing_id>/delete-photo/<int:photo_id>/',
        views.marketplace_delete_photo,
        name='marketplace_delete_photo'
    ),

   path(
        "marketplace/my-listing/<int:listing_id>/delete-main-photo/",
        views.marketplace_delete_main_photo,
        name="marketplace_delete_main_photo",
    ),


# =========================================================
# GENERAL ACCOUNT PASSWORD RESET
# =========================================================

    path(
        'account/password-reset/',
        views.AccountPasswordResetView.as_view(),
        name='account_password_reset'
    ),

    path(
        'account/password-reset/done/',
        views.AccountPasswordResetDoneView.as_view(),
        name='account_password_reset_done'
    ),

    path(
        'account/password-reset/confirm/<uidb64>/<token>/',
        views.AccountPasswordResetConfirmView.as_view(),
        name='account_password_reset_confirm'
    ),

    path(
        'account/password-reset/complete/',
        views.AccountPasswordResetCompleteView.as_view(),
        name='account_password_reset_complete'
    ),

    path(
        'verify-email/<uidb64>/<token>/',
        views.verify_email,
        name='verify_email'
    ),

    path(
        'worker/messages/<int:hire_id>/',
        views.worker_messages,
        name='worker_messages',
    ),

    path(
        "terms-and-conditions/", 
        views.terms_and_conditions, 
        name="terms_and_conditions"
    ),

    path(
        'worker/messages/<int:hire_id>/',
        views.worker_messages,
        name='worker_messages'
    ),

    path(
        'skilled-workers/edit/',
        views.edit_worker_profile,
        name='skilled_worker_edit'
    ),

    path(
        'account/worker/profile/delete/',
        views.delete_worker_profile,
        name='skilled_worker_delete'
    ),

    path(
        'marketplace/delete/<int:listing_id>/',
        views.delete_marketplace_listing,
        name='marketplace_delete_listing'
    ),

    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),

    path(
        'notifications/<int:notification_id>/read/',
        views.mark_notification_read,
        name='mark_notification_read'
    ),

    path(
        'notifications/mark-all-read/',
        views.mark_all_notifications_read,
        name='mark_all_notifications_read'
    ),
]