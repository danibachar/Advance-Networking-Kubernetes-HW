build:
	docker build -f Dockerfile -t yourdockerhubid/fullnameapp:latest .
	docker push yourdockerhubid/fullnameapp:latest

deploy: 
	kubectl apply -f kube/

delete:
	kubectl delete -f kube/