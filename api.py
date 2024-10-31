import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

PORT = 8080

class Data(BaseHTTPRequestHandler):
    def do_GET(self):
        conn = sqlite3.connect('data.sqlite')
        cursor = conn.cursor()
        self.send_response(200)

        self.send_header("Content-type", "application/json")
        self.end_headers()

        query_components = parse_qs(urlparse(self.path).query)

        try:
            # Executa a query
            cursor.execute('''
                SELECT env_value, obj_value FROM sensors
                WHERE strftime('%d', timestamp) = ?
                AND strftime('%m', timestamp) = ?
                AND strftime('%Y', timestamp) = ?;
            ''', (query_components['param1'].pop(), query_components['param2'].pop(), query_components['param3'].pop()))

            # Extrai os dados como uma lista de listas
            data_list = cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            data_list = []

        # Mostra a lista de listas obtida
        print(data_list)

        # Monta a resposta no formato desejado
        response = {
            "data": data_list,
        }
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=Data):
    server_address = ('128.199.8.133', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor rodando na porta {PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
