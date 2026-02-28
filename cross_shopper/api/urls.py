"""URLs for the api app."""

from django.urls import include, path
from rest_framework_nested import routers
from .views.errors import ErrorViewSet
from .views.pricing import PricingViewSet
from .views.report_pricing import ReportPricingReadOnlyViewSet
from .views.report_summary import ReportSummaryViewSet
from .views.reports import ReportsReadOnlyViewSet
from .views.scrapers import ScrapersReadOnlyViewSet

router = routers.SimpleRouter()
router.register(r'errors', ErrorViewSet)
router.register(r'pricing', PricingViewSet)
router.register(r'reports', ReportsReadOnlyViewSet)
router.register(r'scrapers', ScrapersReadOnlyViewSet)

reports_router = routers.NestedSimpleRouter(router, r'reports', lookup='report')
reports_router.register(
    r'pricing',
    ReportPricingReadOnlyViewSet,
    basename='report_pricing',
)
reports_router.register(
    r'summary',
    ReportSummaryViewSet,
    basename='report_summary',
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/", include(reports_router.urls)),
]
