import ssl
import socket
import subprocess
import shlex
import http.server
import socketserver

hostname = 'localhost'
port = 443


# configure and run the server
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.path = 'cert_exp.txt'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


def get_expiration_date(notAfter):
    cmd = "date -d \"{}\" '+%s'".format(notAfter)
    cmd_run = shlex.split(cmd)

    p = subprocess.Popen(cmd_run, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    rc = p.returncode
    if rc != 0:
        print(stderr)
        exit(1)

    result = stdout.decode("utf-8")
    return result


def get_cert_info():
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()

    notAfter = certificate["notAfter"]

    date = get_expiration_date(notAfter=notAfter)
    return date


def main():

    date_exp = get_cert_info()

    ser_exporter = "# HELP certificate_expiration_date Date and time of ssl sertificate expiration\n# TYPE certificate_expiration_date counter\ncertificate_expiration_date {}".format(date_exp)

    with open('cert_exp.txt', 'w') as outfile:
        outfile.write(ser_exporter)

    handler_object = MyHttpRequestHandler
    port = 9101
    httpd = socketserver.TCPServer(("", port), handler_object)
    httpd.serve_forever()


if __name__ == '__main__':
    main()

