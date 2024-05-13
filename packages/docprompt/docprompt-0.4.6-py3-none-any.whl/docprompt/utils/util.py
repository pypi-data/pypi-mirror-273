from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import unquote, urlparse
import warnings

import fsspec
import magic

from docprompt.schema.document import PdfDocument
from docprompt._pdfium import get_pdfium_document


def is_pdf(fd: Union[Path, PathLike, bytes]) -> bool:
    """
    Determines if a file is a PDF
    """
    if isinstance(fd, (bytes, str)):
        mime = magic.from_buffer(fd, mime=True)
    else:
        with open(fd, "rb") as f:
            # We only need the first 1024 bytes to determine if it's a PDF
            mime = magic.from_buffer(f.read(1024), mime=True)

    return mime == "application/pdf"


def get_page_count(fd: Union[Path, PathLike, bytes]) -> int:
    """
    Determines the number of pages in a PDF
    """
    if not isinstance(fd, bytes):
        with open(fd, "rb") as f:
            fd = f.read()

    with get_pdfium_document(fd) as pdf:
        return len(pdf)


def name_from_path(path: Union[Path, PathLike]) -> str:
    if not isinstance(path, Path):
        path = Path(path)

    file_name = path.name

    parsed = urlparse(file_name)

    return unquote(parsed.path)


def read_pdf_bytes_from_path(path: Union[Path, PathLike], **kwargs) -> bytes:
    with fsspec.open(urlpath=str(path), mode="rb", **kwargs) as f:
        return f.read()


def determine_pdf_name_from_bytes(file_bytes: bytes) -> str:
    """
    Attempts to determine the name of a PDF by exaimining metadata
    """
    with get_pdfium_document(file_bytes) as pdf:
        metadata_dict = pdf.get_metadata_dict(skip_empty=True)

    name = None

    if metadata_dict:
        name = (
            metadata_dict.get("Title")
            or metadata_dict.get("Subject")
            or metadata_dict.get("Author")
        )

    if name:
        return f"{name.strip()}.pdf"

    return f"document-{hash_from_bytes(file_bytes)}.pdf"


def load_document(
    fp: Union[Path, PathLike, bytes],
    *,
    file_name: Optional[str] = None,
) -> PdfDocument:
    """
    Loads a document from a file path
    """
    if isinstance(fp, bytes):
        file_bytes = fp
        file_name = file_name or determine_pdf_name_from_bytes(file_bytes)
    else:
        file_name = name_from_path(fp) if file_name is None else file_name

        file_bytes = read_pdf_bytes_from_path(fp)

    if not is_pdf(file_bytes):
        raise ValueError("File is not a PDF")

    return PdfDocument(
        name=unquote(file_name), file_path=str(fp), file_bytes=file_bytes
    )


def load_documents(
    fps: List[Union[Path, PathLike, bytes]],
    *,
    max_threads: int = 12,
):
    """
    Loads multiple documents from file paths, using a thread pool
    """
    futures = []

    thread_count = min(max_threads, len(fps))

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for fp in fps:
            futures.append(executor.submit(load_document, fp))

    results = []

    for future in as_completed(futures):
        results.append(future.result())

    return results


def load_document_from_url(url: str, **kwargs):
    warnings.warn(
        "load_document_from_url is deprecated and will be removed in a future release. Use load_document instead.",
        DeprecationWarning,
    )
    return load_document(url, **kwargs)


def hash_from_bytes(
    byte_data: bytes, hash_func=hashlib.md5, threshold=1024 * 1024 * 128
) -> str:
    """
    Gets a hash from bytes. If the bytes are larger than the threshold, the hash is computed in chunks
    to avoid memory issues. The default hash function is MD5 with a threshold of 128MB which is optimal
    for most machines and use cases.
    """
    hash = hash_func()

    if len(byte_data) > threshold:
        stream = BytesIO(byte_data)
        b = bytearray(128 * 1024)
        mv = memoryview(b)

        while n := stream.readinto(mv):
            hash.update(mv[:n])
    else:
        hash.update(byte_data)

    return hash.hexdigest()
