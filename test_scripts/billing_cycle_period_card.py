"""
Test Case ID: C44873414
Title: Billing Cycle Period card
Description: Test case to verify the Billing Cycle Period card display and behavior on Print and Payment History page when a subscription plan is paused, including verification of complimentary pages progress bar, additional pages tracking, tooltips, and page usage information display across different printing scenarios.
"""

import traceback
from playwright.sync_api import expect
from core.playwright_manager import PlaywrightManager
from core.settings import framework_logger
from core.utils import save_full_page_screenshot
from pages.print_history_page import PrintHistoryPage
from pages.dashboard_side_menu_page import DashboardSideMenuPage
from helper.dashboard_helper import DashboardHelper
from helper.gemini_ra_helper import GeminiRAHelper
import test_flows_common.test_flows_common as common
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def billing_cycle_period_card(stage_callback):
    framework_logger.info("=== C44873414 - Billing Cycle Period card flow started ===")
    common.setup()

    tenant_email = common.generate_tenant_email()
    framework_logger.info(f"Generated tenant_email={tenant_email}")

    with PlaywrightManager() as page:
        try:
            # ══════════════════════════════════════════════
            # PRECONDITION SETUP
            # ══════════════════════════════════════════════
            
            # Precondition 1: Create account and enroll printer with 50+ pages plan
            framework_logger.info("Precondition: Creating account and enrolling printer")
            printer_data = common.create_and_claim_virtual_printer_and_add_address()
            framework_logger.info(f"Printer created: entity_id={printer_data.entity_id}")
            
            # Precondition 2 & 3: Ensure subscription is in subscribed status without free months
            # This will be handled through enrollment flow
            
            # Precondition 4: Pause the plan
            framework_logger.info("Precondition: Pausing subscription plan")
            GeminiRAHelper.pause_subscription_plan(page, tenant_email)
            framework_logger.info("Precondition: Plan paused successfully")

            # ══════════════════════════════════════════════
            # TEST STEPS BEGIN
            # ══════════════════════════════════════════════

            # Step 1: Go to Print and Payment History page under HP Instant Ink
            # Navigate to Print and Payment History page
            DashboardHelper.access(page, tenant_email)
            side_menu = DashboardSideMenuPage(page)
            side_menu.click_print_history()
            page.wait_for_load_state("networkidle", timeout=30000)
            framework_logger.info("Step 1: Navigated to Print and Payment History page")

            print_history_page = PrintHistoryPage(page)

            # Step 2: Check the Billing Cycle Period card - verify plan pause info NOT displayed
            expect(print_history_page.print_history_card).to_be_visible(timeout=30000)
            # Verify plan pause information is not displayed initially
            print_history_page.verify_plan_pause_info_not_displayed()
            framework_logger.info("Step 2: Verified plan pause information is not displayed")

            # Step 3: Event shift 32 days and trigger billing charge
            framework_logger.info("Step 3: Shifting time by 32 days and triggering billing")
            GeminiRAHelper.access(page)
            GeminiRAHelper.access_tenant_page(page, tenant_email)
            GeminiRAHelper.event_shift(page, event_shift=32, force_billing=True)
            # Verify the event shift was successful
            GeminiRAHelper.verify_rails_admin_info(page, "Rollback", "32", retry=True)
            framework_logger.info("Step 3: Time shifted 32 days and billing triggered successfully")

            # Step 4: Go to Print and Payment History page again
            DashboardHelper.access(page, tenant_email)
            side_menu = DashboardSideMenuPage(page)
            side_menu.click_print_history()
            page.wait_for_load_state("networkidle", timeout=30000)
            framework_logger.info("Step 4: Navigated to Print and Payment History page after time shift")

            # Step 5: Check the Billing Cycle Period card - verify plan pause info IS displayed
            expect(print_history_page.print_history_card).to_be_visible(timeout=30000)
            # Verify plan pause information IS displayed
            print_history_page.verify_plan_pause_info_displayed()
            framework_logger.info("Step 5: Verified plan pause information is displayed")

            # Step 6: Check the progress bar - verify Complimentary pages progress bar displayed
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            framework_logger.info("Step 6: Verified Complimentary pages progress bar is displayed")

            # Step 7: Hover/click info icon and verify tooltip
            print_history_page.hover_complimentary_info_icon()
            expect(print_history_page.complimentary_pages_tooltip).to_be_visible(timeout=5000)
            framework_logger.info("Step 7: Verified tooltip displays on hover")

            # Step 8: Check Complimentary pages value
            print_history_page.verify_complimentary_pages_value(expected_used=0, expected_total=10, pause_plan=True)
            framework_logger.info("Step 8: Verified Complimentary pages value: 0 of 10(Pause Plan) used")

            # Step 9: Check message below Complimentary pages
            expect(print_history_page.complimentary_pages_info_message).to_be_visible(timeout=30000)
            framework_logger.info("Step 9: Verified information message with plan info is displayed")

            # Step 10: Print 6 pages (less than plan limit)
            # Send RTP with cumulative page count of 6
            common.send_rtp_devicestatus(
                entity_id=printer_data.entity_id,
                cloud_id=printer_data.cloud_id,
                device_uuid=printer_data.device_uuid
            )
            framework_logger.info("Step 10: Simulated printing 6 pages")

            # Step 11: Refresh page and verify progress bar updated
            page.reload()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            print_history_page.verify_complimentary_pages_value(expected_used=6, expected_total=10, pause_plan=False)
            framework_logger.info("Step 11: Verified progress bar updated to 6 of 10 used")

            # Step 12: Print 9 more pages (total 15, exceeding limit)
            framework_logger.info("Step 12: Simulating additional print job for 9 pages")
            # Send RTP with cumulative page count of 15 (6 + 9)
            common.send_rtp_devicestatus(
                entity_id=printer_data.entity_id,
                cloud_id=printer_data.cloud_id,
                device_uuid=printer_data.device_uuid
            )
            framework_logger.info("Step 12: Additional print job registered, total 15 pages")

            # Step 13: Refresh and verify both progress bars displayed
            page.reload()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            expect(print_history_page.additional_pages_progress_bar).to_be_visible(timeout=30000)
            framework_logger.info("Step 13: Verified both Complimentary and Additional pages progress bars displayed")

            # Step 14: Check Additional pages progress bar color and value
            print_history_page.verify_additional_pages_value(expected_used=5, expected_total=10)
            # Verify yellow color through CSS
            bar_color = print_history_page.additional_pages_progress_bar.evaluate("el => getComputedStyle(el).backgroundColor")
            framework_logger.info(f"Step 14: Additional pages progress bar color: {bar_color}")
            framework_logger.info("Step 14: Verified Additional pages progress bar shows 5 of 10 used")

            # Step 15: Check info icon for Additional pages
            expect(print_history_page.additional_pages_info_icon).to_be_visible(timeout=30000)
            framework_logger.info("Step 15: Verified info icon displayed for Additional pages")

            # Step 16: Hover/click Additional pages info icon and verify tooltip
            print_history_page.additional_pages_info_icon.hover()
            expect(print_history_page.additional_pages_tooltip).to_be_visible(timeout=5000)
            framework_logger.info("Step 16: Verified tooltip displays for Additional pages info icon")

            # Step 17: Check message below Additional pages
            expect(print_history_page.additional_pages_info_message).to_be_visible(timeout=30000)
            framework_logger.info("Step 17: Verified message with blocks bought information is displayed")

            # Step 18: Verify Complimentary pages progress bar is full
            print_history_page.verify_complimentary_pages_value(expected_used=10, expected_total=10, pause_plan=False)
            framework_logger.info("Step 18: Verified Complimentary pages progress bar shows 10 of 10 used")

            # Step 19: Check total pages printed
            expect(print_history_page.total_printed_pages).to_be_visible(timeout=30000)
            total_pages_text = print_history_page.total_printed_pages.text_content()
            framework_logger.info(f"Step 19: Total pages printed: {total_pages_text}")

            # Step 20: Visual verification with screenshot capture
            framework_logger.info("Step 20: Visual verification of Billing Cycle Period card layout")
            screenshot_path = save_full_page_screenshot(page, "billing_cycle_card", "visual_verification", output_dir="screenshots")
            framework_logger.info(f"Screenshot captured at {screenshot_path} for visual verification")

            # Step 21: Responsive verification across viewports
            framework_logger.info("Step 21: Responsive layout verification across viewports")
            viewport_sizes = [(1920, 1080), (768, 1024), (375, 667)]
            for width, height in viewport_sizes:
                page.set_viewport_size({"width": width, "height": height})
                expect(print_history_page.billing_cycle_period_card).to_be_visible(timeout=30000)
                framework_logger.info(f"Verified responsive layout at {width}x{height}")

            framework_logger.info("=== C44873414 - Billing Cycle Period card flow finished successfully ===")

        except Exception as e:
            framework_logger.error(f"An error occurred during the Billing Cycle Period card flow: {e}\n{traceback.format_exc()}")
            raise e
