import asyncio
from pathlib import Path
import time
from typing import Callable
from playwright.async_api import async_playwright, Playwright




key = 'MjZmZWU0MTEtNWE5NC00MjM0LWEwN2YtOGNmMjE1Y2I1ZDQxfEFub258N3wyMTE1NTY4OTUzNzgzNnwxMzM2MzU3NTEzNTAyfDEsMTF8NTAwMDAwMDAwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDF8MXwwfDF8ODcyNzcxMTJ8MXwxfDB8MXwwfDF8MXwxfDF8MXwxfDF8MXwxfDF8MXwxfDB8MHwwfDB8MHwwfDB8MHwxNzgxODc5ODQxOTkxNjR8MzYyMTkyNDQzMzg3N3w3MjF8MHw1MDAwMDAwMDB8MTg4OTk0MHwwfDF8MHwxfDF8MHwxfDF8MXwxfDB8MXwxfDF8MHwwfDF8MXwxfDB8MXwxfDF8MXwwfDF8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MHwwfDB8MCwwLDAsMCwwLDAsMCwwLDAsMCwwLDB8MHwwfDE3Njg2MzU3ODk4Nzh8MA=='

execution_path = Path(__file__).parent.absolute()
key_file_path = Path(execution_path / 'string.txt').absolute()
if not key_file_path.exists():
    key = ''
    key_file_writer = open(file=key_file_path, mode='w', encoding='utf-8')
    key_file_writer.write(key)

key_file_reader = open(file=key_file_path, mode='r', encoding='utf-8')
key = key_file_reader.read()



async def cook_meth(**kwargs):
    click_count = kwargs['click_count']
    button_locator = page.locator("iframe").content_frame.locator("#METH")
    await button_locator.click(click_count=click_count)


async def sell_meth(**kwargs):
    click_count = kwargs['click_count']
    button_locator = page.locator("iframe").content_frame.locator("#CASH")
    await button_locator.click(click_count=click_count)


async def buy_something(**kwargs):
    option = kwargs['option']
    click_count = kwargs['click_count']
    option_has_button = kwargs['option_has_button'] or False

    button_locator = page.locator("iframe").content_frame.locator(f"#OPT{option} > #button").first if option_has_button else page.locator("iframe").content_frame.locator(f"#OPT{option}")

    return await button_locator.click(click_count=click_count) if (
        await button_locator.is_enabled()
        or await button_locator.is_visible()
    ) else None



async def stop_dealers(**kwargs):
    await page.locator("iframe").content_frame.locator("#OPTS1 #button").click()


async def change_tab(**kwargs):
    option = kwargs['option']
    tab = page.locator("iframe").content_frame.locator(f"#TABS{option}")
    await tab.click()
    


async def import_game(save_string: str):
    async def handle_dialog(dialog):
        await dialog.accept(save_string)

    page.once("dialog", handle_dialog)

    frame_locator = page.frame_locator("iframe")
    await frame_locator.locator('a[onclick="importgame();"]').click()


async def export_game():
    dialog_done = asyncio.Event()

    async def handle_dialog(dialog):
        string = dialog.default_value if dialog.type == "prompt" else dialog.message
        if dialog.type == "prompt":
            await dialog.accept(dialog.default_value)
        else:
            await dialog.accept()

        with open(key_file_path, mode="w", encoding="utf-8") as key_file_writer:
            key_file_writer.write(string)
        
        dialog_done.set()

    page.once("dialog", handle_dialog)
    frame_locator = page.frame_locator("iframe")
    await frame_locator.locator('a[onclick="exportgame();"]').click()
    await dialog_done.wait()
    
    
async def save_game():
    nth_child_locator = page.locator("iframe").content_frame.locator("a:nth-child(10)")
    await nth_child_locator.click()


async def do(action: Callable, sequence: (int | float) = None, **kwargs):
    if sequence is not None:
        start_time = time.monotonic()
        end_time = time.monotonic() + sequence * 60
        last_print = -1
        while time.monotonic() < end_time:
            elapsed = int(time.monotonic() - start_time)
            remaining = max(0, int(end_time - time.monotonic()))
            if elapsed != last_print:
                print(f'[loop]\t{elapsed}s, {remaining}s', flush=True)
                last_print = elapsed
            await action(**kwargs)
    else:
        await action(**kwargs)


async def run(playwright: Playwright):
    global browser
    global page

    url = 'https://drmeth.com/'
    
    properties = {
        'headless': False,
        #'slow_mo': 50
    }
    browser = await playwright.chromium.launch(**properties)
    page = await browser.new_page()
    await page.goto(url)

    try:
        while True:

            await do(action=import_game, save_string=key)
            
            await do(action=change_tab, option=2)
            await do(action=buy_something, sequence=15, option='B1', option_has_button=False, click_count=1000)
            await do(action=stop_dealers)
            await do(action=save_game)
            await do(action=export_game)

            exit()

    except (asyncio.CancelledError, KeyboardInterrupt):
        await do(action=stop_dealers)
        await do(action=save_game)
        await do(action=export_game)

async def main():
    async with async_playwright() as playwright:
        try:
            await run(playwright)
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass


if __name__ == '__main__':
    asyncio.run(main())
