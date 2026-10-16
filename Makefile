.PHONY: csr profile qr dev up down
csr:     ; ORG_NAME=$${ORG_NAME:-MDM} bash scripts/make-csr.sh
profile: ; python3 scripts/build-profile.py
qr:      ; python3 scripts/enroll-qr.py "$$ENROLL_URL" site/assets/enroll-qr.png
dev:     ; cd server && docker compose up --build
up:      ; cd server && docker compose up -d --build
down:    ; cd server && docker compose down
