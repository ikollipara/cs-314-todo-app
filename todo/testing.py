"""
django_playwright.py
Ian Kollipara <ian.kollipara@gmail.com>
2025-02-25

Django ❤️ Playwright
"""

from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from playwright.sync_api import Browser as _Browser
from playwright.sync_api import ViewportSize, expect, sync_playwright

Browser = Literal["chromium", "firefox", "webkit"]


class E2ETestCase(LiveServerTestCase):
    """End-to-end Test Case.

    Builds on Django's Live Server Test Case with Playwright to allow
    for rich E2E testing.
    """

    # Configuration Options
    headless: bool = True
    browser: Browser
    timeout: int = 30 * 1000
    viewport: ViewportSize = None
    device: str = None
    expect = expect

    def setUp(self):
        super().setUp()

        self._browser: _Browser = getattr(self.playwright, self.browser).launch(
            timeout=self.timeout, headless=self.headless
        )

        # We use a context over a regular page since a context allows
        # for tracing
        self.ctx = self._browser.new_context(
            **(
                self.playwright.devices[self.device]
                if self.device in self.playwright.devices
                else {"viewport": self.viewport}
            )
        )

        self.page = self.ctx.new_page()

        self.addCleanup(self._browser.close)
        self.addCleanup(self.ctx.close)
        self.addCleanup(self.page.close)

    @contextmanager
    def trace(
        self, save_path: Path | str, *, screenshots: bool = True, snapshots: bool = True
    ):
        """Create a trace of the particular actions. Save to the given path."""
        try:
            self.ctx.tracing.start(screenshots=screenshots, snapshots=snapshots)
            yield
        finally:
            self.ctx.tracing.stop(path=save_path)

    def run(self, result=None):
        with sync_playwright() as playwright:
            self.playwright = playwright
            return super().run(result)


class StaticE2ETestCase(StaticLiveServerTestCase):
    """End-to-end Test Case.

    Builds on Django's Static Live Server Test Case with Playwright to allow
    for rich E2E testing.
    """

    # Configuration Options
    headless: bool = True
    browser: Browser
    viewport: ViewportSize = None
    device: str = None

    def setUp(self):
        super().setUp()

        self._browser: _Browser = getattr(self.playwright, self.browser).launch(
            timeout=self.timeout, headless=self.headless
        )

        # We use a context over a regular page since a context allows
        # for tracing
        self.ctx = self._browser.new_context(
            **(
                self.playwright.devices[self.device]
                if self.device in self.playwright.devices
                else {"viewport": self.viewport}
            )
        )

        self.page = self.ctx.new_page()

        self.addCleanup(self._browser.close)
        self.addCleanup(self.ctx.close)
        self.addCleanup(self.page.close)

    @contextmanager
    def trace(
        self, save_path: Path | str, *, screenshots: bool = True, snapshots: bool = True
    ):
        """Create a trace of the particular actions. Save to the given path."""
        try:
            self.ctx.tracing.start(screenshots=screenshots, snapshots=snapshots)
            yield
        finally:
            self.ctx.tracing.stop(path=save_path)

    def run(self, result=None):
        with sync_playwright() as playwright:
            self.playwright = playwright
            return super().run(result)
