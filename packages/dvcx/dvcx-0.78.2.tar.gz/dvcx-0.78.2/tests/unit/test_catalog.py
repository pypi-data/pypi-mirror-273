from textwrap import dedent


def test_compile_query_script(catalog):
    script = dedent(
        """
        from dvcx.query import C, DatasetQuery, asUDF
        DatasetQuery("s3://bkt/dir1")
        """
    ).strip()
    result = catalog.compile_query_script(script)
    expected = dedent(
        """
        from dvcx.query import C, DatasetQuery, asUDF
        import dvcx.query.dataset
        dvcx.query.dataset.query_wrapper(
        DatasetQuery('s3://bkt/dir1'))
        """
    ).strip()
    assert result == expected
