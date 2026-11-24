#!/usr/bin/env python3
"""Cloud-free Wi-Fi (re)provisioning of a Yeelight bulb over the miIO protocol.

Usage: yeelight_wifi.py <bulb_ip> [token]
- Bulb online in the home LAN: pass its IP and saved token (see local_devices.yaml),
  it is moved to the new SSID without a reset.
- Factory-reset bulb: join its own Wi-Fi (yeelink-light-...), run against 192.168.4.1
  without a token (an unprovisioned bulb hands it out).
It also (re)enables LAN control (Yeelight protocol, TCP 55443).
Needs: pip install cryptography
"""
import getpass, hashlib, json, os, socket, struct, sys, time
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BULB_IP = sys.argv[1] if len(sys.argv) > 1 else "192.168.4.1"
TOKEN_ARG = bytes.fromhex(sys.argv[2]) if len(sys.argv) > 2 else None
PORT = 54321

def md5(b): return hashlib.md5(b).digest()

def send(sock, data):
    sock.sendto(data, (BULB_IP, PORT))
    return sock.recvfrom(4096)[0]

def hello(sock):
    return send(sock, bytes.fromhex("21310020") + b"\xff" * 28)

class Miio:
    def __init__(self, sock, token, did, stamp):
        self.sock, self.token, self.did = sock, token, did
        self.stamp0, self.t0, self.msg_id = stamp, time.time(), 1
        self.key = md5(token)
        self.iv = md5(self.key + token)

    def _crypt(self, data, enc):
        c = Cipher(algorithms.AES(self.key), modes.CBC(self.iv))
        if enc:
            p = padding.PKCS7(128).padder(); data = p.update(data) + p.finalize()
            e = c.encryptor(); return e.update(data) + e.finalize()
        d = c.decryptor(); data = d.update(data) + d.finalize()
        u = padding.PKCS7(128).unpadder(); return u.update(data) + u.finalize()

    def call(self, method, params):
        self.msg_id += 1
        body = self._crypt(json.dumps({"id": self.msg_id, "method": method, "params": params}).encode(), True)
        stamp = self.stamp0 + int(time.time() - self.t0) + 1
        head = struct.pack(">HHI", 0x2131, 32 + len(body), 0) + self.did + struct.pack(">I", stamp)
        pkt = head + md5(head + self.token + body) + body
        reply = send(self.sock, pkt)
        if len(reply) <= 32:
            return None
        return json.loads(self._crypt(reply[32:], False).rstrip(b"\x00"))

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    r = hello(sock)
    did, stamp, token = r[8:12], struct.unpack(">I", r[12:16])[0], r[16:32]
    if token in (b"\xff" * 16, b"\x00" * 16):
        if not TOKEN_ARG:
            sys.exit("The bulb is provisioned and hides its token: pass the saved token as the 2nd argument.")
        token = TOKEN_ARG
    print("Device id:", did.hex(), " token:", token.hex())
    with open(os.path.expanduser("~/yeelight_token.txt"), "w") as f:
        f.write(token.hex() + "\n")
    print("Token saved to ~/yeelight_token.txt")

    dev = Miio(sock, token, did, stamp)
    print("miIO.info ->", (dev.call("miIO.info", []) or {}).get("result", {}).get("model"))
    print("Enable LAN control ->", dev.call("set_ps", ["cfg_lan_ctrl", "1"]))

    ssid = input("Home Wi-Fi SSID (2.4 GHz): ").strip()
    passwd = getpass.getpass("Wi-Fi password (not shown): ")
    print("config_router ->", dev.call("miIO.config_router", {"ssid": ssid, "passwd": passwd, "uid": 0}))
    print("Done. The bulb now joins your Wi-Fi; reconnect this computer to your home network.")

if __name__ == "__main__":
    main()
