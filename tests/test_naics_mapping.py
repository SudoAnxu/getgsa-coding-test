from backend.app.core.utils import map_naics_to_sin

def test_naics_mapping():
    mapped = map_naics_to_sin(["541511", "541512", "541611"])
    assert "54151S" in mapped and "541611" in mapped
    assert mapped.count("54151S") == 1  # dedup
