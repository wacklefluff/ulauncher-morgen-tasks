"""
Ulauncher Morgen Tasks Extension
Manage Morgen tasks from Ulauncher - list, search, and create tasks
"""

import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)


class MorgenTasksExtension(Extension):
    """Main extension class for Morgen Tasks"""

    def __init__(self):
        super(MorgenTasksExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        logger.info("Morgen Tasks Extension initialized")


class KeywordQueryEventListener(EventListener):
    """Handles keyword query events"""

    def on_event(self, event, extension):
        """Handle keyword query event"""
        query = event.get_argument() or ""

        logger.info(f"Keyword triggered with query: '{query}'")

        # Get preferences
        api_key = extension.preferences.get("api_key", "")
        cache_ttl = extension.preferences.get("cache_ttl", "600")

        # For now, just show a welcome message
        items = []

        if not api_key:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Welcome to Morgen Tasks!',
                description='Please configure your API key in extension preferences',
                on_enter=HideWindowAction()
            ))
        else:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Morgen Tasks is working!',
                description=f'API key configured. Query: "{query}"',
                on_enter=HideWindowAction()
            ))

            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Cache TTL',
                description=f'Cache duration: {cache_ttl} seconds',
                on_enter=HideWindowAction()
            ))

        return RenderResultListAction(items)


if __name__ == '__main__':
    MorgenTasksExtension().run()
