"""Helper additions for GeminiRAHelper - Pause subscription method.

Target file: helper/gemini_ra_helper.py
Target class: GeminiRAHelper
Test case: C44873414 - Billing Cycle Period card

Purpose:
Adds a static method to pause a subscription via Rails Admin interface.
This encapsulates the admin/backend interaction that was previously inline in the test script.

Merge instructions:
1. Open helper/gemini_ra_helper.py in the AURA-FRAMEWORK repository
2. Locate the GeminiRAHelper class
3. Add the pause_subscription method below to the class (as a static method)
4. Ensure GlobalState is imported at the top of the file
5. Save the file
6. Run the test script to verify the method works correctly
"""

from core.settings import GlobalState


@staticmethod
def pause_subscription(page, subscription_id):
    """Pause a subscription via Rails Admin.
    
    Args:
        page: Playwright page object
        subscription_id: ID of the subscription to pause
    """
    subscription_page_url = f"{GlobalState.gemini_ra_url}/subscriptions/{subscription_id}/edit"
    page.goto(subscription_page_url)
    page.wait_for_load_state('networkidle', timeout=30000)
    page.select_option('select#subscription_subscription_state', 'paused')
    page.click('button[type="submit"]')
    page.wait_for_load_state('networkidle', timeout=30000)
