.PHONY : backend frontend install install-dev

install:
	cd frontend && yarn
	cd backend && pip3 install .


install-dev:
	cd frontend && yarn
	cd backend && pip3 install .[dev]


serve:
	$(MAKE) -j 2 backend frontend

# run npm start inside ./api  with graphql localserver
backend:
	cd backend && fedmix-backend

# run npm start inside ./frontend
frontend:
	cd frontend && yarn serve

