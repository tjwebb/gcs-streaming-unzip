import functions_framework
from google.cloud import storage
from stream_unzip import stream_unzip
from os import path

@functions_framework.http
def extract(request):
    request_json = request.get_json(silent=True)

    if request_json and 'gcs_source_uri' in request_json:
        gcs_source_uri = request_json['gcs_source_uri']
    if request_json and 'gcs_dest_path' in request_json:
        gcs_dest_path = request_json['gcs_dest_path']
    if request_json and 'filter_ignore' in request_json:
        filter_ignore_regex = request_json['filter_ignore']

    gcs_bucket_name = gcs_source_uri.split("/")[2]
    gcs_path = "/".join(gcs_source_uri.split("/")[3:])
    client = storage.Client()
    bucket = client.bucket(gcs_bucket_name)

    def get_gcs_zip_chunks():
        blob = bucket.blob(gcs_path)
        reader = storage.fileio.BlobReader(blob)
        for chunk_bytes in reader:
            yield chunk_bytes

    for file_name, file_size, unzipped_chunks in stream_unzip(get_gcs_zip_chunks()):
        file_name = file_name.decode('utf-8')
        base = path.splitext(gcs_path)[0]
        out_file = '{}/{}'.format(base, str(file_name))
        blob = bucket.blob(out_file)
        writer = storage.fileio.BlobWriter(blob)
        for chunk in unzipped_chunks:
            writer.write(chunk)

        print('wrote {}'.format(out_file))

    print('done')
    return 'done'
