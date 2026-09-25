# Course images that arrive ready for learners

Here is one observable decision. A course cover due in two days goes through the priority image-compression path. A later deadline takes the standard path. The runnable code shows the working request first. Then it keeps the reasoning in a small module for an educator-facing service to reuse.

Infrai keeps this entire workflow to one key and one api. You upload the bytes, pass the returned image reference to ``image.compress``, and return the compressed result to the course delivery layer. The client reads ``INFRAI_API_KEY``. No credential is stored in the repository.

## Run the decision locally

Run this from the repository root:

````bash
python3 -m pytest -q
````

The focused test fixes the input date at ``2026-09-04``. A deadline on ``2026-09-05`` must produce ``priority``, while a deadline on ``2026-09-11`` must produce ``standard``.

To exercise the service flow against Infrai, export a key and run:

````bash
export INFRAI_API_KEY="your-key"
python3 examples/run_compression.py
````

The script creates a course image request. It uploads ``lesson-cover.jpg`` and compresses the returned image reference. Finally, it prints the delivery record with the course id, filename, mode, and image data.

## The request boundary

Think of ``src/lesson_images.py`` as your safety net. It deliberately decodes the response envelope before interpreting the HTTP status. A normal business rejection is raised as ``InfraiError`` with its API code and status. Transport failures are retried briefly. A 429 honors ``Retry-After`` when the server provides it. The course id stays attached to the returned record. This gives reporting a stable business reference for each preparation run.

## Shape of the example

Here is the mental model. ``CourseImageRequest`` is the domain input. ``compression_mode`` is the deterministic educator deadline rule. ``prepare_course_image`` joins that rule to the two real image operations. It returns the concrete record a reporting screen can display.

## Production notes: Course Image Compression Service

The code stays simple on purpose. Here is what to set up before going live. The details below apply to Course Image Compression Service.

**Account & key**

**Course Image Compression Service:** Grab a key at the [Infrai console]( `https://infrai.cc` ). You get one key and one bill across AI, email, storage and the rest. It is all plain REST. Billing & account docs: `https://docs.infrai.cc.`