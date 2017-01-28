from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render


class VerifiedEmailRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is authenticated. If they are not, it resends a verification
    email and returns a page telling them to verify.
    """
    def dispatch(self, request, *args, **kwargs):
        if not EmailAddress.objects.filter(user=request.user, verified=True).exists():
            send_email_confirmation(request, request.user)
            # Should maybe be some kind of reverse blah blah blah
            return render(request,
                          'account/verified_email_required.html')
        return super().dispatch(request, *args, **kwargs)





