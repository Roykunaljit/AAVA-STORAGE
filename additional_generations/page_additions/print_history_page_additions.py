# Additional locators and methods for PrintHistoryPage
# Merge into: pages/print_history_page.py

# ADD TO __init__ METHOD:
self.billing_cycle_period_card = page.locator("[data-testid='billing-cycle-period-card']")
self.plan_pause_information = page.locator("[data-testid='plan-pause-information']")
self.complimentary_pages_progress_bar = page.locator("[data-testid='complimentary-pages-progress-bar']")
self.complimentary_pages_info_icon = page.locator("[data-testid='complimentary-pages-info-icon']")
self.complimentary_pages_value = page.locator("[data-testid='complimentary-pages-value']")
self.complimentary_pages_message = page.locator("[data-testid='complimentary-pages-message']")
self.additional_pages_progress_bar = page.locator("[data-testid='additional-pages-progress-bar']")
self.additional_pages_info_icon = page.locator("[data-testid='additional-pages-info-icon']")
self.additional_pages_value = page.locator("[data-testid='additional-pages-value']")
self.additional_pages_message = page.locator("[data-testid='additional-pages-message']")
self.total_pages_printed = page.locator("[data-testid='total-pages-printed']")

# ADD THESE METHODS TO THE CLASS BODY:
def verify_billing_cycle_card_visible(self):
    from playwright.sync_api import expect
    expect(self.billing_cycle_period_card).to_be_visible(timeout=30000)

def verify_complimentary_pages_value(self, expected_used, expected_total, pause_plan=True):
    from playwright.sync_api import expect
    expect(self.complimentary_pages_value).to_be_visible(timeout=30000)
    expect(self.complimentary_pages_value).to_contain_text(f"{expected_used} of {expected_total}", timeout=30000)
    if pause_plan:
        expect(self.complimentary_pages_value).to_contain_text("Pause Plan", timeout=30000)
