"""Additional locators and methods for PrintHistoryPage

Merge into: pages/print_history_page.py
Test Case: C44873414 - Billing Cycle Period card

MERGE INSTRUCTIONS:
1. Add 'from playwright.sync_api import expect' at module level in print_history_page.py if not present
2. Locate the existing Elements class in PrintHistoryPage
3. Add the new locator attributes below to the Elements class
4. In the __init__ method, add the property definitions shown below after existing locators
5. Add the verification methods shown below to the class body
6. Remove 'from playwright.sync_api import expect' from inside each method if present
7. Maintain consistent indentation with the existing file

WARNINGS:
- Tooltip selectors use generic [role='tooltip'] which may match multiple elements
- Consider using data-testid attributes for tooltips if available
- Test all new locators after merge to ensure correct element targeting
"""


class Elements:
    # Billing Cycle Period Card locators
    plan_pause_info = "[data-testid='plan-pause-info']"
    billing_cycle_period_card = "[data-testid='billing-cycle-period-card']"
    
    # Complimentary Pages locators
    complimentary_pages_progress_bar = "[data-testid='complimentary-pages-progress-bar']"
    complimentary_pages_value = "[data-testid='complimentary-pages-value']"
    complimentary_pages_info_icon = "[data-testid='complimentary-pages-info-icon']"
    complimentary_pages_info_message = "[data-testid='complimentary-pages-info-message']"
    # WARNING: Generic tooltip selector - may need data-testid for specificity
    complimentary_pages_tooltip = "[role='tooltip']"
    
    # Additional Pages locators
    additional_pages_progress_bar = "[data-testid='additional-pages-progress-bar']"
    additional_pages_value = "[data-testid='additional-pages-value']"
    additional_pages_info_icon = "[data-testid='additional-pages-info-icon']"
    additional_pages_info_message = "[data-testid='additional-pages-info-message']"
    # WARNING: Generic selector - prefer data-testid if available
    additional_pages_tooltip = "[role='tooltip']"


# ═══════════════════════════════════════════════════════════════════════════════
# ADD THE FOLLOWING CODE TO THE __init__ METHOD OF PrintHistoryPage
# (Insert after self.elements = self.Elements())
# ═══════════════════════════════════════════════════════════════════════════════

# Billing Cycle Period Card locators as properties
self.plan_pause_info = page.locator(self.elements.plan_pause_info)
self.billing_cycle_period_card = page.locator(self.elements.billing_cycle_period_card)

# Complimentary Pages locators as properties
self.complimentary_pages_progress_bar = page.locator(self.elements.complimentary_pages_progress_bar)
self.complimentary_pages_value = page.locator(self.elements.complimentary_pages_value)
self.complimentary_pages_info_icon = page.locator(self.elements.complimentary_pages_info_icon)
self.complimentary_pages_info_message = page.locator(self.elements.complimentary_pages_info_message)
self.complimentary_pages_tooltip = page.locator(self.elements.complimentary_pages_tooltip)

# Additional Pages locators as properties
self.additional_pages_progress_bar = page.locator(self.elements.additional_pages_progress_bar)
self.additional_pages_value = page.locator(self.elements.additional_pages_value)
self.additional_pages_info_icon = page.locator(self.elements.additional_pages_info_icon)
self.additional_pages_info_message = page.locator(self.elements.additional_pages_info_message)
self.additional_pages_tooltip = page.locator(self.elements.additional_pages_tooltip)


# ═══════════════════════════════════════════════════════════════════════════════
# ADD THE FOLLOWING METHODS TO THE PrintHistoryPage CLASS BODY
# ═══════════════════════════════════════════════════════════════════════════════

def verify_plan_pause_info_not_displayed(self):
    """Verify plan pause information is not displayed."""
    from playwright.sync_api import expect
    expect(self.plan_pause_info).not_to_be_visible(timeout=10000)


def verify_plan_pause_info_displayed(self):
    """Verify plan pause information is displayed."""
    from playwright.sync_api import expect
    expect(self.plan_pause_info).to_be_visible(timeout=30000)


def verify_complimentary_pages_value(self, expected_used, expected_total, pause_plan=True):
    """Verify complimentary pages value displays correct usage."""
    from playwright.sync_api import expect
    expect(self.complimentary_pages_value).to_contain_text(f"{expected_used} of {expected_total}", timeout=30000)
    if pause_plan:
        expect(self.complimentary_pages_value).to_contain_text("Pause Plan", timeout=30000)


def hover_complimentary_info_icon(self):
    """Hover over complimentary pages info icon to display tooltip."""
    from playwright.sync_api import expect
    expect(self.complimentary_pages_info_icon).to_be_visible(timeout=30000)
    self.complimentary_pages_info_icon.hover()


def verify_additional_pages_value(self, expected_used, expected_total):
    """Verify additional pages value displays correct usage."""
    from playwright.sync_api import expect
    expect(self.additional_pages_value).to_contain_text(f"{expected_used} of {expected_total}", timeout=30000)
