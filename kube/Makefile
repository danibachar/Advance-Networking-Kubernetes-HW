cleanup: delete-simple
	delete-service-discovery

build-simple:
	docker build -f Dockerfile -t yourdockerhubid/simple:latest .
	docker push yourdockerhubid/simple:latest

build-service-discovery:
	docker build -f Dockerfile -t yourdockerhubid/service-discovery:latest .
	docker push yourdockerhubid/service-discovery:latest

deploy-simple:
	kubectl apply -f simple/

delete-simple:
	kubectl delete -f simple/

deploy-service-discovery:
	kubectl apply -f service-discovery/

delete-service-discovery:
	kubectl delete -f service-discovery/