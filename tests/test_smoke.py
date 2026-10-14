"""
Smoke Tests cho project_iaw.

=== SMOKE TEST LÀ GÌ? ===
Smoke test (hay "sanity test") là tầng test đơn giản nhất, chạy đầu tiên.
Mục đích: xác nhận rằng hệ thống "không bốc khói" (không bị vỡ hoàn toàn)
trước khi chạy các test chi tiết hơn.

Nếu smoke test fail → dừng ngay, không lãng phí thời gian chạy test sâu hơn.
Nếu smoke test pass → hệ thống đủ ổn định để test tiếp.

=== CÁC THƯ VIỆN ĐƯỢC SỬ DỤNG ===

1. importlib  (built-in)
   ──────────────────────
   Module cho phép import động (import theo tên string thay vì hardcode).
   importlib.import_module("tên_module") → tương đương với `import tên_module`
   Dùng trong smoke test để kiểm tra package có thể được import không,
   mà không cần biết trước nội dung bên trong.

2. importlib.metadata  (built-in, Python >= 3.8)
   ─────────────────────────────────────────────
   Đọc metadata của package được cài đặt (từ pyproject.toml / setup.py).
   version("tên-package") → trả về chuỗi version như "0.1.0"
   Dùng để kiểm tra package đã được cài đúng vào môi trường.

3. sys  (built-in)
   ─────────────────
   Cung cấp thông tin về Python interpreter đang chạy.
   sys.version_info → tuple (major, minor, micro, ...)
   sys.executable   → đường dẫn tới file python.exe đang dùng
   Dùng để smoke test môi trường Python.

4. types.ModuleType  (built-in)
   ────────────────────────────
   Type hint cho một module Python. Dùng để annotate biến chứa module
   trả về từ importlib.import_module(), giúp mypy kiểm tra kiểu dữ liệu.
"""

import importlib
import importlib.metadata
import sys
import types


class TestSmoke:
    """
    Smoke tests — chạy nhanh, kiểm tra các điều kiện cơ bản nhất.

    Thường được chạy đầu tiên trong CI/CD pipeline với lệnh:
        pytest tests/test_smoke.py -v
    """

    # ------------------------------------------------------------------
    # Môi trường Python
    # ------------------------------------------------------------------

    def test_python_version_is_312_or_higher(self) -> None:
        """
        Dự án yêu cầu Python >= 3.12 (khai báo trong pyproject.toml).
        Kiểm tra interpreter đang chạy phải đúng phiên bản.
        """
        major, minor = sys.version_info.major, sys.version_info.minor
        assert (major, minor) >= (3, 12), (
            f"Cần Python >= 3.12, đang dùng {major}.{minor}. "
            f"Interpreter: {sys.executable}"
        )

    # ------------------------------------------------------------------
    # Package có thể import được không?
    # ------------------------------------------------------------------

    def test_package_is_importable(self) -> None:
        """Package project_iaw phải import được mà không raise exception."""
        # importlib.import_module() sẽ raise ImportError nếu không tìm thấy
        module: types.ModuleType = importlib.import_module("project_iaw")
        assert module is not None

    def test_main_function_exists(self) -> None:
        """Hàm `main` phải tồn tại trong package project_iaw."""
        module: types.ModuleType = importlib.import_module("project_iaw")
        assert hasattr(module, "main"), (
            "Không tìm thấy hàm `main` trong package project_iaw"
        )

    def test_main_is_callable(self) -> None:
        """Hàm `main` phải là callable (có thể gọi được)."""
        module: types.ModuleType = importlib.import_module("project_iaw")
        assert callable(module.main), "`main` tồn tại nhưng không phải là callable"

    # ------------------------------------------------------------------
    # Package metadata
    # ------------------------------------------------------------------

    def test_package_version_exists(self) -> None:
        """
        Package phải có metadata version (được khai báo trong pyproject.toml).
        importlib.metadata.version() đọc thông tin từ package đã được cài.
        """
        try:
            ver = importlib.metadata.version("project-iaw")
            # version phải là chuỗi không rỗng
            assert isinstance(ver, str) and len(ver) > 0, (
                f"Version không hợp lệ: {ver!r}"
            )
        except importlib.metadata.PackageNotFoundError:
            # Package chưa được `pip install -e .` → skip thay vì fail
            import pytest

            pytest.skip(
                "Package 'project-iaw' chưa được cài vào môi trường. Chạy: uv sync"
            )
