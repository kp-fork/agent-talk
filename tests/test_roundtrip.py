"""End-to-end: a scoped follower (`retalk receive --peer X --follow`) feeds the
per-user spool. Skips automatically when retalk isn't installed (e.g. CI without
the private retalk dependency); runs locally where retalk is on PATH."""
import json, os, pathlib, shutil, socket, subprocess, tempfile, time, unittest

RETALK = shutil.which("retalk")
RETALK_SERVER = shutil.which("retalk-server")
PORT = 8808
URL = f"http://127.0.0.1:{PORT}"


def _wait(port, timeout=15):
    end = time.time() + timeout
    while time.time() < end:
        try:
            socket.create_connection(("127.0.0.1", port), 1).close(); return
        except OSError:
            time.sleep(0.1)
    raise TimeoutError("relay did not start")


@unittest.skipUnless(RETALK and RETALK_SERVER, "retalk/retalk-server not on PATH")
class TestRoundTrip(unittest.TestCase):
    def _rk(self, *a):
        r = subprocess.run([RETALK, *a], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, f"retalk {a}: {r.stderr}")
        return r.stdout

    def test_scoped_follower_feeds_spool(self):
        tmp = tempfile.mkdtemp()
        A = os.path.join(tmp, "a"); B = os.path.join(tmp, "b")
        spool = os.path.join(tmp, "inbox.ndjson")
        srv = subprocess.Popen(
            [RETALK_SERVER], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            env=dict(os.environ, RETALK_SERVER_HOST="127.0.0.1",
                     RETALK_SERVER_PORT=str(PORT), RETALK_SERVER_AUDIENCE=URL,
                     RETALK_SERVER_DB=os.path.join(tmp, "relay.db")))
        follower = None
        try:
            _wait(PORT)
            self._rk("init", "--dir", A, "--relay", URL, "--no-passphrase", "--display-name", "alice")
            self._rk("init", "--dir", B, "--relay", URL, "--no-passphrase", "--display-name", "bob")
            aid = json.loads(self._rk("id", "--dir", A, "--json"))["fingerprint"]
            bid = json.loads(self._rk("id", "--dir", B, "--json"))["fingerprint"]
            self._rk("sync", "--dir", A)  # publish alice's keys (no --all needed)
            sf = open(spool, "wb")
            follower = subprocess.Popen(
                [RETALK, "receive", "--peer", bid, "--follow", "--dir", A],
                stdout=sf, stderr=subprocess.DEVNULL)
            time.sleep(2)
            self._rk("send", "--peer", aid, "scoped ping", "--dir", B)  # bob -> alice
            got = None
            for _ in range(8):
                time.sleep(1)
                lines = [l for l in pathlib.Path(spool).read_text().splitlines() if l.strip()]
                if lines:
                    got = json.loads(lines[-1]); break
            self.assertIsNotNone(got, "follower wrote nothing to the spool")
            self.assertEqual(got["text"], "scoped ping")
            self.assertEqual(got["from"], bid)
        finally:
            if follower:
                follower.terminate(); follower.wait(timeout=5)
                sf.close()
            srv.terminate(); srv.wait(timeout=10)


if __name__ == "__main__":
    unittest.main()
