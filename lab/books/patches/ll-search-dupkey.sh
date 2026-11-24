#!/bin/sh
# LazyLibrarian "modern" UI: search results crash (Alpine "Duplicate key on x-for")
# when Google Books returns the same volume twice. Add the row index to the key.
# Idempotent; run by Komodo post-deploy of the "books" stack after every (auto)update.
F=/app/lazylibrarian/data/interfaces/modern/searchresults.html
for i in 1 2 3 4 5 6; do docker exec lazylibrarian test -f "$F" && break; sleep 5; done
docker exec lazylibrarian sh -c "grep -q '(r, idx) in items' $F || sed -i 's/x-for=\"r in items\" :key=\"r.id + .|. + r.source\"/x-for=\"(r, idx) in items\" :key=\"idx + '\''|'\'' + r.id + '\''|'\'' + r.source\"/' $F; grep -c '(r, idx) in items' $F"
