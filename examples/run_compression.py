from datetime import date, timedelta
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.lesson_images import CourseImageRequest, InfraiClient, prepare_course_image


def main() -> None:
    client = InfraiClient(os.environ.get("INFRAI_API_KEY"))
    item = CourseImageRequest("algebra-101", "lesson-cover.jpg", b"demo-image", date.today() + timedelta(days=1))
    result = prepare_course_image(client, item)
    print(result)


if __name__ == "__main__":
    main()
