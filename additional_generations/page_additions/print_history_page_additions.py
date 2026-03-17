"""Page additions for PrintHistoryPage - Billing Cycle Period card.

Target file: pages/print_history_page.py
Test case: C44873414

Merge instructions:
1. Add Elements class attributes to PrintHistoryPage.Elements inner class
2. Add property methods to PrintHistoryPage class body
3. Verify all locators work correctly
"""


class Elements:
    """Locator selectors for PrintHistoryPage."""
    plan_pause_info = "[data-testid='plan-pause-info']"
    billing_cycle_period_card = "[data-testid='billing-cycle-period-card']"
    complimentary_pages_progress_bar = "[data-testid='complimentary-pages-progress-bar']"
    complimentary_pages_value = "[data-testid='complimentary-pages-value']"
    complimentary_pages_info_icon = "[data-testid='complimentary-pages-info-icon']"
    complimentary_pages_info_message = "[data-testid='complimentary-pages-info-message']"
    complimentary_pages_tooltip = "[role='tooltip']:near([data-testid='complimentary-pages-info-icon'])"
    additional_pages_progress_bar = "[data-testid='additional-pages-progress-bar']"
    additional_pages_value = "[data-testid='additional-pages-value']"
    additional_pages_info_icon = "[data-testid='additional-pages-info-icon']"
    additional_pages_info_message = "[data-testid='additional-pages-info-message']"
    additional_pages_tooltip = "[role='tooltip']:near([data-testid='additional-pages-info-icon'])"
    total_printed_pages = "[data-testid='total-printed-pages']"


# Property methods to add to PrintHistoryPage class:
@property
def plan_pause_info(self):
    return self.page.locator(self.elements.plan_pause_info)

@property
def billing_cycle_period_card(self):
    return self.page.locator(self.elements.billing_cycle_period_card)

@property
def complimentary_pages_progress_bar(self):
    return self.page.locator(self.elements.complimentary_pages_progress_bar)

@property
def complimentary_pages_value(self):
    return self.page.locator(self.elements.complimentary_pages_value)

@property
def complimentary_pages_info_icon(self):
    return self.page.locator(self.elements.complimentary_pages_info_icon)

@property
def complimentary_pages_info_message(self):
    return self.page.locator(self.elements.complimentary_pages_info_message)

@property
def complimentary_pages_tooltip(self):
    return self.page.locator(self.elements.complimentary_pages_tooltip)

@property
def additional_pages_progress_bar(self):
    return self.page.locator(self.elements.additional_pages_progress_bar)

@property
def additional_pages_value(self):
    return self.page.locator(self.elements.additional_pages_value)

@property
def additional_pages_info_icon(self):
    return self.page.locator(self.elements.additional_pages_info_icon)

@property
def additional_pages_info_message(self):
    return self.page.locator(self.elements.additional_pages_info_message)

@property
def additional_pages_tooltip(self):
    return self.page.locator(self.elements.additional_pages_tooltip)

@property
def total_printed_pages(self):
    return self.page.locator(self.elements.total_printed_pages)
