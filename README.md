# gcs-streaming-unzip

This is a Google Cloud Function that extracts a file in a Google Cloud Storage (GCS) bucket and writes it back to GCS. It streams and decompresses files in [40MiB chunks](https://cloud.google.com/python/docs/reference/storage/latest/google.cloud.storage.fileio.BlobReader#parameters) to minimize RAM usage.

It allows you to extract large files and avoids some limitations of other approaches:
- The [Dataflow Bulk Decompressor](https://cloud.google.com/dataflow/docs/guides/templates/provided/bulk-decompress-cloud-storage) template only works with archives that contain a single file
- The Dataflow Python SDK does not have the ability to decompress zip files
- CLI tools and most programmatic approaches require sufficient disk + RAM to extract, write, and upload the archive contents
