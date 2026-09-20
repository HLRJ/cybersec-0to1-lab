from pathlib import Path


def test_s00_lab_paths_follow_restructured_order() -> None:
    assert Path("labs/s00/l01-cyber-range/README.md").is_file()
    assert Path("labs/s00/l02-scope/README.md").is_file()
    assert not Path("labs/s00/l01-scope").exists()


def test_restructured_checkpoints_are_explicit() -> None:
    l01 = Path("labs/s00/l01-cyber-range/README.md").read_text(encoding="utf-8")
    l02 = Path("labs/s00/l02-scope/README.md").read_text(encoding="utf-8")
    l03 = Path("labs/s00/l03-recovery/README.md").read_text(encoding="utf-8")
    assert "s00-l01-complete-v2" in l01
    assert "s00-l02-complete-v2" in l02
    assert "s00-l03-complete-v2" in l03


def test_s00_l03_recovery_assets_are_documented() -> None:
    readme = Path("labs/s00/l03-recovery/README.md").read_text(encoding="utf-8")
    assert Path("docs/RESET_GUIDE.md").is_file()
    assert Path("progress/s00/l03-reset-record.md").is_file()
    for image in (
        "01-snapshot-tree-before-l03.webp",
        "02-pre-mutation-checkpoint.webp",
    ):
        assert Path("labs/s00/l03-recovery/images", image).is_file()
        assert f"images/{image}" in readme


def test_curriculum_lists_s00_labs_in_order() -> None:
    text = Path("CURRICULUM.md").read_text(encoding="utf-8")
    headings = ["## S00-L01", "## S00-L02", "## S00-L03", "## S00-L04", "## S00-L05"]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)
