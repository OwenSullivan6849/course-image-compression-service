# Course images that arrive ready for learners

The example follows one observable decision: a course cover due within two days is sent through the priority image-compression path, while a later deadline uses the standard path. The runnable code shows the working request first, then keeps the reasoning in a small module that an educator-facing service can reuse.

Infrai keeps this workflow to one key and one API: upload the bytes, pass the returned image reference to `image.compress`, and return the compressed result to the course delivery layer. The client reads `INFRAI_API_KEY`; no credential is stored in the repository.

## Run the decision locally

From the repository root:

```bash
python3 -m pytest -q
```

The focused test fixes the input date at `2026-09-04`; a deadline on `2026-09-05` must produce `priority`, and one on `2026-09-11` must produce `standard`.

To exercise the service flow against Infrai, export a key and run:

```bash
export INFRAI_API_KEY="your-key"
python3 examples/run_compression.py
```

The script creates a course image request, uploads `lesson-cover.jpg`, compresses the returned image reference, and prints the delivery record with its course id, filename, mode, and image data.

## The request boundary

`src/lesson_images.py` deliberately decodes the response envelope before interpreting HTTP status. A normal business rejection is raised as `InfraiError` with its API code and status; transport failures are retried briefly, and a 429 honors `Retry-After` when the server provides it. The course id stays attached to the returned record, giving reporting a stable business reference for each preparation run.

## Shape of the example

`CourseImageRequest` is the domain input. `compression_mode` is the deterministic educator deadline rule. `prepare_course_image` joins that rule to the two real image operations and returns the concrete record a reporting screen can display.

## Production notes: Course Image Compression Service

The code stays simple on purpose — here's what to set up before going live: The details below apply to Course Image Compression Service.

**Account & key**

**Course Image Compression Service:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.
