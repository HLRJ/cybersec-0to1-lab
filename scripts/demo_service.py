from __future__ import annotations

import argparse
import ipaddress
import json
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


ALLOWED_BIND_NETWORKS = (
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("192.168.77.0/24"),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_bind_host(host: str) -> str:
    address = ipaddress.ip_address(host)
    if not any(address in network for network in ALLOWED_BIND_NETWORKS):
        raise ValueError(f"bind host outside lab scope: {host}")
    return host

def build_event(
    *,
    client_ip: str,
    method: str,
    path: str,
    status: int,
    request_id: str,
    user_agent: str,
) -> dict[str, Any]:
    return {
        "timestamp": utc_now(),
        "request_id": request_id,
        "client_ip": client_ip,
        "method": method,
        "path": path,
        "status": status,
        "user_agent": user_agent,
    }


def write_event(event: dict[str, Any], log_path: Path | None) -> None:
    line = json.dumps(event, ensure_ascii=False, sort_keys=True)
    print(line, flush=True)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

class DemoHandler(BaseHTTPRequestHandler):
    server_version = "CyberLabDemo/1.0"

    def do_GET(self) -> None:
        request_id = str(uuid.uuid4())
        if self.path == "/health":
            status = 200
            payload = {"ok": True, "request_id": request_id}
        else:
            status = 404
            payload = {"ok": False, "request_id": request_id, "error": "not found"}

        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        self.wfile.write(body)

        event = build_event(
            client_ip=self.client_address[0],
            method="GET",
            path=self.path,
            status=status,
            request_id=request_id,
            user_agent=self.headers.get("User-Agent", ""),
        )
        write_event(event, getattr(self.server, "log_path", None))

    def log_message(self, format: str, *args: object) -> None:
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Minimal S00-L05 telemetry demo service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-file", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        host = validate_bind_host(args.host)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    server = ThreadingHTTPServer((host, args.port), DemoHandler)
    server.log_path = args.log_file
    print(
        json.dumps(
            {"event": "service_start", "timestamp": utc_now(), "host": host, "port": args.port},
            sort_keys=True,
        ),
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())