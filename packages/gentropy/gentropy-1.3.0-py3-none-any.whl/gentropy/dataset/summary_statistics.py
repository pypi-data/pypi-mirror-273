"""Summary satistics dataset."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pyspark.sql.functions as f

from gentropy.common.schemas import parse_spark_schema
from gentropy.common.utils import parse_region, split_pvalue
from gentropy.dataset.dataset import Dataset

if TYPE_CHECKING:
    from pyspark.sql.types import StructType

    from gentropy.dataset.study_locus import StudyLocus


@dataclass
class SummaryStatistics(Dataset):
    """Summary Statistics dataset.

    A summary statistics dataset contains all single point statistics resulting from a GWAS.
    """

    @classmethod
    def get_schema(cls: type[SummaryStatistics]) -> StructType:
        """Provides the schema for the SummaryStatistics dataset.

        Returns:
            StructType: Schema for the SummaryStatistics dataset
        """
        return parse_spark_schema("summary_statistics.json")

    def pvalue_filter(self: SummaryStatistics, pvalue: float) -> SummaryStatistics:
        """Filter summary statistics based on the provided p-value threshold.

        Args:
            pvalue (float): upper limit of the p-value to be filtered upon.

        Returns:
            SummaryStatistics: summary statistics object containing single point associations with p-values at least as significant as the provided threshold.
        """
        # Converting p-value to mantissa and exponent:
        (mantissa, exponent) = split_pvalue(pvalue)

        # Applying filter:
        df = self._df.filter(
            (f.col("pValueExponent") < exponent)
            | (
                (f.col("pValueExponent") == exponent)
                & (f.col("pValueMantissa") <= mantissa)
            )
        )
        return SummaryStatistics(_df=df, _schema=self._schema)

    def window_based_clumping(
        self: SummaryStatistics,
        distance: int = 500_000,
        gwas_significance: float = 5e-8,
    ) -> StudyLocus:
        """Generate study-locus from summary statistics using window-based clumping.

        For more info, see [`WindowBasedClumping`][gentropy.method.window_based_clumping.WindowBasedClumping]

        Args:
            distance (int): Distance in base pairs to be used for clumping. Defaults to 500_000.
            gwas_significance (float, optional): GWAS significance threshold. Defaults to 5e-8.

        Returns:
            StudyLocus: Clumped study-locus optionally containing variants based on window.
        """
        from gentropy.method.window_based_clumping import WindowBasedClumping

        return WindowBasedClumping.clump(
            self,
            distance=distance,
            gwas_significance=gwas_significance,
        )

    def exclude_region(self: SummaryStatistics, region: str) -> SummaryStatistics:
        """Exclude a region from the summary stats dataset.

        Args:
            region (str): region given in "chr##:#####-####" format

        Returns:
            SummaryStatistics: filtered summary statistics.
        """
        (chromosome, start_position, end_position) = parse_region(region)

        return SummaryStatistics(
            _df=(
                self.df.filter(
                    ~(
                        (f.col("chromosome") == chromosome)
                        & (
                            (f.col("position") >= start_position)
                            & (f.col("position") <= end_position)
                        )
                    )
                )
            ),
            _schema=SummaryStatistics.get_schema(),
        )

    def sanity_filter(self: SummaryStatistics) -> SummaryStatistics:
        """The function filters the summary statistics by sanity filters.

        The function filters the summary statistics by the following filters:
            - The p-value should not be eqaul 1.
            - The beta and se should not be equal 0.
            - The p-value, beta and se should not be NaN.

        Returns:
            SummaryStatistics: The filtered summary statistics.
        """
        gwas_df = self._df
        gwas_df = gwas_df.dropna(
            subset=["beta", "standardError", "pValueMantissa", "pValueExponent"]
        )

        gwas_df = gwas_df.filter((f.col("beta") != 0) & (f.col("standardError") != 0))
        gwas_df = gwas_df.filter(
            f.col("pValueMantissa") * 10 ** f.col("pValueExponent") != 1
        )

        return SummaryStatistics(
            _df=gwas_df,
            _schema=SummaryStatistics.get_schema(),
        )
