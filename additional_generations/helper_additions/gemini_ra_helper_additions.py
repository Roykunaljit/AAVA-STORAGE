"""GeminiRAHelper Additions

Additional helper methods for GeminiRAHelper to support test case C44873414.
These methods encapsulate Rails Admin interactions for subscription management.
"""

from core.settings import framework_logger


class GeminiRAHelperAdditions:
    """Additional helper methods for Gemini Rails Admin operations."""

    @staticmethod
    def pause_subscription(page):
        """Pauses a subscription by changing state to paused in Rails Admin.
        
        Args:
            page: Playwright Page object
            
        This method encapsulates the Rails Admin interaction pattern for pausing
        a subscription. It assumes the user is already on the tenant's subscription
        detail page in Rails Admin.
        """
        page.click("text=Edit")
        page.select_option("select[name='subscription[state]']", "paused")
        page.click("input[type='submit'][value='Save']")
        framework_logger.info("Subscription state changed to paused")
