from iommi import Table

from app.models import Source


class SourceTable(Table):
    """
    Class to represent a table of sources.
    """

    class Meta:
        """
        This is stuff that you could otherwise pass as arguments to the constructor
        """

        auto = dict(
            model=Source,
            include=["name", "gaiainfo__gaia_id", "other_names", "ra", "dec"],
        )
        columns = dict(
            name=dict(
                cell__url=lambda row, **_: row.get_absolute_url(),
                filter=dict(  # Enables free-text search on the column names
                    include=True,
                    freetext=True,
                ),
            ),
            gaiainfo_gaia_id=dict(
                filter=dict(
                    include=True,
                    freetext=True,
                ),
            ),
            other_names=dict(
                filter=dict(
                    include=True,
                    freetext=True,
                ),
            ),
        )
        query__advanced__include = False  # We don't want the advanced filter
        rows = Source.objects.filter(is_valid=True)
