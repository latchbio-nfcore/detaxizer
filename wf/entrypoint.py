from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], enable_filter: typing.Optional[bool], filter_trimmed: typing.Optional[bool], filter_with_kraken2: typing.Optional[bool], skip_blastn: typing.Optional[bool], save_intermediates: typing.Optional[bool], fastp_save_trimmed_fail: typing.Optional[bool], save_clipped_reads: typing.Optional[bool], fasta: typing.Optional[LatchFile], igenomes_base: typing.Optional[LatchDir], multiqc_methods_description: typing.Optional[str], kraken2db: typing.Optional[str], kraken2confidence: typing.Optional[float], cutoff_tax2filter: typing.Optional[int], cutoff_tax2keep: typing.Optional[float], cutoff_unclassified: typing.Optional[float], tax2filter: typing.Optional[str], blast_coverage: typing.Optional[float], blast_evalue: typing.Optional[float], blast_identity: typing.Optional[float], reads_minlength: typing.Optional[int], fastp_qualified_quality: typing.Optional[int], fastp_cut_mean_quality: typing.Optional[int], genome: typing.Optional[str], saveReference: typing.Optional[bool]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('enable_filter', enable_filter),
                *get_flag('filter_trimmed', filter_trimmed),
                *get_flag('filter_with_kraken2', filter_with_kraken2),
                *get_flag('skip_blastn', skip_blastn),
                *get_flag('save_intermediates', save_intermediates),
                *get_flag('kraken2db', kraken2db),
                *get_flag('kraken2confidence', kraken2confidence),
                *get_flag('cutoff_tax2filter', cutoff_tax2filter),
                *get_flag('cutoff_tax2keep', cutoff_tax2keep),
                *get_flag('cutoff_unclassified', cutoff_unclassified),
                *get_flag('tax2filter', tax2filter),
                *get_flag('blast_coverage', blast_coverage),
                *get_flag('blast_evalue', blast_evalue),
                *get_flag('blast_identity', blast_identity),
                *get_flag('reads_minlength', reads_minlength),
                *get_flag('fastp_save_trimmed_fail', fastp_save_trimmed_fail),
                *get_flag('fastp_qualified_quality', fastp_qualified_quality),
                *get_flag('fastp_cut_mean_quality', fastp_cut_mean_quality),
                *get_flag('save_clipped_reads', save_clipped_reads),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('saveReference', saveReference),
                *get_flag('igenomes_base', igenomes_base),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_detaxizer", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_detaxizer(input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], enable_filter: typing.Optional[bool], filter_trimmed: typing.Optional[bool], filter_with_kraken2: typing.Optional[bool], skip_blastn: typing.Optional[bool], save_intermediates: typing.Optional[bool], fastp_save_trimmed_fail: typing.Optional[bool], save_clipped_reads: typing.Optional[bool], fasta: typing.Optional[LatchFile], igenomes_base: typing.Optional[LatchDir], multiqc_methods_description: typing.Optional[str], kraken2db: typing.Optional[str] = 'https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20231009.tar.gz', kraken2confidence: typing.Optional[float] = 0.05, cutoff_tax2filter: typing.Optional[int] = 2, cutoff_tax2keep: typing.Optional[float] = 0.5, cutoff_unclassified: typing.Optional[float] = 0, tax2filter: typing.Optional[str] = 'Homo', blast_coverage: typing.Optional[float] = 40, blast_evalue: typing.Optional[float] = 0.01, blast_identity: typing.Optional[float] = 40, reads_minlength: typing.Optional[int] = 0, fastp_qualified_quality: typing.Optional[int] = 0, fastp_cut_mean_quality: typing.Optional[int] = 15, genome: typing.Optional[str] = 'GRCh38', saveReference: typing.Optional[bool] = True) -> None:
    """
    nf-core/detaxizer

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, enable_filter=enable_filter, filter_trimmed=filter_trimmed, filter_with_kraken2=filter_with_kraken2, skip_blastn=skip_blastn, save_intermediates=save_intermediates, kraken2db=kraken2db, kraken2confidence=kraken2confidence, cutoff_tax2filter=cutoff_tax2filter, cutoff_tax2keep=cutoff_tax2keep, cutoff_unclassified=cutoff_unclassified, tax2filter=tax2filter, blast_coverage=blast_coverage, blast_evalue=blast_evalue, blast_identity=blast_identity, reads_minlength=reads_minlength, fastp_save_trimmed_fail=fastp_save_trimmed_fail, fastp_qualified_quality=fastp_qualified_quality, fastp_cut_mean_quality=fastp_cut_mean_quality, save_clipped_reads=save_clipped_reads, genome=genome, fasta=fasta, saveReference=saveReference, igenomes_base=igenomes_base, multiqc_methods_description=multiqc_methods_description)

