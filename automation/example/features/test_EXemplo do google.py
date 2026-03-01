import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/?zx=1772367123768&no_sw_cr=1")
    page.get_by_role("combobox", name="Pesquisar").click()
    page.get_by_role("combobox", name="Pesquisar").fill("mouse preço")
    page.get_by_role("combobox", name="Pesquisar").click()
    page.locator("iframe[name=\"a-jw4ginhtassn\"]").content_frame.get_by_role("checkbox", name="Não sou um robô").click()
    page.locator("iframe[name=\"c-jw4ginhtassn\"]").content_frame.locator("[id=\"0\"]").click()
    page.locator("iframe[name=\"c-jw4ginhtassn\"]").content_frame.locator("[id=\"7\"]").click()
    page.locator("iframe[name=\"c-jw4ginhtassn\"]").content_frame.locator("[id=\"5\"]").click()
    page.locator("iframe[name=\"c-jw4ginhtassn\"]").content_frame.get_by_role("button", name="Verificar").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
