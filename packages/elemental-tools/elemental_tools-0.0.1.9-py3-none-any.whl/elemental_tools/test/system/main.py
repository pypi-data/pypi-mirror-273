from elemental_tools.constants import ref_length
from elemental_tools.system import current_timestamp, generate_reference, run_cmd, Cache


def test_current_timestamp():
    assert isinstance(current_timestamp(), str)


def test_generate_reference():

    generated_ref = generate_reference()
    longer_ref = "123456789901234567899012345678990123456789901234567899012345678990"

    try:
        shorted_ref = generate_reference(longer_ref)
        assert False
    except ValueError:
        assert True

    assert len(generated_ref) == ref_length


def test_run_cmd():
    assert run_cmd("echo 'test'")


def test_cache():
    cachefile = Cache()
    assert cachefile.get("test") is None
    cachefile.test = "test"
    cachefile.save()
    assert cachefile.get("test")
    cachefile.destroy()

