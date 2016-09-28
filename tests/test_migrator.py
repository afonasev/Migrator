from migrator.application import migrator_factory


def test_for_coverage():
    assert migrator_factory('migrations')
