from time import perf_counter
import json

DDL = sql = """
    CREATE TABLE IF NOT EXISTS user_match (
        id                          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        doximity_id                 INT UNSIGNED NOT NULL,
        vendor_id                   INT UNSIGNED NOT NULL,
        run_date                    DATE NOT NULL,
        doximity_last_active_date   DATE NOT NULL,
        vendor_last_active_date     DATE NOT NULL,
        is_doximity_active          BOOLEAN NOT NULL,
        is_vendor_active            BOOLEAN NOT NULL,
        emitted_at                  TIMESTAMP NOT NULL,
        loaded_at                   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        INDEX(run_date)
    )
    """

DDL_OUTPUT = f"SQL DDL: {DDL}"

class Timer:
    '''
    Simple class to keep track of how much time something takes.
    dunder string method is used for the formatting needed at the
    end of the run. 
    '''
    def __init__(self) -> None:
        self._start_time = None
        self._stop_time = None

    def __str__(self) -> str:
        return f"Elapsed Time:  {self.seconds_formatter(self.elapsed())}"

    def start(self) -> None:
        self._start_time = perf_counter()

    def stop(self) -> None:
        self._stop_time = perf_counter()

    def elapsed(self) -> float:
        return self._stop_time - self._start_time

    def seconds_formatter(self, seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int((seconds % 3600) % 60)

        hours = '' if hrs == 0 else f"{hrs} hour{'' if hrs == 1 else 's'}"
        minutes = '' if mins == 0 else f"{'' if hrs == 0 else ', '}{mins} minute{'' if mins == 1 else 's'}"
        
        if secs == 0 and mins == 0 and hrs == 0:
            second = f"{secs} seconds"
        else:
            second = '' if secs == 0 else f"{'' if mins == 0 and hrs == 0 else ', '}{secs} second{'' if secs == 1 else 's'}"
        return f"{hours}{minutes}{second}".lstrip().rstrip()

class Increment:
    '''
    Simple class to keep track of counts. Dunder string
    method is used for the formatting needed at the
    end of the run.
    '''
    def __init__(self, incrementor=0) -> None:
        self.value = incrementor

    def __str__(self):
        return f"Total Matches: {self.value}"

    @property
    def incrementor(self) -> int:
        return self._value

    @incrementor.setter
    def incrementor(self, value) -> None:
        self._value = value

    def add(self) -> None:
        self.value += 1

class Sample:
    '''
    Simple class to keep track of sample records. Dunder string
    method is used for the formatting needed at the
    end of the run.
    '''
    def __init__(self, sample_limit: int = 10) -> None:
        self._samples = list()
        self._sample_limit = sample_limit

    def __str__(self) -> list:
        return f"Sample Output: {json.dumps(self._samples, indent=4, default=str)}"

    @property
    def sample_limit(self) -> int:
        return self._sample_limit

    @sample_limit.setter
    def sample_limit(self, value: int) -> None:
        self._sample_limit = value

    def add(self, sample: dict) -> None:
        if len(self._samples) < self.sample_limit:
            self._samples.append(sample)

    def get_samples(self) -> list:
        return self._samples