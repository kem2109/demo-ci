"""
Tests cho module project_iaw (src/project_iaw/__init__.py).

=== CÁC THƯ VIỆN ĐƯỢC SỬ DỤNG ===

1. io.StringIO  (built-in)
   ─────────────────────────────
   StringIO là một "file object ảo" lưu dữ liệu trong bộ nhớ RAM thay vì
   ghi ra đĩa hoặc terminal. Trong test, ta dùng nó để "bắt" (capture) nội
   dung mà print() ghi ra stdout, để có thể assert nội dung đó.

2. unittest.mock.patch  (built-in, module: unittest.mock)
   ──────────────────────────────────────────────────────
   patch() là một context manager / decorator dùng để thay thế (mock) tạm
   thời một đối tượng bằng một đối tượng giả trong suốt thời gian test.
   Sau khi khối `with` kết thúc, đối tượng gốc được khôi phục tự động.
   Ở đây ta dùng: patch("sys.stdout", new_callable=StringIO)
   → Thay thế stdout thật bằng StringIO, nên mọi print() sẽ ghi vào bộ nhớ.

3. pytest  (third-party, cài qua: uv add --dev pytest)
   ──────────────────────────────────────────────────
   Framework test chính. Pytest tự động:
   - Tìm file có tên bắt đầu bằng `test_`
   - Tìm class bắt đầu bằng `Test`
   - Tìm hàm bắt đầu bằng `test_`
   - Chạy chúng và báo cáo kết quả (pass/fail)
   Câu lệnh `assert` của Python thuần được pytest "rewrite" để khi fail
   sẽ hiển thị giá trị thực tế rất rõ ràng.

4. project_iaw  (package nội bộ của dự án)
   ──────────────────────────────────────
   Import trực tiếp từ source code của dự án (src/project_iaw/__init__.py).
   Pytest biết tìm thấy package này nhờ cấu hình `pythonpath = [".", "src"]`
   trong pyproject.toml.
"""

from io import StringIO
from unittest.mock import patch

import pytest

from project_iaw import main


class TestMain:
    """
    Test suite cho hàm main().

    Dùng class để nhóm các test liên quan lại với nhau.
    Khi dùng class, pytest KHÔNG yêu cầu __init__() — chỉ cần tên class
    bắt đầu bằng `Test`.
    """

    # ------------------------------------------------------------------
    # Happy path tests (kiểm tra luồng bình thường)
    # ------------------------------------------------------------------

    def test_main_runs_without_error(self) -> None:
        """Hàm main() phải chạy thành công mà không raise exception."""
        # patch("sys.stdout") → chặn print() ghi ra terminal trong lúc test
        with patch("sys.stdout", new_callable=StringIO):
            main()  # Nếu raise bất kỳ exception nào → test FAIL tự động

    def test_main_prints_expected_message(self) -> None:
        """Hàm main() phải in đúng thông điệp ra stdout."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            # getvalue() trả về toàn bộ nội dung đã được "print" vào StringIO
            output = mock_stdout.getvalue()

        assert "Hello from project-iaw!" in output, (
            f"Thông điệp không đúng. Thực tế nhận được: {output!r}"
        )

    def test_main_returns_none(self) -> None:
        """Hàm main() phải trả về None (theo type hint -> None)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = main()

        assert result is None

    # ------------------------------------------------------------------
    # Output format tests (kiểm tra định dạng output)
    # ------------------------------------------------------------------

    def test_main_output_ends_with_newline(self) -> None:
        """print() tự động thêm newline — output phải kết thúc bằng '\\n'."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()

        assert output.endswith("\n"), (
            f"Output phải kết thúc bằng newline. Thực tế: {output!r}"
        )

    def test_main_output_is_single_line(self) -> None:
        """main() chỉ nên in đúng 1 dòng (không in thêm dòng trắng thừa)."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            # strip() loại bỏ newline cuối, sau đó đếm số dòng thực sự
            lines = mock_stdout.getvalue().strip().splitlines()

        assert len(lines) == 1, (
            f"Dự kiến 1 dòng output, thực tế có {len(lines)} dòng: {lines}"
        )

    # ------------------------------------------------------------------
    # Parametrize tests — chạy cùng 1 test với nhiều bộ dữ liệu khác nhau
    # pytest.mark.parametrize giúp tránh lặp code test
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        "keyword",
        [
            "Hello",  # Phải có từ "Hello"
            "project-iaw",  # Phải có tên project
        ],
    )
    def test_main_output_contains_keyword(self, keyword: str) -> None:
        """Output phải chứa từng keyword quan trọng."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main()
            output = mock_stdout.getvalue()

        assert keyword in output, (
            f"Keyword {keyword!r} không có trong output: {output!r}"
        )
