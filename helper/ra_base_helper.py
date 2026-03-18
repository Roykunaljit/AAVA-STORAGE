"""Rails Admin Base Helper module.

Provides utility methods for interacting with Rails Admin interface.
"""

from core.settings import framework_logger


class RABaseHelper:
    """Static helper class for Rails Admin base operations."""

    @staticmethod
    def click_tenant_link(page, tenant_email):
        """Click the tenant link in Rails Admin search results.
        
        Args:
            page: Playwright page object
            tenant_email: Email address of the tenant to click
        """
        framework_logger.info(f"Clicking tenant link for {tenant_email}")
        page.locator(f"a:has-text('{tenant_email}')").first.click()

    @staticmethod
    def click_edit_link(page):
        """Click the Edit link in Rails Admin.
        
        Args:
            page: Playwright page object
        """
        framework_logger.info("Clicking Edit link")
        page.locator("a:has-text('Edit')").click()

    @staticmethod
    def access_page(page, page_name):
        """Navigate to a specific page by clicking a navigation link.
        
        Args:
            page: Playwright page object
            page_name: Name of the page to navigate to
        """
        framework_logger.info(f"Navigating to {page_name} page")
        page.locator(f'//a[@class="nav-link" and normalize-space(text())="{page_name}"]').click()

    @staticmethod
    def get_item_by_title(page, title):
        """Locate and return a card body element by searching for a card with a specific title.
        
        Args:
            page: Playwright page object
            title: Title text to search for
            
        Returns:
            Locator for the card body element
        """
        card = page.locator(f'div.card:has(h5.card-header:text-is("{title}"), h5.card-header a:text-is("{title}"))')
        if card.count() == 0:
            page.wait_for_selector(f'div.card:has(h5.card-header:text-is("{title}"))', timeout=10000)
        if card.count() == 0:
            raise ValueError(f"Field with title '{title}' not found")
        return card.locator('div.card-body')

    @staticmethod
    def get_field_text_by_title(page, title):
        """Retrieve the text content from a field within a card section.
        
        Args:
            page: Playwright page object
            title: Title of the field to retrieve
            
        Returns:
            Text content of the field
        """
        field = RABaseHelper.get_item_by_title(page, title)
        return field.inner_text().strip()

    @staticmethod
    def wait_page_to_load(page, page_title, timeout=60000):
        """Wait for a specific page to fully load.
        
        Args:
            page: Playwright page object
            page_title: Title of the page to wait for
            timeout: Timeout in milliseconds (default 60000)
        """
        framework_logger.info(f"Waiting for page '{page_title}' to load")
        page.wait_for_selector(f'h1:has-text("Details for {page_title}")', timeout=timeout)
