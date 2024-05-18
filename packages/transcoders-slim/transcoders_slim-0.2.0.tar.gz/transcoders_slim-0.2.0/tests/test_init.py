def test_version():
    # Check that we can import the version number
    from transcoders_slim import __version__

    assert isinstance(__version__, str)
    assert __version__ != ""
