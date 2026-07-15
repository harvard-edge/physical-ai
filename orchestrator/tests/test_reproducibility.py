from mios_controller.reproducibility import reconstruct_campaign_twice


def test_two_clean_campaign_reconstructions_match(tmp_path):
    report = reconstruct_campaign_twice(tmp_path)
    assert report.reconstructions == 2
    assert report.identical
    assert len(report.evidence_digest) == 64
