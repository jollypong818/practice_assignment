"""개인 로컬 전송 장부. 동시 실행 방지·먼저 예약하여 예외 후에도 한도를 보존합니다.
분산 요금 차단 장치가 아니며 같은 PC의 순차 수업 프로그램용입니다.
"""
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone
import os
import json
import tempfile


class BudgetStopped(Exception):
    pass


class SendLedger:
    def __init__(self, path, limit):
        self.path = Path(path)
        self.limit = limit

    @contextmanager
    def locked(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock = self.path.with_suffix(".lock")
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise BudgetStopped("다른 실행 중이거나 잠금이 남았습니다. 동시 실행을 멈추고 강사에게 확인하세요") from None
        try:
            os.close(descriptor)
            yield
        finally:
            lock.unlink(missing_ok=True)

    def reserve(self, run_id, send_attempt):
        with self.locked():
            if self.path.exists():
                try:
                    data = json.loads(self.path.read_text(encoding="utf-8"))
                    if type(data["used"]) is not int or data["used"] < 0 or not isinstance(data["events"], list):
                        raise ValueError()
                except (OSError, ValueError, KeyError, TypeError):
                    raise BudgetStopped("장부가 손상되었습니다. 0으로 초기화하지 않고 중단합니다") from None
            else:
                data = {"used": 0, "events": []}
            if data["used"] >= self.limit:
                raise BudgetStopped("개인 실제 전송 예산에 도달했습니다. 강사 확인 전 반복하지 마세요")
            data["used"] += 1
            data["events"].append({"run_id": run_id, "send_attempt": send_attempt,
                                   "reserved_at": datetime.now(timezone.utc).isoformat()})
            handle, temp = tempfile.mkstemp(prefix="ledger-", suffix=".tmp", dir=self.path.parent)
            try:
                with os.fdopen(handle, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                    file.flush()
                    os.fsync(file.fileno())
                os.replace(temp, self.path)
            finally:
                Path(temp).unlink(missing_ok=True)
            return data["used"]
