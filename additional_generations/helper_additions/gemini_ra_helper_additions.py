"""Helper additions for GeminiRAHelper - Pause subscription method.

Target file: helper/gemini_ra_helper.py
Target class: GeminiRAHelper
Test case: C44873414 - Billing Cycle Period card

Purpose:
Adds pause_subscription static method to encapsulate Rails Admin pause plan operation.
This method eliminates the need for inline page.locator() calls in test scripts when
pausing a subscription via Rails Admin.

Merge instructions:
1. Open helper/gemini_ra_helper.py in the AURA-FRAMEWORK repository
2. Locate the GeminiRAHelper class
3. Add the pause_subscription method below to the class (as a static method)
4. Place it near other subscription state manipulation methods like subscription_to_subscribed
5. Save the file
6. Update test scripts to use GeminiRAHelper.pause_subscription(page, tenant_email) instead of inline Rails Admin interactions
"""

from playwright.sync_api import Page


@staticmethod
def pause_subscription(page: Page, tenant_email: str):
    """Pause a subscription via Rails Admin.
    
    Args:
        page: Playwright page object
        tenant_email: Email of the tenant whose subscription to pause
    """
    GeminiRAHelper.access(page)
    GeminiRAHelper.access_tenant_page(page, tenant_email)
    
    # Navigate to subscription edit page
    edit_link = page.locator("a:has-text('Edit')")
    edit_link.click()
    page.wait_for_load_state('networkidle', timeout=30000)
    
    # Update state to paused
    subscription_state_dropdown = page.locator("select[name='subscription[subscription_state]']")
    subscription_state_dropdown.select_option('paused')
    
    # Save changes
    save_button = page.locator("input[type='submit'][value='Save']")
    save_button.click()
    page.wait_for_load_state('networkidle', timeout=30000)
    
    # Verify state changed
    GeminiRAHelper.verify_rails_admin_info(page, 'Subscription State', 'paused', retry=True)
