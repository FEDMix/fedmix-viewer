.PHONY : backend frontend install install-dev run frontend-dist

install:
	cd frontend && yarn
	cd backend && pip3 install .


install-dev:
	cd frontend && yarn
	cd backend && pip3 install -e .[dev]


serve:
	$(MAKE) -j 2 backend frontend

# run npm start inside ./api  with graphql localserver
backend:
	cd backend && fedmix-backend

# run npm start inside ./frontend
frontend:
	cd frontend && yarn serve


frontend-dist:
	cd frontend && yarn && yarn build

run: frontend-dist
	docker-compose up

