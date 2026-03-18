"""Test Case C44873414 - Billing Cycle Period card.

Verifies Billing Cycle Period card display and behavior on Print and Payment History page
when subscription plan is paused, including complimentary pages progress bar, additional
pages tracking, tooltips, and page usage information across different printing scenarios.

Test Case ID: C44873414
Module: HP Instant Ink
Priority: P2
Test Type: Regression
"""

import traceback

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from playwright.sync_api import expect

from core.playwright_manager import PlaywrightManager
from core.settings import framework_logger

from pages.dashboard_side_menu_page import DashboardSideMenuPage
from pages.print_history_page import PrintHistoryPage

from helper.dashboard_helper import DashboardHelper
from helper.enrollment_helper import EnrollmentHelper
from helper.gemini_ra_helper import GeminiRAHelper
from helper.ra_base_helper import RABaseHelper

import test_flows_common.test_flows_common as common


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
            printer_data = common.create_and_claim_virtual_printer_and_add_address()
            EnrollmentHelper.start_enrollment_and_sign_in(page, tenant_email)
            EnrollmentHelper.select_printer(page, printer_index=0)
            EnrollmentHelper.select_plan(page, plan_pages=50)
            EnrollmentHelper.finish_enrollment(page)
            
            # Precondition 2 & 3: Ensure subscription is in subscribed status without free months
            org_token, tenant_id = common.get_org_aware_token(tenant_email)
            subscription_data = common.subscription_data_from_gemini(tenant_id)
            subscription_id = subscription_data['id']
            free_months = subscription_data.get('free_months')
            assert free_months is None or free_months == 0, f"Subscription has free months: {free_months}"
            common.validate_subscription_state(subscription_id, 'subscribed')
            framework_logger.info("Preconditions 1-3 completed: Enrollment with 50 pages plan, verified subscribed status without free months")
            
            # Precondition 4: Pause the plan via Rails Admin
            GeminiRAHelper.access(page)
            GeminiRAHelper.access_tenant_page(page, tenant_email)
            # Navigate to subscription edit and manually pause
            # TODO: Implement pause_subscription method in GeminiRAHelper or use UI navigation
            framework_logger.info("Precondition 4: Navigated to tenant page for manual pause")

            # ══════════════════════════════════════════════
            # PRECONDITION SETUP COMPLETE - TEST STEPS BEGIN
            # ══════════════════════════════════════════════

            # Step 1: Go to Print and Payment History page under HP Instant Ink
            DashboardHelper.access(page, tenant_email)
            side_menu = DashboardSideMenuPage(page)
            side_menu.click_print_history()
            page.wait_for_load_state("networkidle", timeout=30000)
            framework_logger.info("Step 1: Navigated to Print and Payment History page")

            print_history_page = PrintHistoryPage(page)

            # Step 2: Check the Billing Cycle Period card - verify plan pause info NOT displayed
            expect(print_history_page.print_history_card).to_be_visible(timeout=30000)
            expect(print_history_page.plan_pause_info).not_to_be_visible(timeout=30000)
            framework_logger.info("Step 2: Verified plan pause information is not displayed")

            # Step 3: Event shift 32 days and trigger billing charge
            framework_logger.info("Step 3: Shifting time by 32 days and triggering billing")
            GeminiRAHelper.access(page)
            GeminiRAHelper.access_tenant_page(page, tenant_email)
            GeminiRAHelper.event_shift(page, event_shift=32, force_billing=True)
            subscription_data_after_shift = common.subscription_data_from_gemini(tenant_id)
            framework_logger.info("Step 3: Time shifted 32 days and billing triggered successfully")

            # Step 4: Go to Print and Payment History page again
            DashboardHelper.access(page, tenant_email)
            side_menu = DashboardSideMenuPage(page)
            side_menu.click_print_history()
            page.wait_for_load_state("networkidle", timeout=30000)
            framework_logger.info("Step 4: Navigated to Print and Payment History page after time shift")

            # Step 5: Check the Billing Cycle Period card - verify plan pause info IS displayed
            expect(print_history_page.print_history_card).to_be_visible(timeout=30000)
            expect(print_history_page.plan_pause_info).to_be_visible(timeout=30000)
            framework_logger.info("Step 5: Verified plan pause information is displayed")

            # Step 6: Check the progress bar - verify Complimentary pages progress bar displayed
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            framework_logger.info("Step 6: Verified Complimentary pages progress bar is displayed")

            # Step 7: Hover/click info icon and verify tooltip (device-specific)
            device_type = common.GlobalState.device_type if hasattr(common, 'GlobalState') else 'desktop'
            if device_type == 'mobile' or device_type == 'tablet':
                print_history_page.complimentary_pages_info_icon.click()
            else:
                print_history_page.complimentary_pages_info_icon.hover()
            expect(print_history_page.complimentary_pages_tooltip).to_be_visible(timeout=10000)
            expect(print_history_page.complimentary_pages_tooltip).not_to_be_empty(timeout=30000)
            framework_logger.info("Step 7: Verified tooltip displays with message")

            # Step 8: Check Complimentary pages value
            expect(print_history_page.complimentary_pages_value).to_contain_text("0 of 10", timeout=30000)
            expect(print_history_page.complimentary_pages_value).to_contain_text("Pause Plan", timeout=30000)
            framework_logger.info("Step 8: Verified Complimentary pages value: 0 of 10(Pause Plan) used")

            # Step 9: Check message below Complimentary pages
            expect(print_history_page.complimentary_pages_info_message).to_be_visible(timeout=30000)
            expect(print_history_page.complimentary_pages_info_message).not_to_be_empty(timeout=30000)
            framework_logger.info("Step 9: Verified information message with plan info")

            # Step 10: Print 6 pages (less than plan limit)
            for _ in range(6):
                common.send_rtp_devicestatus(
                    entity_id=printer_data.entity_id,
                    cloud_id=printer_data.cloud_id,
                    device_uuid=printer_data.device_uuid
                )
                page.wait_for_timeout(1000)
            page.wait_for_timeout(5000)
            subscription_data_step10 = common.subscription_data_from_gemini(tenant_id)
            pages_printed = subscription_data_step10.get('pages_printed', subscription_data_step10.get('page_count', 0))
            assert pages_printed >= 6, f"Expected at least 6 pages printed, got {pages_printed}"
            framework_logger.info("Step 10: Simulated printing 6 pages")

            # Step 11: Refresh page and verify progress bar updated
            page.reload()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            bar_color = print_history_page.complimentary_pages_progress_bar.evaluate("el => window.getComputedStyle(el).backgroundColor")
            assert "rgb(0, 0, 0)" in bar_color or "black" in bar_color.lower(), f"Expected black color, got {bar_color}"
            expect(print_history_page.complimentary_pages_value).to_contain_text("6", timeout=30000)
            framework_logger.info("Step 11: Verified progress bar filled with black color and updated to 6 of 10 used")

            # Step 12: Print 9 more pages (total 15, exceeding limit)
            for _ in range(9):
                common.send_rtp_devicestatus(
                    entity_id=printer_data.entity_id,
                    cloud_id=printer_data.cloud_id,
                    device_uuid=printer_data.device_uuid
                )
                page.wait_for_timeout(1000)
            page.wait_for_timeout(5000)
            subscription_data_step12 = common.subscription_data_from_gemini(tenant_id)
            pages_printed = subscription_data_step12.get('pages_printed', subscription_data_step12.get('page_count', 0))
            assert pages_printed >= 15, f"Expected at least 15 pages printed, got {pages_printed}"
            framework_logger.info("Step 12: Printed 9 additional pages (15 total) exceeding complimentary limit")

            # Step 13: Refresh and verify both progress bars displayed
            page.reload()
            page.wait_for_load_state("domcontentloaded", timeout=30000)
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            expect(print_history_page.additional_pages_progress_bar).to_be_visible(timeout=30000)
            framework_logger.info("Step 13: Verified both Complimentary and Additional pages progress bars displayed")

            # Step 14: Check Additional pages progress bar color and value
            expect(print_history_page.additional_pages_progress_bar).to_be_visible(timeout=30000)
            bar_color = print_history_page.additional_pages_progress_bar.evaluate("el => window.getComputedStyle(el).backgroundColor")
            assert "rgb(255, 255, 0)" in bar_color or "yellow" in bar_color.lower(), f"Expected yellow color, got {bar_color}"
            expect(print_history_page.additional_pages_value).to_contain_text("5 of 10", timeout=30000)
            framework_logger.info("Step 14: Additional pages progress bar verified as yellow with value 5 of 10 used")

            # Step 15: Check info icon for Additional pages
            expect(print_history_page.additional_pages_info_icon).to_be_visible(timeout=30000)
            framework_logger.info("Step 15: Verified info icon displayed for Additional pages")

            # Step 16: Hover/click Additional pages info icon and verify tooltip (device-specific)
            if device_type == 'mobile' or device_type == 'tablet':
                print_history_page.additional_pages_info_icon.click()
            else:
                print_history_page.additional_pages_info_icon.hover()
            expect(print_history_page.additional_pages_tooltip).to_be_visible(timeout=10000)
            expect(print_history_page.additional_pages_tooltip).not_to_be_empty(timeout=30000)
            framework_logger.info("Step 16: Additional pages tooltip verified")

            # Step 17: Check message below Additional pages
            expect(print_history_page.additional_pages_info_message).to_be_visible(timeout=30000)
            expect(print_history_page.additional_pages_info_message).to_contain_text("block", timeout=30000)
            framework_logger.info("Step 17: Verified message with blocks bought information")

            # Step 18: Verify Complimentary pages progress bar is full
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            bar_color = print_history_page.complimentary_pages_progress_bar.evaluate("el => window.getComputedStyle(el).backgroundColor")
            assert "rgb(0, 0, 0)" in bar_color or "black" in bar_color.lower(), f"Expected black color, got {bar_color}"
            bar_width = print_history_page.complimentary_pages_progress_bar.evaluate("el => window.getComputedStyle(el).width")
            parent_width = print_history_page.complimentary_pages_progress_bar.evaluate("el => window.getComputedStyle(el.parentElement).width")
            assert bar_width == parent_width, f"Progress bar not full: {bar_width} vs {parent_width}"
            expect(print_history_page.complimentary_pages_value).to_contain_text("10 of 10", timeout=30000)
            framework_logger.info("Step 18: Complimentary pages progress bar full (10 of 10)")

            # Step 19: Check total pages printed
            billing_card = print_history_page.billing_cycle_period_card
            total_pages_element = print_history_page.total_printed_pages
            expect(total_pages_element).to_be_visible(timeout=30000)
            total_pages_text = total_pages_element.text_content()
            assert "15" in total_pages_text, f"Expected 15 pages in total, got: {total_pages_text}"
            framework_logger.info("Step 19: Verified total pages printed")

            # Step 20: Visual verification - screenshot captured
            expect(billing_card).to_be_visible(timeout=30000)
            billing_card.screenshot(path="screenshots/billing_cycle_card_visual.png")
            expect(print_history_page.complimentary_pages_progress_bar).to_be_visible(timeout=30000)
            expect(print_history_page.additional_pages_progress_bar).to_be_visible(timeout=30000)
            expect(print_history_page.complimentary_pages_info_icon).to_be_visible(timeout=30000)
            expect(print_history_page.additional_pages_info_icon).to_be_visible(timeout=30000)
            framework_logger.info("Step 20: Screenshot captured for visual verification")

            # Step 21: Responsive verification across viewports
            viewport_sizes = [(1920, 1080), (768, 1024), (375, 667)]
            for width, height in viewport_sizes:
                page.set_viewport_size({"width": width, "height": height})
                page.wait_for_load_state("networkidle", timeout=10000)
                expect(billing_card).to_be_visible(timeout=30000)
            framework_logger.info("Step 21: Verified responsive layout at all viewports")

            framework_logger.info("=== C44873414 - Billing Cycle Period card flow finished successfully ===")

        except Exception as e:
            framework_logger.error(f"An error occurred during the Billing Cycle Period card flow: {e}\n{traceback.format_exc()}")
            raise e
