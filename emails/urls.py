from rest_framework.routers import DefaultRouter
from emails.views import MailboxViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"mailboxes", MailboxViewSet, basename="mailbox")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = router.urls