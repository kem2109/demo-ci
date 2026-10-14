"""
conftest.py - Pytest configuration và shared fixtures.

File này được pytest tự động load, dùng để:
- Khai báo fixtures dùng chung cho toàn bộ test suite
- Cấu hình hooks, plugins tùy chỉnh
- Thiết lập môi trường test (vd: database giả, temp dir, ...)
"""

import pytest

# ---------------------------------------------------------------------------
# Ví dụ fixture đơn giản – thêm fixture của bạn ở đây
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_data() -> dict[str, int]:
    """Trả về dữ liệu mẫu dùng chung trong nhiều test."""
    return {"a": 1, "b": 2, "c": 3}
