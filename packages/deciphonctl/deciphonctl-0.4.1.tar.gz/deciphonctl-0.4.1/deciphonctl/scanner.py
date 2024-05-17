from multiprocessing import JoinableQueue, Process
from pathlib import Path
from subprocess import DEVNULL

from deciphon.h3daemon import H3Daemon
from deciphon_core.scan import Params, Scan
from deciphon_core.schema import DBFile, HMMFile, NewSnapFile
from deciphon_core.sequence import Sequence
from loguru import logger
from pydantic import FilePath

from deciphonctl.consumer import Consumer
from deciphonctl.download import download
from deciphonctl.files import (
    atomic_file_creation,
    remove_temporary_files,
    unique_temporary_file,
)
from deciphonctl.models import ScanRequest
from deciphonctl.progress import Progress
from deciphonctl.progress_informer import ProgressInformer
from deciphonctl.sched import Sched
from deciphonctl.settings import Settings
from deciphonctl.worker import worker_loop


class Scanner(Consumer):
    def __init__(
        self, sched: Sched, qin: JoinableQueue, qout: JoinableQueue, num_threads: int
    ):
        super().__init__(qin)
        self._num_threads = num_threads
        self._sched = sched
        remove_temporary_files()
        self._qout = qout

    def callback(self, message: str):
        x = ScanRequest.model_validate_json(message)

        hmmfile = Path(x.hmm.name)
        dbfile = Path(x.db.name)

        if not hmmfile.exists():
            with atomic_file_creation(hmmfile) as t:
                download(self._sched.presigned.download_hmm_url(hmmfile.name), t)

        if not dbfile.exists():
            with atomic_file_creation(dbfile) as t:
                download(self._sched.presigned.download_db_url(dbfile.name), t)

        with unique_temporary_file(".dcs") as t:
            snap = NewSnapFile(path=t)

            db = DBFile(path=FilePath(dbfile))

            logger.info("starting h3daemon")
            with H3Daemon(HMMFile(path=FilePath(hmmfile)), stdout=DEVNULL) as daemon:
                params = Params(
                    num_threads=self._num_threads,
                    multi_hits=x.multi_hits,
                    hmmer3_compat=x.hmmer3_compat,
                )
                logger.info(f"scan parameters: {params}")
                scan = Scan(params, db)
                with scan:
                    bar = Progress("scan", scan, self._sched, x.job_id)
                    bar.start()
                    scan.dial(daemon.port)
                    for seq in x.seqs:
                        scan.add(Sequence(seq.id, seq.name, seq.data))
                    scan.run(snap)
                    bar.stop()
                    logger.info(
                        "Scan has finished successfully and "
                        f"results stored in '{snap.path}'."
                    )
            self._sched.snap_post(x.id, snap.path)


def scanner_entry(settings: Settings, sched: Sched, num_workers: int, num_threads: int):
    qin = JoinableQueue()
    qout = JoinableQueue()
    informer = ProgressInformer(sched, qout)
    pressers = [Scanner(sched, qin, qout, num_threads) for _ in range(num_workers)]
    consumers = [Process(target=x.run, daemon=True) for x in pressers]
    consumers += [Process(target=informer.run, daemon=True)]
    worker_loop(settings, f"/{settings.mqtt_topic}/scan", qin, consumers)
