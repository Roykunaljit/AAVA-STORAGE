"""
Additional locators for OverviewPage

Target File: pages/overview_page.py
Target Class: OverviewPage
Target Section: Elements inner class

Merge Instructions:
1. Open pages/overview_page.py in the AURA-FRAMEWORK repository
2. Locate the OverviewPage class
3. Find the Elements inner class inside OverviewPage
4. Add all locator definitions below to the Elements class as class attributes
5. Maintain alphabetical order within the Elements class
6. Ensure no duplicate locator names
7. Test the page object after merging to verify all locators work

Test Case: C44873414 - Billing Cycle Period card
Purpose: These locators enable pause plan functionality for the test case,
         including pause plan link, modal, dropdown, confirmation, and banner.
"""

# ══════════════════════════════════════════════════════════════════════════════
# ADD TO Elements CLASS IN OverviewPage
# ══════════════════════════════════════════════════════════════════════════════

class Elements:
    """
    Additional locator strings for OverviewPage.
    Merge these into the existing Elements class in pages/overview_page.py
    """
    
    # Pause Plan Elements
    pause_plan_link = "[data-testid='pause-plan-link']"
    pause_plan_modal = "[data-testid='pause-plan-modal']"
    pause_plan_dropdown = "[data-testid='pause-plan-dropdown']"
    confirm_pause_plan = "[data-testid='confirm-pause-plan']"
    plan_paused_banner = "[data-testid='plan-paused-banner']"
