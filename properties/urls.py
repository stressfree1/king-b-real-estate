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
    #
    # Kept so existing templates/links do not break.
    # They now use the unified account system.
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
]