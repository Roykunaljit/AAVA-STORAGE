"""
Additional locators and methods for PrintHistoryPage
Merge into: pages/print_history_page.py

Instructions:
1. Add locators to the Elements class in PrintHistoryPage
2. These locators support the Billing Cycle Period card test case C44873414
"""

# ══════════════════════════════════════════════════════════════════════════════
# ADD TO Elements CLASS IN PrintHistoryPage
# ══════════════════════════════════════════════════════════════════════════════

# Billing Cycle Period Card - Main Container
billing_cycle_period_card = "[data-testid='billing-cycle-card']"
billing_cycle_period_title = "[data-testid='billing-cycle-title']"

# Plan Pause Information
plan_pause_info_text = "[data-testid='plan-pause-info']