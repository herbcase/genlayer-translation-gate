from pathlib import Path
import os
import pytest
from gltest.direct import sdk_loader

# Keep SDK downloads inside the checkout. Override to reuse an existing cache.
sdk_loader.CACHE_DIR = Path(os.environ.get("GLTEST_SDK_CACHE", Path(__file__).parents[1] / ".cache" / "gltest-direct"))
SDK_VERSION = "v0.2.16"


@pytest.fixture(autouse=True)
def windows_stdin_compat(monkeypatch):
    """gltest 0.29.2 unlinks fd-0's file while open, which Windows forbids.

    Defer only that WinError 32 cleanup until the VM restores stdin. Contract
    execution, SDK storage, calldata and validator behavior remain unchanged.
    """
    if os.name != "nt":
        yield
        return
    from gltest.direct import loader
    original = loader._inject_message_to_fd0
    deferred = []

    def inject(vm):
        try:
            original(vm)
        except PermissionError as exc:
            if exc.winerror != 32 or getattr(vm, "_original_stdin_fd", None) is None:
                raise
            deferred.append(Path(exc.filename))

    monkeypatch.setattr(loader, "_inject_message_to_fd0", inject)
    yield
    for path in deferred:
        path.unlink(missing_ok=True)


@pytest.fixture
def gate(direct_deploy):
    path = Path(__file__).parents[1] / "contracts" / "translation_gate.py"
    return direct_deploy(str(path), sdk_version=SDK_VERSION)
