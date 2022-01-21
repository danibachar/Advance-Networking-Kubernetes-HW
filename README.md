# Advance-Networking-Kubernetes-HW

A base repository for the the Kubernetes HW of the Advance Networking Course in Reichman university.

## Submission guidelines

- Fork this repository or just clone it into a local folder
- The repository have 2 folders, one for each section to follow. and subfolder for the subsections
- Your final submission **on moodle** will a zip named ex5.zip that contains the folders s1 and s2 after you fill their files as described in the instructions below - make sure that you read the submission example on the ex5 moodle assignment page. A submission that does not follow the **exact** guidelines and zip structure will not be checked!

## Basics of Kubernetes

- Please note, it is highly recommended to use a Linux machine for this assignemnt.
  If you have a Windows machine I'd recommend to install some Linux virtual machine and run on it.
  Everything should also work on Windows the main caviet will be running shell scripts.

- Throughout this assignment you will need to use `curl` command, [it should be available even on Windows 10 machine](https://stackoverflow.com/questions/9507353/how-do-i-install-and-use-curl-on-windows)

- By the end of this Section you can learn to:
  - Deploy a containerized application on a cluster.
  - Scale the deployment.
  - Update the containerized application with a new software version.
  - Debug the containerized application.

- Prerequisits
  - [Install Docker](https://docs.docker.com/get-docker/)
  - [Install Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
  - [Install Kubectl](https://kubernetes.io/docs/tasks/tools/)
  - Open an account on [Docker Hub](https://docs.docker.com/docker-id/) - you can open a personla account for free, or use an existing one if you have.
  - Clone / fork and clone this repository and make sure to run from the repo root folder!

- [Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/) - a great summary and explanation about kubectl and Kubernetes API.
  
### 1) Create a local Kubernetes cluster and learn some Docker commands

***Make sure to run the commands from the **kube** folder of inside this repo***

- Objectives:
  - Learn what a Kubernetes cluster is.
  - Learn what Docker is.
  - Start a Kubernetes cluster using an online terminal.
  - Build and push a docker application

- Guidelines:
  1) Open your computer's Terminal (windows CMD)
  2) Docker build and push
     1) Take a look at the `kube` folder, it contains a simple python `flask` application `app.py`, a `Dockerfile` a `Makefile` and two folders `simple`, and `service-discovery`
        1) Take some time to explor the application.
        2) Docker can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. Using docker build users can create an automated build that executes several command-line instructions in succession.
     2) Lets build and run your first docker application
        1) Make sure you installed the prerequisits register to Dockerhub and you have username and passowrk
        2) Run `docker login` and enter username and password
           1) If successful you should see on your terminal something like  ```Logging in with your password grants your terminal complete access to your account. For better security, log in with a limited-privilege personal access token. Learn more at https://docs.docker.com/go/access-tokens/```
        3) Cd into the `kube` directory `cd kube`
        4) Now let build your first docker container, run `docker build -f Dockerfile -t yourdockerhubid/simple:latest .`, where `yourdockerhubid` is YOUR Docker Hub.
        5) Now lets run the docker file locally `docker run --rm -it -p 3000:8080 yourdockerhubid/simple:latest`
        6) Now open any browser and navigate to `http://localhost:3000`
           1) You should see `Advance Networking app running on host localhost:3000`
           2) `-p` flag allows you to map the container port to a local port
        7) Great - now that we have built and run our first container lets push the image to the cloud so we can use it with kubernetes later!
           1) run `docker push yourdockerhubid/simple:latest`
           2) By the end it should have pushed the docker container we have built to you Docker Hub account.
              1) You can login into you docker hub account and see it there!

  3) Kind cluster
     1) Run the following command to create a new Kind cluster
        - `kind create cluster --name cluster1`
        - ![You should see a similar output on the CMD](/resources/1/kind-create-cluster.png)
     2) Validating cluster installation
        - run the command `kind get clusters`
        - You should see the `cluster1` name provided
     3) Validating `kubectl` connection and start learning Kubernetes API
        - Let’s view the cluster details. We’ll do that by running `kubectl cluster-info`
        - ![You should see a similar output on the CMD](/resources/1/kubectl-cluster-info.png)
        - We’ll be focusing on the command line for deploying and exploring our application. To view the nodes in the cluster, run the `kubectl get nodes` command
        - ![You should see a similar output on the CMD](/resources/1/kubectl-get-nodes.png)
        - This command shows all nodes that can be used to host our applications. Now we have only one node, and we can see that its status is ready (it is ready to accept applications for deployment).

- Summary:
  - We got familair with the basic building blocks of Kubernetes - the `Node` and the `Data plan`, sumarized in the following image ![Kubernetes Cluster](/resources/1/module_01_cluster.svg)
  - Kind and Docker, provides us with a local way to simulate and interact with kubernetes clusters.
  - `kubectl` is our local client for interacting with the Kubernetes API. We can watch, get, and apply changes to Kuberenetes. the basics command we run allow us to mainly interact with the underlaying API for gathering information about the cluster. In the next few steps we wll learn more about the Kubernetes API and how to create resources and deploy applications on this system.

- Submission:
  - Nothing to submit for this subseciton
  
### 2) Using kubectl to Create a Deployment

***Make sure to run the commands from the **kube** folder of inside this repo***

- Objectives:
  - Learn about application Deployments.
  - Deploy your first app on Kubernetes with kubectl.

- Guidelines:
  1) Open your computer's Terminal (windows CMD)
  2) Let’s deploy our first app on Kubernetes with the `kubectl create deployment` command. We need to provide the deployment name and app image location (include the full repository url for images hosted outside Docker hub).
  3) Run `kubectl create deployment simple --image=yourdockerhubid/simple:latest` (see that you updated you docker hub id)
      - Great! You just deployed your first application by creating a deployment. This performed a few things for you:
        - searched for a suitable node where an instance of the application could be run (we have only 1 available node)
        - scheduled the application to run on that Node
        - configured the cluster to reschedule the instance on a new Node when needed
  4) Run `kubectl get deployments`
      - We see that there is 1 deployment running a single instance of your app. The instance is running inside a Docker container on your node.
  5) You can use `--help` after the command to get additional info about possible parameters (`kubectl get nodes --help`)
  6) Note that alternativly to the `kubectl create deployment` you can interact with the Kubernetes API using YAML files!
     1) Run `kubectl delete deployment simple`
     2) Run `kubectl apply -f simple/frontend-deployment.yaml` (see that you updated you docker hub id of the image inside the yaml)
     3) Run `kubectl get deployments`
     4) Notice any difference?

- Summary:
  - We got familair with the another building block of Kubernetes - the `Deployment`, sumarized in the following image ![Kubernetes Cluster](/resources/2/module_02_first_app.svg)
  - The Deployment instructs Kubernetes how to create and update instances of your application. Once you've created a Deployment, the Kubernetes control plane schedules the application instances included in that Deployment to run on individual Nodes in the cluster. Once the application instances are created, a Kubernetes Deployment Controller continuously monitors those instances. If the Node hosting an instance goes down or is deleted, the Deployment controller replaces the instance with an instance on another Node in the cluster. This provides a self-healing mechanism to address machine failure or maintenance.

- Submission:
  - Pods that are running inside Kubernetes are running on a private, isolated network. By default they are visible from other pods and services within the same kubernetes cluster, but not outside that network. When we use kubectl, we're interacting through an API endpoint to communicate with our application.
  - The kubectl command can create a proxy that will forward communications into the cluster-wide, private network. The proxy can be terminated by pressing control-C and won't show any output while its running.
  - We will open a second terminal window to run the proxy.
    - Open additional Terminal, and run `kubectl proxy`
  - We now have a connection between our host (the online terminal) and the Kubernetes cluster. The proxy enables direct access to the API from these terminals.
  - Run the command `curl http://localhost:8001/version` and paste its output into `/s1/2/curl-version-output.txt` - commit the changes
  - The API server will automatically create an endpoint for each pod, based on the pod name, that is also accessible through the proxy. First we need to get the Pod name, and we'll store in the environment variable POD_NAME
  - Run `export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')`
  - Run `echo Name of the Pod: $POD_NAME``
  - (This command might not work on windows, in that case you can just run `kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'` and copy paste the output in the next parts)
  - Now Run `curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/` and copy the output of the command into - `/s1/2/curl-pod-details.txt` - commit the changes
  - Note! In order for the new deployment to be accessible without using the Proxy, a Service is required which will be explained in the next modules.

### 3) Viewing Pods and Nodes

***Make sure to run the commands from the **kube** folder of inside this repo***

- Objectives:
  - Learn about Kubernetes Pods.
  - Learn about Kubernetes Nodes.
  - Troubleshoot deployed applications.

- Guidelines:
  1) Let’s verify that the application we deployed in the previous scenario is running. We’ll use the kubectl get command and look for existing Pods - `kubectl get pods`
  2) Next, to view what containers are inside that Pod and what images are used to build those containers we run the describe pods command `kubectl describe pods` now we see here details about the Pod’s container: IP address, the ports used and a list of events related to the lifecycle of the Pod.
  3) Run `kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'` to get the pod's name - remember the previouse time we used this command? you can use the `$POD_NAME` env variable if you wish.
  4) Anything that the application would normally send to STDOUT becomes logs for the container within the Pod. We can retrieve these logs using the kubectl logs command - `kubectl logs $POD_NAME`
  5) Next let’s start a bash session in the Pod’s container - run `kubectl exec -ti $POD_NAME -- bash`
  6) We have now an open console on the container where we run our NodeJS application. The source code of the app is in the server.js file run - `cat app.py`
  7) You can check that the application is up by running a curl command `curl localhost:8080`
  8) To close your container connection type `exit`

- Summary:
  - Pods:
    - When you created a Deployment in Part 2, Kubernetes created a Pod to host your application instance. A Pod is a Kubernetes abstraction that represents a group of one or more application containers (such as Docker), and some shared resources for those containers. Those resources include:
      - Shared storage, as Volumes
      - Networking, as a unique cluster IP address
      - Information about how to run each container, such as the container image version or specific ports to use
      - ![Details](/resources/3/module_03_pods.svg)

    Pods are the atomic unit on the Kubernetes platform. Each Pod is tied to the Node where it is scheduled, and remains there until termination (according to restart policy) or deletion. In case of a Node failure, identical Pods are scheduled on other available Nodes in the cluster.
  - Nodes:
    - A Pod always runs on a Node. A Node is a worker machine in Kubernetes and may be either a virtual or a physical machine, depending on the cluster. Each Node is managed by the control plane. A Node can have multiple pods, and the Kubernetes control plane automatically handles scheduling the pods across the Nodes in the cluster. The control plane's automatic scheduling takes into account the available resources on each Node.
    Every Kubernetes Node runs at least:

      - Kubelet, a process responsible for communication between the Kubernetes control plane and the Node; it manages the Pods and the containers running on a machine.
      - A container runtime (like Docker) responsible for pulling the container image from a registry, unpacking the container, and running the application.
  - Troubleshoot Kubernetes - usefull commands:
    - `kubectl get` - list resources
    - `kubectl describe` - show detailed information about a resource
    - `kubectl logs` - print the logs from a container in a pod
    - `kubectl exec` - execute a command on a container in a pod

- Submission:
  - copy paste the output of the (1) command (i.e `kubectl get pods`) into `/s1/3/get-pods.txt`
  - copy paste the output of the (2) command (i.e `kubectl describe pods`) into `/s1/3/describe-pods.txt`
  - copy paste the output of the (6) command (i.e `cat app.py`) into `/s1/3/cat-app.txt`
  - Commit all the changes

### 4) Using a Service to Expose Your App

***Make sure to run the commands from the **kube** folder of inside this repo***

- Objectives:
  - Learn about a Service in Kubernetes
  - Understand how labels and LabelSelector objects relate to a Service
  - Expose an application outside a Kubernetes cluster using a Service
  
- Guidelines:
  1) Verify the application is still running run `kubectl get pods`
  2) Next, let’s list the current Services from our cluster run `kubectl get services`
  3) We have a Service called kubernetes that is created by default when kind starts its first cluster. To create a new service and expose it to external traffic we’ll use the `expose` command with `NodePort` as parameter.
     1) Run `kubectl expose deployment/simple --type="NodePort" --port 8080`
     2) Run `kubectl get services` again and
  4) Note that alternativly to the `kubectl expose` you can interact with the Kubernetes API using YAML files!
     1) Run `kubectl delete service simple`
     2) Run `kubectl apply -f simple/frontend-service.yaml`
     3) Run `kubectl get services`
     4) Notice any difference?
  5) We have now a running Service called `simple`. Here we see that the Service received a unique cluster-IP, an internal port and an external-IP (the IP of the Node).
  6) To find out what port was opened externally (by the NodePort option) we’ll run the describe service command `kubectl describe services/simple` and note the value under `NodePort` - this is the port open port on the VM that is assigned to our pod. Under `IP` we can see the node ip address
     1) If we were using a regular (or cloud) cluster with access to the Kubernetes nodes, we could have simply access the service with a `curl` command such as `curl $NODE_IP:$NODE_PORT`. Where `$NDOE_IP` = `IP` from the describe command, and `$NODE_PORT` = `NodePort` from the describe command.
     2) But we are using local kind environment which leaves us with two options (see if you can find another) - the simple one is using port forwarding - `kubectl port-forward service/simple 8080:8080`
     3) Now you can run `curl localhost:8080` or just open the browser with `localhost:8080` and observe the returned value
  7) The Deployment created automatically a label for our Pod.
     1) With describe deployment command you can see the name of the label - `kubectl describe deployment | grep Labels`
     2) Let’s use this label to query our list of Pods. We’ll use the kubectl get pods command with -l as a parameter, followed by the label values - `kubectl get pods -l app=simple`
     3) You can do the same to list the existing services - `kubectl get services -l app=simple`
     4) Get the name of the Pod `kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}'`
     5) To apply a new label we use the label command followed by the object type, object name and the new label `kubectl label pods $POD_NAME version=v1`
     6) This will apply a new label to our Pod (we pinned the application version to the Pod), and we can check it with the describe pod command `kubectl describe pods $POD_NAME`
     7) We see here that the label is attached now to our Pod. And we can query now the list of pods using the new label - `kubectl get pods -l version=v1`

- Summary:
  - Kubernetes Services
    Kubernetes Pods are mortal. Pods in fact have a lifecycle. When a worker node dies, the Pods running on the Node are also lost. Each Pod in a Kubernetes cluster has a unique IP address, even Pods on the same Node, so there needs to be a way of automatically reconciling changes among Pods so that your applications continue to function.
    A Service in Kubernetes is an abstraction which defines a logical set of Pods and a policy by which to access them. Services enable a loose coupling between dependent Pods. A Service is defined using YAML (preferred) or JSON, like all Kubernetes objects. The set of Pods targeted by a Service is usually determined by a LabelSelector see below for why you might want a Service without including selector in the spec.

    Although each Pod has a unique IP address, those IPs are not exposed outside the cluster without a Service. Services allow your applications to receive traffic. Services can be exposed in different ways by specifying a type in the ServiceSpec:

    - ClusterIP (default) - Exposes the Service on an internal IP in the cluster. This type makes the Service only reachable from within the cluster.
    - NodePort - Exposes the Service on the same port of each selected Node in the cluster using NAT. Makes a Service accessible from outside the cluster using `<NodeIP>:<NodePort>`. Superset of ClusterIP.
    - LoadBalancer - Creates an external load balancer in the current cloud (if supported) and assigns a fixed, external IP to the Service. Superset of NodePort.
    - ExternalName - Maps the Service to the contents of the externalName field (e.g. foo.bar.example.com), by returning a CNAME record with its value. No proxying of any kind is set up. This type requires v1.7 or higher of kube-dns, or CoreDNS version 0.0.8 or higher.

    Additionally, note that there are some use cases with Services that involve not defining selector in the spec. A Service created without selector will also not create the corresponding Endpoints object. This allows users to manually map a Service to specific endpoints. Another possibility why there may be no selector is you are strictly using type: ExternalName.

    - Services Labels and Selectors
    A Service routes traffic across a set of Pods. Services are the abstraction that allow pods to die and replicate in Kubernetes without impacting your application. Discovery and routing among dependent Pods (such as the frontend and backend components in an application) is handled by Kubernetes Services.
    Services match a set of Pods using labels and selectors, a grouping primitive that allows logical operation on objects in Kubernetes. Labels are key/value pairs attached to objects and can be used in any number of ways:
      - Designate objects for development, test, and production
      - Embed version tags
      - Classify an object using tags

    - ![Details](/resources/4/module_04_labels.svg)

- Submission:
  - Copy paste the output of the `curl` command from part (6.2) into `/s1/4/curl-output.txt`
  - Copy paste the output of the `describe` command from part (7.1) into `/s1/4/describe-deployment.txt`
  - Copy paste the output `kubectl get pods` command from part (7.7) into `/s1/4/pods-version-label.txt`
  - Commit all the changes

### 5)

***Make sure to run the commands from the **kube** folder of inside this repo***

- Objectives:
  - Learning how to scale deployments

- Guidelines:
  1) To list your deployments use the get deployments command `kubectl get deployments`. How many replicas does your current deployment has? We should have 1 Pod!
  2) To see the ReplicaSet created by the Deployment, run `kubectl get rs`
     1) DESIRED displays the desired number of replicas of the application, which you define when you create the Deployment. This is the desired state.
     2) CURRENT displays how many replicas are currently running.
  3) Next, let’s scale the Deployment to 4 replicas run `kubectl scale deployments/simple --replicas=4`
     1) Run `kubectl get deployments` to see the new state of your deployment
     2) Run `kubectl get pods` to see the amount of pods
  4) Let’s check that the Service is load-balancing the traffic.
     1) Use what you have learned from in part for and expose the service (it might already be expose)
     2) Run `kubectl get services` and copy its ip address lets call it `$SCV_IP` (something like `10.96.100.242`)
     3) Now, if we are using Mac or windows `kind` it is kind of hard to expose cluster nodes and services, so what we will do is just open bash to a pod like we learned before in part 3 section 5 (exec command)
     4) once you managed to open bash on some pod, run the following bash loop `for i in $(seq 1 20); do` click enter and type `curl $SCV_IP:8080` where `$SCV_IP` is the IP you copied in 4.2, click enter again, type `done` and click enter again.
     5) You shall us hiting a different Pod with every request.
  5) Run `kubectl scale deployments/simple --replicas=2` to scale thr replica count down.
  6) Run `kubectl get pods
  7) ` to see the new amount of pods

- Suammry:
  - In the previous modules we created a Deployment, and then exposed it publicly via a Service. The Deployment created only one Pod for running our application. When traffic increases, we will need to scale the application to keep up with user demand. Scaling is accomplished by changing the number of replicas in a Deployment
  - ![Before](/resources/5/module_05_scaling1.svg)
  - ![After](/resources/5/module_05_scaling2.svg)
  - Kubernetes also supports [autoscaling](https://kubernetes.io/docs/user-guide/horizontal-pod-autoscaling/) of Pods

- Submission:
  - Copy the output of the curl loop we wrote in 4.4 into `/s1/5/curl-load-balance-output.text`
  - Copy the output of the scale command in 6 into `/s1/5/scale-down-2-replica.text`  (try to get the pods in their different lifecycle moment (i.e 2 should be running and 2 should be terminating))

### 6) DNS Service Discovery

***Make sure to run the commands from the **kube** folder of inside this repo***

- Objectives:
  - Learn about Kubernetes Service Discovery mechanism
  
- Guidelines:
  1) We are going to build a simple microservice application using Kubernetes Service Discovery mechanism!
     1) Read [here](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) for more information about DNS Service Discovery on Kubernetes
     2) Kubernetes cluster uses `kube-dns` and in some layouts `core-dns` as a local DNS service which allows us to utilize the DNS Service Discovery
     3) In short, each service we create in the system can be accessable with the cluster with the followin FQDN
        1) `service-name.namespace.svc.cluster.local`
        2) We didn't talk about namespaces in Kuberentes, we deploy all our applications on the `default` namespace - but if you want to extend your mind about it read more [here](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
  2) Take a look at the `kube/service-discovery` yamls. We configure two applications
     1) We are using environment variables to allow dependencies between services
     2) Note that we are using the same flask application from our first few parts
  3) Go into the `Makefile` see the commands?
     1) Lets update them to make our life a bit easy
     2) wherever it written `yourdockerhubid` put your own Docker Hub ID you register with - and make sure you are logged-in (`docker login`)
  4) Run `make build-service-discovery`
     1) An optional to clean the previous (Part 1-5) is to run `make delete-simple`
  5) Run `make deploy-service-discovery`
  6) Run `kubectl get svc,pods,deployments`
     1) How does the output looks?
  7) Run `kubectl port-forward service/sd-front 8080:8080`

- Suammry:
  - We have learned how different microservices can communicate with each other in a Kubernetes Cluster
  - We learn how Kuberenetes utilize DNS Service Discovery to allow communication within the Cluster
  
- Submission:
  - Nothing to submit for this subseciton, you can leave the relevant folder empty

- Diclaimer - the meterials here are taken from the basic [Kubernetes toturial](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

### Final assignment

Ok good, by now you should have known how to deploy a basic microservice on Kubernetes, how to scale, expose, debug and update your microservice.
In the final assignment you would build and deploy a toy example application that requires several microservice to communicate with each other. We shall call it `full-name-app`

Use your knowledge and example YAMLs provided to build 2 layer microservice application
You shall have some `frontend` serivce that you will expose to the outside world.
This application will depened on two others - `first-name-db` and `last-name-db`
The `first-name-db` will return your first name (as string)
The `last-name-db` will return your last name (as string)
Your task is to send a GET request to the `frontend` application from the outside world, then the front end will send one GET to the `first-name-db` and one GET to the `last-name-db`, combine the result together and return string of type:
```Hey my name is {first name} {last name}```

** Bounus of 10 points to whomever decide to deploy on some cloud platform and send a working link to the application so we can access it remotely, you can get free 200$ on Google Cloud and Azure!

- For this part take a look at the folder named `s2`, and lets go over it briefly so you will know what you submit:
  - `app.py` - The application code we are going to run using Docker and Kuberenetes
  - `Dockerfile` - Docker file describing the container the applicaiton is going to run in
  - `test.sh` script - will be used by the testers to make sure the application is running as expected.
  - `Makefile` - A basic build script, please take the time to explorer the file and understand how it works, because eventually our tests going to run it - using the `test.sh` script.
  - `requirements.txt` - A requirements file is a list of all of a project’s dependencies, [read](https://realpython.com/lessons/using-requirement-files/) more about python dependencies
  - `kube` directory
    - `first-name-db`
    - `last-name-db`
    - `frontend` - The externally expose service, simple service that uses environment variable to fetch data from its dependencies (i.e first/last name dbs)
- Eventuall what you will need to to is update the yaml files of the different microservice to comply with the task requirements, run `./test.sh` and make sure the application works as expected! i.e returns ```Hey my name is {first name} {last name}``` with the appropriate first and last names.

- Submission:
  - The s2 complete folder with your filled up yaml files.
