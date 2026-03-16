# Additional locators and methods for PrintHistoryPage
# Merge into: pages/print_history_page.py
# Test Case: C44873414 - Billing Cycle Period card

# ADD TO __init__ METHOD:

# Billing Cycle Period Card locators
self.plan_pause_info = page.locator("[data-testid='plan-pause-info']")
self.billing_cycle_period_card = page.locator("[data-testid='billing-cycle-period-card']")

# Complimentary Pages locators
self.complimentary_pages_progress_bar = page.locator("[data-testid='complimentary-pages-progress-bar']")
self.complimentary_pages_value = page.locator("[data-testid='complimentary-pages-value']")
self.complimentary_pages_info_icon = page.locator("[data-testid='complimentary-pages-info-icon']")
self.complimentary_pages_info_message = page.locator("[data-testid='complimentary-pages-info-message']")

# Additional Pages locators
self.additional_pages_progress_bar = page.locator("[data-testid='additional-pages-progress-bar']")
self.additional_pages_value = page.locator("[data-testid='additional-pages-value']")
self.additional_pages_info_icon = page.locator("[data-testid='additional-pages-info-icon']")
self.additional_pages_info_message = page.locator("[data-testid='additional-pages-info-message']")

# ADD THESE METHODS TO CLASS BODY:

def verify_plan_pause_info_not_displayed(self):
    from playwright.sync_api import expect
    if self.plan_pause_info.count() > 0:
        expect(self.plan_pause_info).not_to_be_visible(timeout=10000)

def verify_plan_pause_info_displayed(self):
    from playwright.sync_api import expect
    expect(self.plan_pause_info).to_be_visible(timeout=30000)

def verify_complimentary_pages_value(self, expected_used, expected_total, pause_plan=True):
    from playwright.sync_api import expect
    expect(self.complimentary_pages_value).to_contain_text(f"{expected_used} of {expected_total}", timeout=30000)
    if pause_plan:
        expect(self.complimentary_pages_value).to_contain_text("Pause Plan", timeout=30000)

def hover_complimentary_info_icon(self):
    from playwright.sync_api import expect
    expect(self.complimentary_pages_info_icon).to_be_visible(timeout=30000)
    self.complimentary_pages_info_icon.hover()

def verify_additional_pages_value(self, expected_used, expected_total):
    from playwright.sync_api import expect
    expect(self.additional_pages_value).to_contain_text(f"{expected_used} of {expected_total}", timeout=30000)
