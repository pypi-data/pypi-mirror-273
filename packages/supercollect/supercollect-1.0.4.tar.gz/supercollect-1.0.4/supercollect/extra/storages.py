import json
from urllib.parse import unquote, urldefrag, urlsplit, urlunsplit

from django.conf import settings
from storages.backends.s3 import S3StaticStorage


class ABDeploymentManifestFileMixin:
    """
    staticfiles.json => active
    staticfiles_inactive.json => inactive, ready to be claimed
    staticfiles_archived.json => cleanup on next run

    USE_INACTIVE = False => which file is being read
    CLAIM_INACTIVE = False =>
        staticfiles.json -> staticfiles_archived.json
        staticfiles_inactive.json -> staticfiles.json
    """

    manifest_version = "1.1"  # the manifest format standard
    manifest_active_name = "staticfiles.json"
    manifest_inactive_name = "staticfiles_inactive.json"
    manifest_archive_name = "staticfiles_archived.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.claim_manifest = settings.SUPERCOLLECT_AB_CLAIM_INACTIVE
        self.read_manifest_name = (
            self.manifest_inactive_name
            if self.claim_manifest
            else self.manifest_active_name
        )
        self.hashed_files = self.load_manifest()

    def read_manifest(self, name: str):
        try:
            with self.open(name) as manifest:
                return manifest.read().decode()
        except FileNotFoundError:
            return None

    def perform_claim(self):
        # Mark old (currently active) manifest file as archived for cleanup
        old_manifest = self.read_manifest(self.manifest_active_name)
        if old_manifest:
            self._save(self.manifest_archive_name, old_manifest)

        # Mark claimed manifest as active
        self._save(self.manifest_active_name, self.manifest)

    def load_manifest(self):
        manifest = self.read_manifest(self.read_manifest_name)
        if manifest is None:
            return {}

        if self.claim_manifest:
            self.perform_claim()

        try:
            stored = json.loads(manifest)
        except json.JSONDecodeError:
            pass
        else:
            version = stored.get("version")
            if version in ("1.0", "1.1"):
                return stored.get("paths", {})

        raise ValueError(
            "Couldn't load manifest '%s' (version %s)"
            % (self.read_manifest_name, self.manifest_version)
        )

    def save_manifest(self, file):
        if self.exists(self.manifest_inactive_name):
            self.delete(self.manifest_inactive_name)
        self._save(self.manifest_inactive_name, file)

    def stored_name(self, name):
        parsed_name = urlsplit(unquote(name))
        clean_name = parsed_name.path.strip()
        cache_name = self.hashed_files.get(clean_name, None)
        if cache_name is None:
            raise ValueError("Missing staticfiles manifest entry for '%s'" % clean_name)
        unparsed_name = list(parsed_name)
        unparsed_name[2] = cache_name
        # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        if "?#" in name and not unparsed_name[3]:
            unparsed_name[2] += "?"
        return urlunsplit(unparsed_name)

    def _url(self, hashed_name_func, name, force=False):
        """
        Return the non-hashed URL in DEBUG mode.
        """
        if settings.DEBUG and not force:
            hashed_name, fragment = name, ""
        else:
            clean_name, fragment = urldefrag(name)
            if urlsplit(clean_name).path.endswith("/"):  # don't hash paths
                hashed_name = name
            else:
                hashed_name = hashed_name_func(name)

        final_url = super().url(hashed_name)

        # Special casing for a @font-face hack, like url(myfont.eot?#iefix")
        # http://www.fontspring.com/blog/the-new-bulletproof-font-face-syntax
        query_fragment = "?#" in name  # [sic!]
        if fragment or query_fragment:
            urlparts = list(urlsplit(final_url))
            if fragment and not urlparts[4]:
                urlparts[4] = fragment
            if query_fragment and not urlparts[3]:
                urlparts[2] += "?"
            final_url = urlunsplit(urlparts)

        return unquote(final_url)

    def url(self, name, force=False):
        """
        Return the non-hashed URL in DEBUG mode.
        """
        return self._url(self.stored_name, name, force)


class S3ManifestStaticStorageAB(ABDeploymentManifestFileMixin, S3StaticStorage):
    pass
