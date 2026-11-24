#!/bin/sh
# Calibre-Web-Automated: e-mailed books keep the transliterated on-disk file name
# ("Nieznaika v ... .epub") and Send-to-Kindle shows it as the title. Name the
# attachment "<title> - <author>.<ext>" from the book's metadata.opf (Unicode).
# Idempotent; run by Komodo post-deploy of the "books" stack after every (auto)update.
for i in 1 2 3 4 5 6; do docker exec calibre-web test -f /app/calibre-web-automated/cps/tasks/mail.py && break; sleep 5; done
docker exec -i calibre-web python3 - <<'PY'
p = "/app/calibre-web-automated/cps/tasks/mail.py"
s = open(p).read()
if "_mbuz_display_name" in s:
    print("already patched"); raise SystemExit
old = "message.add_attachment(data, maintype=main_type, subtype=sub_type, filename=self.attachment)"
assert old in s, "anchor not found"
s = s.replace(old, "message.add_attachment(data, maintype=main_type, subtype=sub_type, filename=_mbuz_display_name(self.filepath, self.attachment))")
s += '''

def _mbuz_display_name(book_path, attachment):
    """Attachment name from metadata.opf (title - author.ext); falls back to the file name."""
    import re
    try:
        opf = open(os.path.join(config.get_book_path(), book_path, "metadata.opf"), encoding="utf-8").read()
        title = re.search(r"<dc:title[^>]*>([^<]+)</dc:title>", opf).group(1).strip()
        m = re.search(r"<dc:creator[^>]*>([^<]+)</dc:creator>", opf)
        name = title + (" - " + m.group(1).strip() if m else "")
        name = re.sub(r'[\\\\/:*?"<>|\\r\\n]+', " ", name).strip()[:150]
        return name + os.path.splitext(attachment)[1]
    except Exception:
        return attachment
'''
open(p, "w").write(s)
print("patched")
PY
docker restart calibre-web >/dev/null
