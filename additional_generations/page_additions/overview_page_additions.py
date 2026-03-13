"""
Additional locators for OverviewPage

Target File: pages/overview_page.py
Target Class: OverviewPage
Target Section: __init__ method

Merge Instructions:
1. Open pages/overview_page.py in the AURA-FRAMEWORK repository
2. Locate the OverviewPage class
3. Find the __init__ method
4. Add all locator definitions below as direct properties (self.locator_name = page.locator('selector'))
5. Maintain alphabetical order within the __init__ method
6. Ensure no duplicate locator names
7. Test the page object after merging to verify all locators work

Test Case: C44873414 - Billing Cycle Period card
Purpose: These locators enable pause plan functionality for the test case,
         including pause plan link, modal, dropdown, confirmation, and banner.

NOTE: According to the mapping report, these locators already exist in pages/overview_page.py.
This file provides the correct selectors for these existing locators to ensure they match
the actual UI elements used in test case C44873414.
"""

# ══════════════════════════════════════════════════════════════════════════════
# ADD TO __init__ METHOD IN OverviewPage
# ══════════════════════════════════════════════════════════════════════════════

# Example of how these should be added to the __init__ method:
# def __init__(self, page):
#     super().__init__(page)
#     # ... existing locators ...
#     
#     # Pause Plan Elements (with fallback selectors)
#     self.pause_plan_link = page.locator("[data-testid='pause-plan-link'], a:has-text('Pause')")
#     self.pause_plan_modal = page.locator("[data-testid='pause-plan-modal'], [role='dialog']:has-text('Pause')")
#     self.pause_plan_dropdown = page.locator("[data-testid='pause-plan-dropdown']")
#     self.confirm_pause_plan = page.locator("[data-testid='confirm-pause-plan']")
#     self.plan_paused_banner = page.locator("[data-testid='plan-paused-banner']")


# ══════════════════════════════════════════════════════════════════════════════
# LOCATOR DEFINITIONS (for reference)
# ══════════════════════════════════════════════════════════════════════════════

# Pause Plan Elements (with fallback selectors)
pause_plan_link = "[data-testid='pause-plan-link'], a:has-text('Pause')"
pause_plan_modal = "[data-testid='pause-plan-modal'], [role='dialog']:has-text('Pause')"
pause_plan_dropdown = "[data-testid='pause-plan-dropdown']"
confirm_pause_plan = "[data-testid='confirm-pause-plan']"
plan_paused_banner = "[data-testid='plan-paused-banner']"
