import os
import logging
from django.conf import settings
from django.core.files.storage import Storage, FileSystemStorage
from django.utils.deconstruct import deconstructible

logger = logging.getLogger(__name__)

@deconstructible
class ImageKitStorage(Storage):
    """
    Custom Django Storage backend that uploads media files to ImageKit.io Cloud Storage.
    Falls back gracefully to FileSystemStorage if ImageKit credentials are not configured.
    """

    def __init__(self, **kwargs):
        self.public_key = getattr(settings, 'IMAGEKIT_PUBLIC_KEY', '') or os.getenv('IMAGEKIT_PUBLIC_KEY', '')
        self.private_key = getattr(settings, 'IMAGEKIT_PRIVATE_KEY', '') or os.getenv('IMAGEKIT_PRIVATE_KEY', '')
        self.url_endpoint = (getattr(settings, 'IMAGEKIT_URL_ENDPOINT', '') or os.getenv('IMAGEKIT_URL_ENDPOINT', '')).rstrip('/')
        self.fallback_storage = FileSystemStorage()
        self._client = None

    @property
    def is_configured(self):
        return bool(self.private_key and self.url_endpoint)

    @property
    def client(self):
        if self._client is None and self.is_configured:
            try:
                from imagekitio import ImageKit
                self._client = ImageKit(private_key=self.private_key)
            except Exception as e:
                logger.error(f"Failed to initialize ImageKit client: {e}")
                self._client = None
        return self._client

    def _save(self, name, content):
        """
        Upload the file to ImageKit if configured; otherwise use FileSystemStorage.
        """
        if not self.is_configured or not self.client:
            logger.info("ImageKit credentials not configured. Storing locally with FileSystemStorage.")
            return self.fallback_storage._save(name, content)

        try:
            # Read content bytes
            content.seek(0)
            file_bytes = content.read()

            filename = os.path.basename(name)
            # Upload to ImageKit cloud
            upload_response = self.client.files.upload(
                file=file_bytes,
                file_name=filename,
                folder="/tweeter_photos",
                use_unique_file_name=True,
            )

            # Store the full CDN url or remote path returned by ImageKit
            if hasattr(upload_response, 'url') and upload_response.url:
                return upload_response.url
            elif hasattr(upload_response, 'file_path') and upload_response.file_path:
                return upload_response.file_path.lstrip('/')
            return name
        except Exception as e:
            logger.error(f"Error uploading image to ImageKit: {e}. Falling back to local storage.")
            content.seek(0)
            return self.fallback_storage._save(name, content)

    def url(self, name):
        """
        Returns the absolute URL for the image on ImageKit CDN or local fallback.
        """
        if not name:
            return ""

        # If name is already a full ImageKit or web URL
        if name.startswith('http://') or name.startswith('https://'):
            return name

        # If ImageKit endpoint is configured
        if self.url_endpoint:
            clean_path = name.lstrip('/')
            return f"{self.url_endpoint}/{clean_path}"

        # Otherwise fallback to local URL
        try:
            return self.fallback_storage.url(name)
        except Exception:
            return f"{settings.MEDIA_URL}{name}"

    def exists(self, name):
        if not self.is_configured:
            return self.fallback_storage.exists(name)
        # ImageKit auto-generates unique names when configured
        return False

    def delete(self, name):
        if not self.is_configured:
            return self.fallback_storage.delete(name)
        # ImageKit remote deletion can be added here if file_id is maintained
        pass
