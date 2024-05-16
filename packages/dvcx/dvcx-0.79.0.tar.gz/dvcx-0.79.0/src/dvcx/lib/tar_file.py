from dvcx.client.fileslice import FileSlice
from dvcx.lib.file import File, VFile, VFileError, VFileRegistry


class TarVFile(VFile):
    @classmethod
    def get_vtype(cls) -> str:
        return "tar"

    @classmethod
    def open(cls, file: File, location: list[dict]):
        if len(location) > 1:
            VFileError(file, "multiple 'location's are not supported yet")

        loc = location[0]

        if (offset := loc.get("offset", None)) is None:
            VFileError(file, "'offset' is not specified")

        if (size := loc.get("size", None)) is None:
            VFileError(file, "'size' is not specified")

        if (parent := loc.get("parent", None)) is None:
            VFileError(file, "'parent' is not specified")

        tar_file = File(**parent)
        tar_file.set_catalog(file._catalog)

        tar_file_uid = tar_file.get_uid()
        client = file._catalog.get_client(tar_file_uid.storage)
        fd = client.open_object(tar_file_uid, use_cache=file._caching_enabled)
        return FileSlice(fd, offset, size, file.name)


VFileRegistry.register(TarVFile)
