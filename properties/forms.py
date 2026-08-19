from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from .models import (
    JobApplicant,
    ContactMessage,
    SkilledWorker,
    Customer,
    MarketplaceListing,
)


# =========================================================
# GENERAL ACCOUNT REGISTRATION
# =========================================================
#
# This is the ONLY form used to create the main King B
# account.
#
# The user creates ONE account with:
#   - Full name
#   - Email
#   - Phone
#   - Password
#
# After registration, the account automatically receives
# a Customer profile.
#
# Later, the same account can apply to become a Skilled
# Worker without creating another User account.
# =========================================================

class AccountRegistrationForm(forms.Form):

    full_name = forms.CharField(
        label='Full Name',
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your full name',
                'class': 'customer-input',
                'autocomplete': 'name',
            }
        )
    )

    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
                'class': 'customer-input',
                'autocomplete': 'email',
            }
        )
    )

    phone = forms.CharField(
        label='Phone Number',
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your phone number',
                'class': 'customer-input',
                'autocomplete': 'tel',
            }
        )
    )

    password = forms.CharField(
        label='Create Password',
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Create a password',
                'class': 'customer-input',
                'autocomplete': 'new-password',
            }
        )
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
                'class': 'customer-input',
                'autocomplete': 'new-password',
            }
        )
    )

    def clean_email(self):

        email = self.cleaned_data.get(
            'email'
        )

        if email:

            email = email.strip().lower()

            if User.objects.filter(
                username__iexact=email
            ).exists():

                raise forms.ValidationError(
                    'An account with this email already exists. '
                    'Please log in instead.'
                )

        return email

    def clean_password(self):

        password = self.cleaned_data.get(
            'password'
        )

        if password and len(password) < 8:

            raise forms.ValidationError(
                'Password must be at least 8 characters long.'
            )

        return password

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            'password'
        )

        confirm_password = cleaned_data.get(
            'confirm_password'
        )

        if (
            password
            and confirm_password
            and password != confirm_password
        ):

            self.add_error(
                'confirm_password',
                'Passwords do not match.'
            )

        return cleaned_data


# =========================================================
# MULTIPLE IMAGE UPLOAD
# =========================================================

class MultipleFileInput(
    forms.ClearableFileInput
):

    allow_multiple_selected = True


class MultipleFileField(
    forms.FileField
):

    widget = MultipleFileInput

    def clean(
        self,
        data,
        initial=None
    ):

        single_file_clean = super().clean

        if not data:

            return []

        if isinstance(
            data,
            (list, tuple)
        ):

            return [
                single_file_clean(
                    file,
                    initial
                )
                for file in data
            ]

        return [
            single_file_clean(
                data,
                initial
            )
        ]


# =========================================================
# JOB APPLICATION
# =========================================================

class JobApplicationForm(forms.ModelForm):

    class Meta:

        model = JobApplicant

        fields = [
            'full_name',
            'phone',
            'email',
            'skill',
            'years_of_experience',
            'id_type',
            'id_number',
            'id_document',
            'cv',
        ]

        widgets = {

            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your full name'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your phone number'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email address'
                }
            ),

            'skill': forms.TextInput(
                attrs={
                    'placeholder': (
                        'e.g. Plumbing, Electrical, Sales'
                    )
                }
            ),

            'years_of_experience': forms.NumberInput(
                attrs={
                    'min': 0,
                    'placeholder': 'Years of experience'
                }
            ),

            'id_number': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your ID number'
                }
            ),
        }


# =========================================================
# CONTACT MESSAGE
# =========================================================

class ContactMessageForm(forms.ModelForm):

    class Meta:

        model = ContactMessage

        fields = [
            'name',
            'email',
            'phone',
            'subject',
            'message',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Your full name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Your email address'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Your phone number'
                }
            ),

            'subject': forms.TextInput(
                attrs={
                    'placeholder': 'What is this about?'
                }
            ),

            'message': forms.Textarea(
                attrs={
                    'placeholder': 'How can we help you?',
                    'rows': 6
                }
            ),
        }


# =========================================================
# SKILLED WORKER PROFILE
# =========================================================
#
# IMPORTANT:
#
# This form DOES NOT create a Django User.
#
# The user is already logged in and already has a general
# King B account.
#
# The existing User is attached to the SkilledWorker profile
# in the view using:
#
#     worker.user = request.user
#
# =========================================================

class SkilledWorkerRegistrationForm(
    forms.ModelForm
):

    class Meta:

        model = SkilledWorker

        fields = [
            'full_name',
            'phone',
            'email',
            'skill',
            'years_of_experience',
            'location',
            'description',
            'services',
            'profile_image',
            'id_type',
            'id_number',
            'id_document',
            'cv',
            'availability',
        ]

        widgets = {

            'full_name': forms.TextInput(
                attrs={
                    'placeholder': (
                        'Enter your full name'
                    ),
                    'class': 'customer-input',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': (
                        'Enter your phone number'
                    ),
                    'class': 'customer-input',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': (
                        'Enter your email address'
                    ),
                    'class': 'customer-input',
                }
            ),

            'skill': forms.TextInput(
                attrs={
                    'placeholder': (
                        'e.g. Electrician, Plumber, Carpenter'
                    ),
                    'class': 'customer-input',
                }
            ),

            'years_of_experience': forms.NumberInput(
                attrs={
                    'min': 0,
                    'placeholder': (
                        'Years of experience'
                    ),
                    'class': 'customer-input',
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': (
                        'e.g. Port Harcourt, Rivers State'
                    ),
                    'class': 'customer-input',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': (
                        'Tell people about your '
                        'experience and expertise...'
                    ),
                    'class': 'customer-input',
                }
            ),

            'services': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': (
                        'List the services you provide...'
                    ),
                    'class': 'customer-input',
                }
            ),

            'availability': forms.Select(
                attrs={
                    'class': 'customer-input',
                }
            ),

            'id_type': forms.Select(
                attrs={
                    'class': 'customer-input',
                }
            ),

            'id_number': forms.TextInput(
                attrs={
                    'placeholder': (
                        'Enter your ID number'
                    ),
                    'class': 'customer-input',
                }
            ),

            'id_document': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': (
                        '.jpg,.jpeg,.png,.pdf'
                    ),
                }
            ),

            'profile_image': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': (
                        '.jpg,.jpeg,.png'
                    ),
                }
            ),

            'cv': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': (
                        '.pdf,.doc,.docx'
                    ),
                }
            ),
        }

    def __init__(
        self,
        *args,
        current_user=None,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        # Store the existing logged-in account.
        #
        # This is used by clean_email() so the user's own
        # email is allowed.
        self.current_user = current_user

        # Existing worker profile:
        # ID document is no longer required.
        if self.instance and self.instance.pk:

            self.fields[
                'id_document'
            ].required = False

    def clean_email(self):

        email = self.cleaned_data.get(
            'email'
        )

        if not email:

            return email

        email = email.strip().lower()

        # -------------------------------------------------
        # EXISTING LOGGED-IN USER
        # -------------------------------------------------
        #
        # The current user's own email is allowed.
        #
        if (
            self.current_user
            and self.current_user.email
            and self.current_user.email.strip().lower() == email
        ):

            return email

        # -------------------------------------------------
        # OTHER ACCOUNT
        # -------------------------------------------------

        if User.objects.filter(
            username__iexact=email
        ).exists():

            raise forms.ValidationError(
                'This email already belongs to another account.'
            )

        return email

    def clean_id_type(self):

        id_type = self.cleaned_data.get(
            'id_type'
        )

        if not id_type:

            raise forms.ValidationError(
                'Please select an identification type.'
            )

        return id_type

    def clean_id_number(self):

        id_number = self.cleaned_data.get(
            'id_number'
        )

        if not id_number:

            raise forms.ValidationError(
                'Please enter your ID number.'
            )

        return id_number.strip()

    def clean_id_document(self):

        id_document = self.cleaned_data.get(
            'id_document'
        )

        # New worker application requires ID document.
        if (
            not id_document
            and not self.instance.pk
        ):

            raise forms.ValidationError(
                'Please upload a copy of your '
                'identification document.'
            )

        return id_document


# =========================================================
# CUSTOMER PROFILE
# =========================================================
#
# This form DOES NOT create a User.
#
# It creates or updates a Customer profile attached to
# the existing general King B account.
#
# =========================================================

class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [
            'full_name',
            'phone',
            'email',
            'address',
            'id_type',
            'id_number',
            'id_document',
        ]

        widgets = {

            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Full Name',
                    'class': 'customer-input',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Phone Number',
                    'class': 'customer-input',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email Address',
                    'class': 'customer-input',
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Address',
                    'class': 'customer-input',
                }
            ),

            'id_type': forms.Select(
                attrs={
                    'class': 'customer-input',
                }
            ),

            'id_number': forms.TextInput(
                attrs={
                    'placeholder': 'ID Number',
                    'class': 'customer-input',
                }
            ),

            'id_document': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': (
                        '.jpg,.jpeg,.png,.pdf'
                    ),
                }
            ),
        }

    def __init__(
        self,
        *args,
        **kwargs
    ):

        super().__init__(
            *args,
            **kwargs
        )

        # Existing customer does not need to upload ID again.
        if self.instance and self.instance.pk:

            self.fields[
                'id_document'
            ].required = False

    def clean_id_type(self):

        id_type = self.cleaned_data.get(
            'id_type'
        )

        # When editing an existing verified profile,
        # allow the previous value to remain.
        if not id_type:

            if self.instance and self.instance.pk:
                return self.instance.id_type

            raise forms.ValidationError(
                'Please select an identification type.'
            )

        return id_type

    def clean_id_number(self):

        id_number = self.cleaned_data.get(
            'id_number'
        )

        # When editing an existing profile, preserve it.
        if not id_number:

            if self.instance and self.instance.pk:
                return self.instance.id_number

            raise forms.ValidationError(
                'Please enter your ID number.'
            )

        return id_number.strip()

    def clean_id_document(self):

        id_document = self.cleaned_data.get(
            'id_document'
        )

        # Existing customer:
        # keep the old document when no new file is selected.
        if (
            not id_document
            and self.instance
            and self.instance.pk
        ):

            return self.instance.id_document

        if not id_document:

            raise forms.ValidationError(
                'Please upload a copy of your '
                'identification document.'
            )

        return id_document


# =========================================================
# SKILLED WORKER PASSWORD RESET
# =========================================================

class SkilledWorkerPasswordResetForm(
    PasswordResetForm
):

    def get_users(
        self,
        email
    ):

        email = email.strip().lower()

        users = User.objects.filter(
            email__iexact=email,
            is_active=True,
            skilled_worker_profile__isnull=False,
        )

        for user in users:

            if user.has_usable_password():

                yield user


# =========================================================
# MARKETPLACE LISTING
# =========================================================

class MarketplaceListingForm(
    forms.ModelForm
):

    images = MultipleFileField(
        required=True,
        widget=MultipleFileInput(
            attrs={
                'class': 'marketplace-file-input',
                'accept': (
                    'image/jpeg,'
                    'image/png,'
                    'image/webp'
                ),
                'multiple': True,
            }
        ),
        label='Item Photos'
    )

    class Meta:

        model = MarketplaceListing

        fields = [
            'title',
            'category',
            'price',
            'location',
            'description',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'What are you selling?'
                    ),
                    'autocomplete': 'off',
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter price',
                    'min': '0',
                    'step': '0.01',
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Where is the item located?'
                    ),
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Describe the item, its condition, '
                        'features and other important information.'
                    ),
                    'rows': 7,
                }
            ),
        }

    def clean_images(self):

        images = self.cleaned_data.get(
            'images'
        )

        if not images:

            raise forms.ValidationError(
                'Please upload at least 4 photos of your item.'
            )

        if len(images) < 4:

            raise forms.ValidationError(
                f'Please upload at least 4 photos. '
                f'You currently selected {len(images)}.'
            )

        if len(images) > 10:

            raise forms.ValidationError(
                'You can upload a maximum of 10 photos.'
            )

        allowed_types = {
            'image/jpeg',
            'image/png',
            'image/webp',
        }

        for image in images:

            if image.content_type not in allowed_types:

                raise forms.ValidationError(
                    f'{image.name} is not a supported '
                    'image format. Please use JPG, PNG or WEBP.'
                )

            if image.size > 5 * 1024 * 1024:

                raise forms.ValidationError(
                    f'{image.name} is too large. '
                    'Each image must be less than 5MB.'
                )

        return images