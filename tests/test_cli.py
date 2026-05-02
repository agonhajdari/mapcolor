from pathlib import Path

from mapcolor.__main__ import main


def test_cli_writes_output_file(tmp_path: Path):
    svg = tmp_path / "map.svg"
    output = tmp_path / "out.svg"
    svg.write_text(
        """
        <svg xmlns="http://www.w3.org/2000/svg">
          <rect id="a" x="0" y="0" width="10" height="10" />
        </svg>
        """,
        encoding="utf-8",
    )

    exit_code = main([str(svg), "--output", str(output)])

    assert exit_code == 0
    assert 'fill="#' in output.read_text(encoding="utf-8")
