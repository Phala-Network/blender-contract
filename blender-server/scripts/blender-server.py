#!/usr/bin/env python3

import os
import sys
import subprocess
from urllib.parse import urlparse, parse_qsl
import uuid
from http.server import SimpleHTTPRequestHandler, HTTPServer

BLENDER = '/blender/blender'


class RenderingRequestHandler(SimpleHTTPRequestHandler):
    def simple_respond(self, code, body):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_PUT(self):
        input_dir = os.path.join('/data', 'scenes')
        if not os.path.exists(input_dir):
            os.mkdir(input_dir)

        file_id = str(uuid.uuid1())
        filename = os.path.basename(self.path)
        extension = os.path.splitext(filename)[-1]
        filepath = os.path.join(input_dir, file_id + '.blend')
        if extension != '.blend':
            self.simple_respond(415,
                                'Only .blend is supported\n')
            return

        file_length = int(self.headers['Content-Length'])
        with open(filepath, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))
        print(f"File {filename} uploaded as {file_id}", flush=True)

        self.simple_respond(201, 'File ID "%s"\n' % file_id)

    def do_GET(self):
        input_dir = os.path.join('/data', 'scenes')
        output_dir = os.path.join('/data', 'images')

        url = urlparse(self.path)
        if url.path == '/render':
            query = dict(parse_qsl(url.query))
            if 'id' not in query:
                self.simple_respond(404, 'File ID required')
                return

            file_id = query['id']
            filepath = os.path.join(input_dir, file_id + '.blend')
            if not os.path.exists(filepath):
                self.simple_respond(404, 'File not found')
                return

            blender = subprocess.Popen([BLENDER, '-b', filepath,
                                        '-t', '4',
                                        '-F', 'PNG',
                                        '-o', os.path.join(output_dir,
                                                           file_id),
                                        '-f', '1'])
            blender.wait()
            print(f"Render {file_id} finished", flush=True)
            self.simple_respond(
                201, 'File "%s" rendered\n' % (file_id + '0001.png'))

        elif url.path == '/download':
            query = dict(parse_qsl(url.query))
            if 'filename' not in query:
                self.simple_respond(404, 'Filename required')
                return

            filename = query['filename']
            filepath = os.path.join(output_dir, filename)
            if not os.path.exists(filepath):
                self.simple_respond(404, 'File not found')
                return

            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open(filepath, 'rb') as input_file:
                self.wfile.write(input_file.read())

        else:
            self.simple_respond(404, 'Invalid path')


def main(argv):
    if len(argv) != 2:
        print(f'Usage: {argv[0]} <PORT>', file=sys.stderr)
        return 1

    if not os.path.exists(BLENDER):
        print('Blender not found', file=sys.stderr)
        return 1

    port = int(argv[1])
    srv = HTTPServer(('localhost', port), RenderingRequestHandler)

    print('Launch render server', flush=True)
    srv.serve_forever()

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
