"""Page additions for PrintHistoryPage - Billing Cycle Period card elements.

Target file: pages/print_history_page.py
Target class: PrintHistoryPage
Test case: C44873414 - Billing Cycle Period card
Test case title: Verifies Billing Cycle Period card display and behavior on Print and Payment History page

Purpose:
Adds locators and property methods for billing cycle period card elements including:
- Plan pause information display
- Billing cycle period card container
- Complimentary pages progress bar and related elements (value, info icon, tooltip, message)
- Additional pages progress bar and related elements (value, info icon, tooltip, message)
- Total printed pages display

These elements are required for test case C44873414 which verifies pause plan functionality
and page usage tracking across complimentary and additional page allocations.

Merge instructions:
1. Open pages/print_history_page.py in the AURA-FRAMEWORK repository
2. Locate the existing 'class Elements:' inner class (should be near the top of PrintHistoryPage class)
3. Add the following 13 attributes to the Elements class (after existing attributes):
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
4. Scroll to the end of the PrintHistoryPage class body (before the final closing)
5. Add all 13 property methods listed in this file
6. Save the file
7. Run the test script to verify all locators work
8. If any locators fail, inspect the actual HTML and update the data-testid values
"""

# Attributes to add to PrintHistoryPage.Elements inner class:
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
