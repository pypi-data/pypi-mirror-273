from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.contrib.staticfiles.storage import (
    ManifestStaticFilesStorage,
    StaticFilesStorage,
    staticfiles_storage,
)

from supercollect.utils import get_all_files


class Command(collectstatic.Command):
    """
    Uses FileSystemStorage to collect and post-process files.
    Then, files are uploaded.
    This significantly speeds up the process for remote locations.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--turbo",
            action="store_true",
            help="Use turbo mode.",
        )

    def set_options(self, **options):
        super().set_options(**options)
        self.turbo = options["turbo"]

    def collect(self):
        manifest_deployment, temp_storage = False, None

        if self.turbo:
            if hasattr(staticfiles_storage, "manifest_version"):
                manifest_deployment = True

            self.storage = temp_storage = (
                ManifestStaticFilesStorage(location=settings.STATIC_ROOT)
                if manifest_deployment
                else StaticFilesStorage(location=settings.STATIC_ROOT)
            )

        collected = super().collect()
        if not self.turbo:
            return collected

        self.storage = staticfiles_storage
        with ThreadPoolExecutor(max_workers=32) as executor:
            for file in get_all_files(temp_storage):
                executor.submit(self.upload, file, temp_storage)

        return collected

    def handle(self, **options):
        report = super().handle(**options)
        return "Super.collected()" if self.turbo else report

    def upload(self, path, source_storage):
        with source_storage.open(path) as source_file:
            self.storage.save(path, source_file)
