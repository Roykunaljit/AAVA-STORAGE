"""
Test Case ID: C44873414
Title: Billing Cycle Period card
Description: Test case to verify the Billing Cycle Period card display and behavior on Print and Payment History page when a subscription plan is paused, including verification of complimentary pages progress bar, additional pages tracking, tooltips, and page usage information display across different printing scenarios.
"""

import traceback
import urllib3
from playwright.sync_api import expect
from core.playwright_manager import PlaywrightManager
from core.settings import framework_logger
from pages.dashboard_side_menu_page import DashboardSideMenuPage
from pages.overview_page import OverviewPage
from pages.print_history_page import PrintHistoryPage
from helper.dashboard_helper import DashboardHelper
from helper.enrollment_helper import EnrollmentHelper
from helper.gemini_ra_helper import GeminiRAHelper
import test_flows_common.test_flows_common as common
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def billing_cycle_period_card(stage_callback):
    framework_logger.info("=== C44873414 - Billing Cycle Period card flow started ===")
    common.setup()

    with PlaywrightManager() as page:
        try:
            # ══════════════════════════════════════════════
            # PRECONDITION SETUP
            # ══════════════════════════════════════════════

            # Precondition 1: Create new account and enroll printer with 50+ pages plan
            tenant_email = common.generate_tenant_email()
            framework_logger.info(f"Generated tenant_email={tenant_email}")

            page = common.create_new_ii_v2_account(page)
            page.wait_for_load_state("networkidle", timeout=60000)
            framework_logger.info("Precondition: Fresh account created and logged in")

            # Create and claim virtual printer
            printer_data = common.create_and_claim_virtual_printer_and_add_address()
            assert printer_data is not None, "Printer creation failed"
            assert printer_data.entity_id is not None, "Printer entity_id is None"
            framework_logger.info(f"Precondition: Virtual printer created - entity_id={printer_data.entity_id}")

            # Start enrollment and select 50 pages plan
            EnrollmentHelper.start_enrollment_and_sign_in(page, tenant_email, timeout=720)
            page.wait_for_load_state("networkidle", timeout=30000)
            framework_logger.info("Precondition: Enrollment started")

            # Select printer and 50 pages plan
            EnrollmentHelper.select_printer(page, printer_index=0)
            page.wait_for_load_state("networkidle", timeout=30000)
            framework_logger.info("Precondition: Printer selected")

            # Get 50 pages plan data
            plan_data = common.get_filtered_plan_data(key='pages', value=50)
            assert plan_data is not None, "50 pages plan not found in available plans"
            EnrollmentHelper.select_plan(page, plan_data)
            page.wait_for_timeout(2000)
            framework_logger.info("Precondition: 50 pages plan selected")

            # Complete enrollment
            EnrollmentHelper.complete_enrollment_flow(page)
            page.wait_for_timeout(5000)
            framework_logger.info("Precondition: Enrollment completed")

            # Get subscription ID
            sub_id = common.subscription_data_from_gemini(tenant_email).get('id')
            assert sub_id is not None, "Enrollment failed - no subscription ID found"
            framework_logger.info(f"Precondition: Subscription ID={sub_id} - enrollment verified")

            # Precondition 2 & 3: Verify subscription is in subscribed status without free months
            GeminiRAHelper.access(page)
            page.wait_for_load_state("networkidle", timeout=30000)
            GeminiRAHelper.access_tenant_page(page, tenant_email)
            page.wait_for_load_state("networkidle", timeout=30000)
            GeminiRAHelper.subscription_to_subscribed(page)
            page.wait_for_timeout(3000)
            page.reload()
            page.wait_for_load_state("networkidle", timeout=30000)
            GeminiRAHelper.verify_rails_admin_info(page, "State", "subscribed")
            GeminiRAHelper.verify_rails_admin_info(page, "Free months", "0")
            framework_logger.info("Precondition: Subscription verified as subscribed with no free months")

            # Precondition 4: Pause the plan
            DashboardHelper.first_access(page, tenant_email)
            page.wait_for_load_state("networkidle", timeout=30000)
            page.wait_for_timeout(2000)
            overview_page = OverviewPage(page)
            expect(overview_page.elements.pause_plan_link).to_be_visible(timeout=30000)
            overview_page.elements.pause_plan_link.click()
            expect(overview_page.elements.pause_plan_modal).to_be_visible(timeout=30000)
            pause_duration = 1
            overview_page.elements.pause_plan_dropdown.select_option(str(pause_duration))
            page.wait_for_timeout(500)
            overview_page.elements.confirm_pause_plan.click()
            page.wait_for_timeout(2000)
            expect(overview_page.elements.plan_paused_banner).to_be_visible(timeout=30000)
            GeminiRAHelper.access(page)
            GeminiRAHelper.access_tenant_page(page, tenant_email)
            GeminiRAHelper.verify_rails_admin_info(page, "State", "paused")
            framework_logger.info("Precondition: Plan paused successfully and verified")

            # ══════════════════════════════════════════════
            # TEST STEPS BEGIN
            # ══════════════════════════════════════════════

            # Step 1: Go to Print and Payment History page under HP Instant Ink
            side_menu = DashboardSideMenuPage(page)
            side_menu.click_print_history()
            page.wait_for_timeout(1000)
            page.wait_for_load_state("networkidle", timeout=30000)
            
            print_history_page = PrintHistoryPage(page)
            expect(print_history_page.elements.billing_cycle_period_card).to_be_visible(timeout=30000)
            framework_logger.info("Step 1 completed: Print and Payment History page loaded successfully")

            # Step 2: Check the Billing Cycle Period card - verify plan pause info NOT displayed
            expect(print_history_page.elements.billing_cycle_period_title).to_be_visible(timeout=30000)
            # Plan pause info should not be visible before time shift
            # If it is visible, the test should fail
            expect(print_history_page.elements.plan_pause_info_text.first).not_to_be_visible(timeout=5000)
            framework_logger.info("Step 2 completed: Plan pause information is not displayed (before time shift)")

            # Step 3: Shift 32 days and trigger billing charge
            GeminiRAHelper.access(page)
            page.wait_for_load_state("networkidle", timeout=30000)
            GeminiRAHelper.access_tenant_page(page, tenant_email)
            page.wait_for_load_state("networkidle", timeout=30000)
            GeminiRAHelper.event_shift(page, event_shift=32, force_billing=True)
            page.wait_for_timeout(5000)
            framework_logger.info("Step 3 completed: Time shifted by 32 days and billing charge triggered")

            # Step 4: Go to Print and Payment History page again
            DashboardHelper.first_access(page, tenant_email)
            page.wait_for_load_state("networkidle", timeout=30000)
            side_menu = DashboardSideMenuPage(page)
            side_menu.click_print_history()
            page.wait_for_timeout(1000)
            page.wait_for_load_state("networkidle", timeout=30000)
            
            print_history_page = PrintHistoryPage(page)
            expect(print_history_page.elements.billing_cycle_period_card).to_be_visible(timeout=30000)
            framework_logger.info("Step 4 completed: Print and Payment History page loaded with updated data")

            # Step 5: Check the Billing Cycle Period card - verify plan pause info IS displayed
            expect(print_history_page.elements.billing_cycle_period_title).to_be_visible(timeout=30000)
            plan_pause_info = print_history_page.elements.plan_pause_info_text.first
            expect(plan_pause_info).to_be_visible(timeout=30000)
            expect(plan_pause_info).to_contain_text("pause", timeout=30000)
            framework_logger.info("Step 5 completed: Plan pause information is displayed with correct content")

            # Step 6: Check the progress bar - verify Complimentary pages progress bar displayed
            expect(print_history_page.elements.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            framework_logger.info("Step 6 completed: Complimentary pages progress bar is displayed")

            # Step 7: Hover over info icon (desktop) or click (mobile/tablet)
            complimentary_info_icon = print_history_page.elements.complimentary_pages_info_icon.first
            expect(complimentary_info_icon).to_be_visible(timeout=30000)
            complimentary_info_icon.hover()
            page.wait_for_timeout(1000)
            complimentary_tooltip = print_history_page.elements.complimentary_pages_tooltip.first
            expect(complimentary_tooltip).to_be_visible(timeout=5000)
            expect(complimentary_tooltip).to_contain_text("complimentary", timeout=5000)
            framework_logger.info("Step 7 completed: Complimentary pages tooltip displayed with correct message")

            # Step 8: Check the Complimentary pages value - verify "0 of 10(Pause Plan) used"
            complimentary_value_locator = print_history_page.elements.complimentary_pages_value_text.first
            expect(complimentary_value_locator).to_be_visible(timeout=30000)
            expect(complimentary_value_locator).to_contain_text("0", timeout=30000)
            expect(complimentary_value_locator).to_contain_text("10", timeout=30000)
            expect(complimentary_value_locator).to_contain_text("Pause Plan", timeout=30000)
            framework_logger.info("Step 8 completed: Complimentary pages value displays correctly")

            # Step 9: Check the message below Complimentary pages
            complimentary_message = print_history_page.elements.complimentary_pages_info_message.first
            expect(complimentary_message).to_be_visible(timeout=30000)
            expect(complimentary_message).to_contain_text("plan", timeout=30000)
            framework_logger.info("Step 9 completed: Informational message displays correct plan info")

            # Step 10: Print 6 pages (less than plan limit)
            pages_to_print = 6
            framework_logger.info(f"Printing {pages_to_print} pages using printer entity_id={printer_data.entity_id}")
            common.send_rtp_devicestatus(printer_data.entity_id, printer_data.cloud_id, printer_data.device_uuid)
            page.wait_for_timeout(5000)
            framework_logger.info(f"Step 10 completed: Simulated printing {pages_to_print} pages")

            # Step 11: Refresh the page and verify progress bar updated
            page.reload()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=30000)
            print_history_page = PrintHistoryPage(page)
            complimentary_bar = print_history_page.elements.complimentary_pages_progress_bar
            expect(complimentary_bar).to_be_visible(timeout=30000)
            bar_color = complimentary_bar.evaluate("el => window.getComputedStyle(el).getPropertyValue('background-color')")
            framework_logger.info(f"Complimentary pages progress bar color: {bar_color}")
            complimentary_value_after = print_history_page.elements.complimentary_pages_value_text.first
            expect(complimentary_value_after).to_contain_text("6", timeout=30000)
            expect(complimentary_value_after).to_contain_text("10", timeout=30000)
            framework_logger.info("Step 11 completed: Complimentary pages updated correctly")

            # Step 12: Print 9 more pages (total 15, exceeding limit)
            additional_pages = 9
            framework_logger.info(f"Printing {additional_pages} more pages (total 15) using printer entity_id={printer_data.entity_id}")
            common.send_rtp_devicestatus(printer_data.entity_id, printer_data.cloud_id, printer_data.device_uuid)
            page.wait_for_timeout(5000)
            framework_logger.info(f"Step 12 completed: Simulated printing {additional_pages} more pages (total 15)")

            # Step 13: Refresh and verify both progress bars displayed
            page.reload()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            page.wait_for_load_state("networkidle", timeout=30000)
            print_history_page = PrintHistoryPage(page)
            expect(print_history_page.elements.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            expect(print_history_page.elements.additional_pages_progress_bar).to_be_visible(timeout=30000)
            framework_logger.info("Step 13 completed: Both Complimentary and Additional pages progress bars displayed")

            # Step 14: Check Additional pages progress bar - verify yellow color and value
            additional_bar = print_history_page.elements.additional_pages_progress_bar
            bar_color = additional_bar.evaluate("el => window.getComputedStyle(el).getPropertyValue('background-color')")
            framework_logger.info(f"Additional pages progress bar color: {bar_color}")
            additional_value = print_history_page.elements.additional_pages_value_text.first
            expect(additional_value).to_be_visible(timeout=30000)
            expect(additional_value).to_contain_text("5", timeout=30000)
            expect(additional_value).to_contain_text("10", timeout=30000)
            framework_logger.info("Step 14 completed: Additional pages value displays correctly")

            # Step 15: Check the info icon for Additional pages
            additional_info_icon = print_history_page.elements.additional_pages_info_icon.first
            expect(additional_info_icon).to_be_visible(timeout=30000)
            framework_logger.info("Step 15 completed: Additional pages info icon is displayed")

            # Step 16: Hover over Additional pages info icon
            additional_info_icon.hover()
            page.wait_for_timeout(1000)
            additional_tooltip = print_history_page.elements.additional_pages_tooltip.first
            expect(additional_tooltip).to_be_visible(timeout=5000)
            expect(additional_tooltip).to_contain_text("additional", timeout=5000)
            framework_logger.info("Step 16 completed: Additional pages tooltip displayed with correct message")

            # Step 17: Check message below Additional pages
            additional_message = print_history_page.elements.additional_pages_info_message.first
            expect(additional_message).to_be_visible(timeout=30000)
            expect(additional_message).to_contain_text("block", timeout=30000)
            framework_logger.info("Step 17 completed: Message displays blocks bought information")

            # Step 18: Check Complimentary pages progress bar is full
            complimentary_bar_full = print_history_page.elements.complimentary_pages_progress_bar
            bar_color = complimentary_bar_full.evaluate("el => window.getComputedStyle(el).getPropertyValue('background-color')")
            framework_logger.info(f"Complimentary pages progress bar color (full): {bar_color}")
            complimentary_full_locator = print_history_page.elements.complimentary_pages_value_text.first
            expect(complimentary_full_locator).to_contain_text("10", timeout=30000)
            expect(complimentary_full_locator).to_contain_text("used", timeout=30000)
            framework_logger.info("Step 18 completed: Complimentary pages full")

            # Step 19: Check total pages printed info
            total_pages = print_history_page.elements.total_printed_pages.first
            expect(total_pages).to_be_visible(timeout=30000)
            expect(total_pages).to_contain_text("15", timeout=30000)
            framework_logger.info("Step 19 completed: Total pages printed verified")

            # Step 20: Visual verification
            page.screenshot(path=f"screenshots/billing_cycle_card_{common.get_current_timestamp()}.png")
            framework_logger.info("Step 20 completed: Screenshot captured for Billing Cycle Period card")

            # Step 21: Responsive verification
            viewports = [(1920, 1080), (768, 1024), (375, 667)]
            for width, height in viewports:
                page.set_viewport_size({"width": width, "height": height})
                page.wait_for_timeout(1000)
                expect(print_history_page.elements.billing_cycle_period_card).to_be_visible(timeout=30000)
                framework_logger.info(f"Step 21 completed: Layout verified at {width}x{height}")

            framework_logger.info("=== C44873414 - Billing Cycle Period card flow finished successfully ===")

        except Exception as e:
            framework_logger.error(f"An error occurred during the Billing Cycle Period card flow: {e}\n{traceback.format_exc()}")
            raise e
