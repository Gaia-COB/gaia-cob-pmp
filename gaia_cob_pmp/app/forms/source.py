from iommi import Form

from app.models import Source, SourceGaiaInfo


class SourceForm(Form):
    """
    Handles the common setup for source-based forms.
    """

    class Meta:
        auto__model = Source
        fields = dict(
            ra__group="Coordinates",
            dec__group="Coordinates",
        )


class SourceGaiaInfoForm(Form):
    """
    Handles the common setup for source Gaia info-based forms.
    """

    class Meta:
        auto__model = SourceGaiaInfo
        fields = dict(
            parallax__group="Parallax",
            parallax_error__group="Parallax",
            pmra__group="PMRA",
            pmra_error__group="PMRA",
            pmdec__group="PMDEC",
            pmdec_error__group="PMDEC",
            radial_velocity__group="Radial Velocity",
            radial_velocity_error__group="Radial Velocity",
            astrometric_excess_noise__group="Astrometric Excess Noise",
            astrometric_excess_noise_sig__group="Astrometric Excess Noise",
        )
