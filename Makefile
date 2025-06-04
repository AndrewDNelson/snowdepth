IMAGE=snowdepth-ingest

build:
	docker build -t $(IMAGE) .

run:
	docker run --rm --env-file .env -v $(PWD)/data:/app/data -v $(PWD)/logs:/app/logs $(IMAGE)

run-date:
	docker run --rm --env-file .env -v $(PWD)/data:/app/data -v $(PWD)/logs:/app/logs $(IMAGE) --date $(DATE)

clean:
	docker image prune -f
