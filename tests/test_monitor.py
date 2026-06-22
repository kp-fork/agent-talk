"""The inbox monitor resolves this session's user from the session->user map
and pushes new spool lines (no retalk needed)."""
import os, pathlib, select, subprocess, tempfile, time, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MON = os.path.join(ROOT, "bin", "inbox-monitor.sh")


class TestMonitor(unittest.TestCase):
    def test_resolves_user_from_map_and_pushes(self):
        home = tempfile.mkdtemp()
        sid = "s.test.1"
        udir = os.path.join(home, "proj", ".agent-talk", "users", "alice")  # local-scope abs dir
        os.makedirs(udir)
        os.makedirs(os.path.join(home, ".agent-talk", "by-session"))
        mon = subprocess.Popen(["bash", MON, sid], env=dict(os.environ, HOME=home),
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        try:
            time.sleep(1)  # monitor waits for the map
            pathlib.Path(home, ".agent-talk", "by-session", sid).write_text(udir + "\n")
            time.sleep(3)  # monitor reads map + attaches tail
            pathlib.Path(udir, "inbox.ndjson").write_text('{"text":"hi"}\n')
            line = ""
            if select.select([mon.stdout], [], [], 5)[0]:
                line = mon.stdout.readline().strip()
            self.assertEqual(line, '{"text":"hi"}')
        finally:
            mon.terminate(); mon.wait(timeout=5)

    def test_idles_without_session_id(self):
        home = tempfile.mkdtemp()
        mon = subprocess.Popen(["bash", MON, "${CLAUDE_SESSION_ID}"],
                               env=dict(os.environ, HOME=home),
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        try:
            time.sleep(1)
            self.assertFalse(select.select([mon.stdout], [], [], 1)[0],
                             "monitor should emit nothing without a session id")
            self.assertIsNone(mon.poll(), "monitor should keep idling, not exit")
        finally:
            mon.terminate(); mon.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
