from rest_framework import fields

from management.utils import mask_phone_number


class AnonymizedStringField(fields.CharField):
    def to_representation(self, value):
        value = super().to_representation(value)
        if len(value) > 1:
            return f"{value[0]}{len(value) * 'x'}"
        return value


class AnonymizedEmailField(fields.EmailField):
    def to_representation(self, value):
        value = super().to_representation(value)

        if len(value) > 1:
            email_part, domain_part = value.split("@")
            return f"{email_part[0]}{len(email_part) * 'x'}@{domain_part}"


class AnonymizedPhoneField(fields.CharField):
    def to_representation(self, value):
        value = super().to_representation(value)
        if len(value) > 1:
            return mask_phone_number(value)

        return value
