from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from .models import (
    AccountSettings,
    JobApplicant,
    ContactMessage,
    SkilledWorker,
    Customer,
    MarketplaceListing,
    MarketplaceReview,
)


# =========================================================
# GENERAL ACCOUNT REGISTRATION
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
    
    terms_agreed = forms.BooleanField(
    required=True,
    error_messages={
        'required': (
            'You must agree to the Terms & Conditions '
            'before creating your account.'
        )
    }
)
    
    
    

    def clean_email(self):

        email = self.cleaned_data.get('email')

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

        password = self.cleaned_data.get('password')

        if password and len(password) < 8:

            raise forms.ValidationError(
                'Password must be at least 8 characters long.'
            )

        return password

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

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

class MultipleFileInput(forms.ClearableFileInput):

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    widget = MultipleFileInput

    def clean(self, data, initial=None):

        if not data:
            return []

        if not isinstance(data, (list, tuple)):

            data = [data]

        cleaned_files = []

        for file in data:

            cleaned_file = super().clean(
                file,
                initial
            )

            cleaned_files.append(
                cleaned_file
            )

        return cleaned_files


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

class SkilledWorkerRegistrationForm(forms.ModelForm):

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
                    'placeholder': 'Enter your full name',
                    'class': 'customer-input',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your phone number',
                    'class': 'customer-input',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter your email address',
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
                    'placeholder': 'Years of experience',
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
                    'placeholder': 'Enter your ID number',
                    'class': 'customer-input',
                }
            ),

            'id_document': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': '.jpg,.jpeg,.png,.pdf',
                }
            ),

            'profile_image': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': '.jpg,.jpeg,.png',
                }
            ),

            'cv': forms.ClearableFileInput(
                attrs={
                    'class': 'customer-file',
                    'accept': '.pdf,.doc,.docx',
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

        self.current_user = current_user

        if self.instance and self.instance.pk:

            self.fields[
                'id_document'
            ].required = False

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if not email:
            return email

        email = email.strip().lower()

        if (
            self.current_user
            and self.current_user.email
            and self.current_user.email.strip().lower() == email
        ):

            return email

        if User.objects.filter(
            username__iexact=email
        ).exists():

            raise forms.ValidationError(
                'This email already belongs to another account.'
            )

        return email

    def clean_id_type(self):

        id_type = self.cleaned_data.get('id_type')

        if not id_type:

            raise forms.ValidationError(
                'Please select an identification type.'
            )

        return id_type

    def clean_id_number(self):

        id_number = self.cleaned_data.get('id_number')

        if not id_number:

            raise forms.ValidationError(
                'Please enter your ID number.'
            )

        return id_number.strip()

    def clean_id_document(self):

        id_document = self.cleaned_data.get('id_document')

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
                    'accept': '.jpg,.jpeg,.png,.pdf',
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )

        if self.instance and self.instance.pk:

            self.fields[
                'id_document'
            ].required = False

    def clean_id_type(self):

        id_type = self.cleaned_data.get('id_type')

        if not id_type:

            if self.instance and self.instance.pk:
                return self.instance.id_type

            raise forms.ValidationError(
                'Please select an identification type.'
            )

        return id_type

    def clean_id_number(self):

        id_number = self.cleaned_data.get('id_number')

        if not id_number:

            if self.instance and self.instance.pk:
                return self.instance.id_number

            raise forms.ValidationError(
                'Please enter your ID number.'
            )

        return id_number.strip()

    def clean_id_document(self):

        id_document = self.cleaned_data.get('id_document')

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

    def get_users(self, email):

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
class MarketplaceListingForm(forms.ModelForm):

    # -----------------------------------------------------
    # MULTIPLE PHOTOS
    # -----------------------------------------------------

    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                'class': 'marketplace-file-input',
                'accept': 'image/jpeg,image/png,image/webp',
                'multiple': True,
            }
        ),
        label='Item Photos'
    )

    class Meta:

        model = MarketplaceListing

        fields = [
            # Basic information
            'title',
            'category',
            'subcategory',
            'condition',

            # Pricing
            'price',
            'price_type',
            'negotiable',

            # Location
            'state',
            'city',
            'specific_location',

            # Product information
            'brand',
            'model',
            'year',
            'color',
            'quantity',

            # Description
            'description',

            # Seller preferences
            'contact_phone',
            'whatsapp_available',
            'delivery_available',
        ]

        widgets = {

            # =================================================
            # BASIC INFORMATION
            # =================================================

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'What are you selling?',
                    'autocomplete': 'off',
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'subcategory': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter a subcategory',
                }
            ),

            'condition': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            # =================================================
            # PRICING
            # =================================================

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter price',
                    'min': '0',
                    'step': '0.01',
                }
            ),

            'price_type': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'negotiable': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            # =================================================
            # LOCATION
            # =================================================

            'state': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Rivers State',
                }
            ),

            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Port Harcourt',
                }
            ),

            'specific_location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Estate, street, area or landmark',
                }
            ),

            # =================================================
            # PRODUCT INFORMATION
            # =================================================

            'brand': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Samsung, Toyota, LG',
                }
            ),

            'model': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter model',
                }
            ),

            'year': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. 2024',
                    'min': '1900',
                    'max': '2100',
                }
            ),

            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Black',
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Quantity available',
                    'min': '1',
                }
            ),

            # =================================================
            # DESCRIPTION
            # =================================================

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Describe your item in detail. Include its '
                        'condition, features, specifications, '
                        'age, defects and anything buyers should know.'
                    ),
                    'rows': 8,
                }
            ),

            # =================================================
            # SELLER PREFERENCES
            # =================================================

            'contact_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone number buyers can contact',
                    'autocomplete': 'tel',
                }
            ),

            'whatsapp_available': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),

            'delivery_available': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    # =====================================================
    # IMAGE VALIDATION
    # =====================================================

    def clean_images(self):

        images = self.cleaned_data.get('images')

        # -------------------------------------------------
        # EDITING EXISTING LISTING
        # -------------------------------------------------

        if self.instance and self.instance.pk:

            if not images:
                return []

            if len(images) > 10:
                raise forms.ValidationError(
                    'You can upload a maximum of 10 photos at a time.'
                )

        # -------------------------------------------------
        # NEW LISTING
        # -------------------------------------------------

        else:

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

        # -------------------------------------------------
        # VALIDATE EACH IMAGE
        # -------------------------------------------------

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


# =========================================================
# UNIFIED ACCOUNT SETTINGS
# =========================================================

class AccountSettingsForm(forms.ModelForm):

    full_name = forms.CharField(
        max_length=200,
        required=True,
        label='Full Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your full name',
                'autocomplete': 'name',
                'class': 'account-settings-input',
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter your email address',
                'autocomplete': 'email',
                'class': 'account-settings-input',
            }
        )
    )

    phone = forms.CharField(
        max_length=50,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your phone number',
                'autocomplete': 'tel',
                'class': 'account-settings-input',
            }
        )
    )

    class Meta:

        model = AccountSettings

        fields = (
            'full_name',
            'email',
            'phone',
            'address',
            'profile_image',
            'property_alerts',
            'plot_availability_alerts',
            'estate_alerts',
            'hire_notifications',
            'security_notifications',
            'profile_visible',
        )

        widgets = {

            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your address',
                    'autocomplete': 'street-address',
                    'class': 'account-settings-input',
                }
            ),

            'profile_image': forms.ClearableFileInput(
                attrs={
                    'accept': 'image/*',
                    'class': 'account-settings-file',
                }
            ),
        }

    def __init__(
        self,
        *args,
        user=None,
        **kwargs
    ):

        self.user = user

        super().__init__(
            *args,
            **kwargs
        )

        if not self.user:

            raise ValueError(
                'AccountSettingsForm requires a logged-in user.'
            )

        self.fields[
            'full_name'
        ].initial = (
            self.user.get_full_name()
            or self.user.first_name
            or ''
        )

        self.fields[
            'email'
        ].initial = self.user.email or ''

        current_phone = ''

        if self.instance and self.instance.pk:

            current_phone = (
                self.instance.phone or ''
            )

        if not current_phone:

            try:

                current_phone = (
                    self.user.customer_profile.phone
                    or ''
                )

            except Customer.DoesNotExist:

                pass

        if not current_phone:

            try:

                current_phone = (
                    self.user.skilled_worker_profile.phone
                    or ''
                )

            except SkilledWorker.DoesNotExist:

                pass

        self.fields[
            'phone'
        ].initial = current_phone

    # =====================================================
    # EMAIL
    # =====================================================

    def clean_email(self):

        email = (
            self.cleaned_data['email']
            .strip()
            .lower()
        )

        if not email:

            raise forms.ValidationError(
                'Email address is required.'
            )

        if (
            User.objects
            .filter(
                username__iexact=email
            )
            .exclude(
                pk=self.user.pk
            )
            .exists()
        ):

            raise forms.ValidationError(
                'This email address is already '
                'being used by another account.'
            )

        if (
            User.objects
            .filter(
                email__iexact=email
            )
            .exclude(
                pk=self.user.pk
            )
            .exists()
        ):

            raise forms.ValidationError(
                'This email address is already '
                'being used by another account.'
            )

        return email

    # =====================================================
    # FULL NAME
    # =====================================================

    def clean_full_name(self):

        full_name = (
            self.cleaned_data['full_name']
            .strip()
        )

        if not full_name:

            raise forms.ValidationError(
                'Full name is required.'
            )

        return full_name

    # =====================================================
    # PHONE
    # =====================================================

    def clean_phone(self):

        phone = (
            self.cleaned_data['phone']
            .strip()
        )

        if not phone:

            raise forms.ValidationError(
                'Phone number is required.'
            )

        return phone

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, commit=True):

        settings = super().save(
            commit=False
        )

        full_name = (
            self.cleaned_data['full_name']
            .strip()
        )

        email = (
            self.cleaned_data['email']
            .strip()
            .lower()
        )

        phone = (
            self.cleaned_data['phone']
            .strip()
        )

        settings.phone = phone

        # -------------------------------------------------
        # MAIN USER
        # -------------------------------------------------

        self.user.first_name = full_name
        self.user.email = email
        self.user.username = email

        # -------------------------------------------------
        # CUSTOMER
        # -------------------------------------------------

        try:

            customer = self.user.customer_profile

            customer.full_name = full_name
            customer.email = email
            customer.phone = phone

            if settings.address:

                customer.address = settings.address

            if commit:

                customer.save()

        except Customer.DoesNotExist:

            pass

        # -------------------------------------------------
        # SKILLED WORKER
        # -------------------------------------------------

        try:

            worker = self.user.skilled_worker_profile

            worker.full_name = full_name
            worker.email = email
            worker.phone = phone

            if commit:

                worker.save()

        except SkilledWorker.DoesNotExist:

            pass

        # -------------------------------------------------
        # SAVE EVERYTHING
        # -------------------------------------------------

        if commit:

            self.user.save(
                update_fields=[
                    'first_name',
                    'email',
                    'username',
                ]
            )

            settings.save()

        return settings


# =========================================================
# MARKETPLACE SELLER REVIEW
# =========================================================

class MarketplaceSellerReviewForm(forms.ModelForm):

    class Meta:

        model = MarketplaceReview

        fields = [
            'rating',
            'comment',
        ]

        widgets = {

            'rating': forms.Select(
                choices=[
                    (5, '★★★★★ - Excellent'),
                    (4, '★★★★☆ - Very Good'),
                    (3, '★★★☆☆ - Good'),
                    (2, '★★☆☆☆ - Fair'),
                    (1, '★☆☆☆☆ - Poor'),
                ],
                attrs={
                    'class': 'review-input',
                }
            ),

            'comment': forms.Textarea(
                attrs={
                    'class': 'review-input',
                    'placeholder': (
                        'Share your experience with this seller...'
                    ),
                    'rows': 6,
                }
            ),
        }

    def clean_comment(self):

        comment = self.cleaned_data.get(
            'comment'
        )

        if not comment or not comment.strip():

            raise forms.ValidationError(
                'Please write a review.'
            )

        return comment.strip()