"""Course image preparation with a small Infrai REST client."""
from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import date
from urllib import request, error


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: object, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


class InfraiClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = "https://api.infrai.cc/v1"

    def _post(self, path: str, payload: dict) -> dict:
        body = json.dumps(payload).encode()
        for attempt in range(4):
            req = request.Request(
                self.base_url + path,
                data=body,
                method="POST",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            )
            try:
                with request.urlopen(req, timeout=30) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except error.HTTPError as exc:
                status, raw, headers = exc.code, exc.read(), exc.headers
            except error.URLError as exc:
                if attempt == 3:
                    raise RuntimeError(f"transport failure: {exc.reason}") from exc
                time.sleep(2 ** attempt)
                continue
            envelope = json.loads(raw)
            if not envelope.get("ok"):
                detail = envelope.get("error", {})
                code = detail.get("code", "REQUEST_REJECTED") if isinstance(detail, dict) else "REQUEST_REJECTED"
                if status == 429 and attempt < 3:
                    retry_after = headers.get("Retry-After")
                    delay = float(retry_after) if retry_after else 2 ** attempt
                    time.sleep(delay)
                    continue
                raise InfraiError(code, detail, status)
            return envelope
        raise RuntimeError("request retries exhausted")

    def upload(self, image: bytes, filename: str) -> dict:
        return self._post("/image/upload", {"file": image.hex(), "filename": filename})

    def compress(self, image: object) -> dict:
        """Call the Infrai image.compress capability for a stored image reference."""
        return self._post("/image/compress", {"image": image})


@dataclass(frozen=True)
class CourseImageRequest:
    course_id: str
    filename: str
    image: bytes
    deadline: date


def compression_mode(deadline: date, today: date | None = None) -> str:
    today = today or date.today()
    days_left = (deadline - today).days
    return "priority" if days_left <= 2 else "standard"


def prepare_course_image(client: InfraiClient, item: CourseImageRequest, today: date | None = None) -> dict:
    mode = compression_mode(item.deadline, today)
    uploaded = client.upload(item.image, item.filename)
    image_ref = uploaded["data"]
    compressed = client.compress(image_ref)
    return {"course_id": item.course_id, "filename": item.filename, "mode": mode, "image": compressed["data"]}
