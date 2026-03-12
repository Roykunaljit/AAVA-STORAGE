"""
Additional locators for PrintHistoryPage

Target File: pages/print_history_page.py
Target Class: PrintHistoryPage
Target Section: Elements inner class

Merge Instructions:
1. Open pages/print_history_page.py in the AURA-FRAMEWORK repository
2. Locate the PrintHistoryPage class
3. Find the Elements inner class inside PrintHistoryPage
4. Add all locator definitions below to the Elements class as class attributes
5. Maintain alphabetical order within the Elements class
6. Ensure no duplicate locator names
7. Test the page object after merging to verify all locators work

Test Case: C44873414 - Billing Cycle Period card
Purpose: These locators enable verification of the Billing Cycle Period card,
         including plan pause information, complimentary pages progress bar,
         additional pages progress bar, tooltips, and page usage tracking.
"""

# ══════════════════════════════════════════════════════════════════════════════
# ADD TO Elements CLASS IN PrintHistoryPage
# ══════════════════════════════════════════════════════════════════════════════

class Elements:
    """
    Additional locator strings for PrintHistoryPage.
    Merge these into the existing Elements class in pages/print_history_page.py
    """
    
    # Billing Cycle Period Card - Main Container
    billing_cycle_period_card = "[data-testid='billing-cycle-card']"
    billing_cycle_period_title = "[data-testid='billing-cycle-title']"

    # Plan Pause Information
    plan_pause_info_text = "[data-testid='plan-pause-info']"

    # Complimentary Pages Section
    complimentary_pages_progress_bar = "[data-testid='complimentary-pages-progress-bar']"
    complimentary_pages_value_text = "[data-testid='complimentary-pages-value']"
    complimentary_pages_info_icon = "[data-testid='complimentary-pages-info-icon']"
    complimentary_pages_tooltip = "[role='tooltip'][data-testid='complimentary-pages-tooltip']"
    complimentary_pages_info_message = "[data-testid='complimentary-pages-info-message']"

    # Additional Pages Section
    additional_pages_progress_bar = "[data-testid='additional-pages-progress-bar']"
    additional_pages_value_text = "[data-testid='additional-pages-value']"
    additional_pages_info_icon = "[data-testid='additional-pages-info-icon']"
    additional_pages_tooltip = "[role='tooltip'][data-testid='additional-pages-tooltip']"
    additional_pages_info_message = "[data-testid='additional-pages-info-message']"

    # Total Pages Printed
    total_printed_pages = "[data-testid='total-printed-pages']"
