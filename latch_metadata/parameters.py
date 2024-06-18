
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title='Input/output options',
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'enable_filter': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='General workflow parameters',
        description='If the filtering step should be carried out.',
    ),
    'filter_trimmed': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If the pre-processed reads should be used by the filter.',
    ),
    'filter_with_kraken2': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If the output of kraken2 should be used for filtering.',
    ),
    'skip_blastn': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='If blastn should be skipped.',
    ),
    'save_intermediates': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save intermediates to the results folder.',
    ),
    'kraken2db': NextflowParameter(
        type=typing.Optional[str],
        default='https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20231009.tar.gz',
        section_title='kraken2',
        description='The database which is used in the classification step.',
    ),
    'kraken2confidence': NextflowParameter(
        type=typing.Optional[float],
        default=0.05,
        section_title=None,
        description='Confidence in the classification of a read as a certain taxon.',
    ),
    'cutoff_tax2filter': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description='If a read has less k-mers assigned to the taxon/taxa to be assessed/to be filtered the read is ignored by the pipeline.',
    ),
    'cutoff_tax2keep': NextflowParameter(
        type=typing.Optional[float],
        default=0.5,
        section_title=None,
        description='Ratio per read of assigned to tax2filter k-mers to k-mers assigned to any other taxon (except unclassified).',
    ),
    'cutoff_unclassified': NextflowParameter(
        type=typing.Optional[float],
        default=0,
        section_title=None,
        description='Ratio per read of assigned to tax2filter k-mers to unclassified k-mers.',
    ),
    'tax2filter': NextflowParameter(
        type=typing.Optional[str],
        default='Homo',
        section_title=None,
        description='The taxon or taxonomic group to be assessed or filtered by the pipeline.',
    ),
    'blast_coverage': NextflowParameter(
        type=typing.Optional[float],
        default=40,
        section_title='blastn',
        description='Coverage is the percentage of the query sequence which can be found in the alignments of the sequence match. It can be used to fine-tune the validation step.',
    ),
    'blast_evalue': NextflowParameter(
        type=typing.Optional[float],
        default=0.01,
        section_title=None,
        description='The expected(e)-value contains information on how many hits of the same score can be found in a database of the size used in the query by chance. The parameter can be used to fine-tune the validation step.',
    ),
    'blast_identity': NextflowParameter(
        type=typing.Optional[float],
        default=40,
        section_title=None,
        description='Identity is the percentage of the exact matches in the query and the sequence found in the database. The parameter can be used to fine-tune the validation step.',
    ),
    'reads_minlength': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title='fastp options',
        description='fastp option defining the minimum readlength of a read',
    ),
    'fastp_save_trimmed_fail': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='fastp option defining if the reads which failed to be trimmed should be saved',
    ),
    'fastp_qualified_quality': NextflowParameter(
        type=typing.Optional[int],
        default=0,
        section_title=None,
        description='fastp option to define the threshold of quality of an individual base',
    ),
    'fastp_cut_mean_quality': NextflowParameter(
        type=typing.Optional[int],
        default=15,
        section_title=None,
        description='fastp option to define the mean quality for trimming',
    ),
    'save_clipped_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='fastp option to define if the clipped reads should be saved',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default='GRCh38',
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'saveReference': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description=None,
    ),
    'igenomes_base': NextflowParameter(
        type=typing.Optional[LatchDir],
        default=None,
        section_title=None,
        description='Directory / URL base for iGenomes references.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

