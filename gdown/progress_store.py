import time
import threading

_PROGRESS = {}
_LOCK = threading.Lock()

def init_progress(task_id: str, total: int | None):
    with _LOCK:
        _PROGRESS[task_id] = {
            "start_time": time.time(),
            "total": total,
            "downloaded": 0,
            "percent": 0.0,
            "status": "running",
            "cancelled": False,
            "total_files": 0,
            "current_file": 0,
        }

def folder_update_progress(task_id: str, total: int | None):
    with _LOCK:
        task = _PROGRESS.get(task_id)
        if not task:
            return
        task["start_time"] = time.time()
        task["total"] = total
        task["downloaded"] = 0
        task["percent"] = 0.0

def update_progress(task_id: str, downloaded: int, total: int | None):
    if total is None or total <= 0:
        return
    with _LOCK:
        task = _PROGRESS.get(task_id)
        if not task:
            return
        task["downloaded"] = downloaded
        task["total"] = total
        percent = (downloaded / total) * 100
        percent = max(0, min(100, percent))
        task["percent"] = round(percent, 2)



def complete_progress(task_id: str):
    with _LOCK:
        if task_id in _PROGRESS:
            _PROGRESS[task_id]["status"] = "completed"


def fail_progress(task_id: str, error: str):
    with _LOCK:
        if task_id in _PROGRESS:
            _PROGRESS[task_id]["status"] = "failed"
            _PROGRESS[task_id]["error"] = error


def remove_progress(task_id: str):
    with _LOCK:
        _PROGRESS.pop(task_id, None)


def get_progress(task_id: str):
    with _LOCK:
        return _PROGRESS.get(task_id)


def get_all_progress():
    with _LOCK:
        return dict(_PROGRESS)


def cancel_task(task_id: str) -> bool:
    with _LOCK:
        task = _PROGRESS.get(task_id)
        if not task:
            return False
        if task.get("status") != "running":
            return False
        task["cancelled"] = True
        task["status"] = "cancelled"
        return True
    
def set_folder_file_meta(task_id: str, total_files: int):
    with _LOCK:
        task = _PROGRESS.get(task_id)
        if not task:
            return
        task["total_files"] = total_files
        task["current_file"] = 0


def update_folder_file_index(task_id: str, current_index: int):
    with _LOCK:
        task = _PROGRESS.get(task_id)
        if not task:
            return
        task["current_file"] = current_index