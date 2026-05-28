from plugins.base_plugin.base_plugin import BasePlugin
import requests
import logging


logger = logging.getLogger(__name__)


class YoutubeSubsCount(BasePlugin):
    def _fetch_subscriber_count(self, api_key, channel_id):
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {
            "part": "statistics",
            "id": channel_id,
            "key": api_key,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise RuntimeError("YouTube API request timed out.") from exc
        except requests.exceptions.HTTPError as exc:
            content = exc.response.text if exc.response is not None else "No response content"
            raise RuntimeError(f"YouTube API HTTP error: {content}") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Failed to contact YouTube API: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise RuntimeError("YouTube API returned invalid JSON.") from exc

        items = data.get("items")
        if not isinstance(items, list) or not items:
            raise RuntimeError("Invalid response: could not find the YouTube channel.")

        statistics = items[0].get("statistics", {})
        subs = statistics.get("subscriberCount")
        if subs is None:
            raise RuntimeError("Invalid response: could not find subscriber count.")

        try:
            return int(subs)
        except (TypeError, ValueError) as exc:
            logger.error("Unexpected subscriberCount value: %r", subs)
            raise RuntimeError("Invalid response: subscriber count was not numeric.") from exc

    def generate_image(self, settings, device_config):
        api_key = device_config.load_env_key("YOUTUBE_API_KEY")
        custom_text = settings.get("custom_text", "SUBSCRIBERS").strip() or "SUBSCRIBERS"
        channel_id = settings.get("channel_id", "").strip()

        if not api_key:
            raise RuntimeError(
                "Missing YouTube API key. Add a key named YOUTUBE_API_KEY in the InkyPi key settings."
            )
        if not channel_id:
            raise RuntimeError("Missing channel ID in plugin settings.")

        subs = self._fetch_subscriber_count(api_key, channel_id)

        dimensions = device_config.get_resolution()

        template_params = {
            "title": custom_text,
            "subscriber_count": f"{subs:,}",
            "logo_path": self.get_plugin_dir("resources/youtube-logo.png"),
            "plugin_settings": settings,
        }

        image = self.render_image(
            dimensions,
            "youtube_subs.html",
            "youtube_subs.css",
            template_params,
        )

        if not image:
            raise RuntimeError("Failed to take screenshot, please check logs.")

        return image

    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params["custom_text"] = "SUBSCRIBERS"
        template_params["channel_id"] = ""
        template_params["style_settings"] = True
        return template_params