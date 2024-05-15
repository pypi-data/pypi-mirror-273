def get_all_files(storage):
    def collect(dirname=""):
        dirs, files = storage.listdir(dirname)
        for file in files:
            yield f"{dirname}/{file}" if dirname else file
        for dir in dirs:
            yield from collect(dir if not dirname else f"{dirname}/{dir}")

    return collect()
