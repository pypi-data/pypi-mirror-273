from openi import FileProgressBar

pbar = FileProgressBar("sample.zip", 1024 * 1024 * 64)
pbar.update(1024 * 1024 * 32)
