                                         Dockerfile

consignes et instructions 

- une image de base officielle Python (la version allégée est un plus appréciable),
- l'application servie par gunicorn(elle est déjà installée requirements.txt) — pas le serveur de développement Flask,
- le processus s'exécutant en tant qu'utilisateur non root,
- a .dockerignore) Ainsi, votre image ne contient pas votre environnement virtuel ni votre historique Git.
- le conteneur doit écouter sur le port 8000 et répondre /health

plan

- Choisir une image de base légère
- Définir le répertoire de travail
- Copier uniquement
- Installer les dépendances
- Copier le code de l'application
- Créer un utilisateur non-root et basculer vers cet utilisateur
- Documenter le port d'écoute
- Mettre en place un HEALTHCHECK sur /health
- Définir la commande de démarrage  


Résultat

walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test$ docker build -t task-api .
[+] Building 1.5s (11/11) FINISHED                                                                                  docker:default
 => [internal] load build definition from Dockerfile                                                                          0.1s
 => => transferring dockerfile: 455B                                                                                          0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                           0.9s
 => [internal] load .dockerignore                                                                                             0.1s
 => => transferring context: 110B                                                                                             0.1s
 => [1/6] FROM docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea     0.0s
 => => resolve docker.io/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea     0.0s
 => [internal] load build context                                                                                             0.1s
 => => transferring context: 1.26kB                                                                                           0.1s
 => CACHED [2/6] WORKDIR /app                                                                                                 0.0s
 => CACHED [3/6] COPY app/requirements.txt .                                                                                  0.0s
 => CACHED [4/6] RUN pip install --no-cache-dir -r requirements.txt                                                           0.0s
 => CACHED [5/6] COPY app/app.py .                                                                                            0.0s
 => CACHED [6/6] RUN useradd --create-home appuser                                                                            0.0s
 => exporting to image                                                                                                        0.1s
 => => exporting layers                                                                                                       0.0s
 => => exporting manifest sha256:d65ffee98658aea0d37a99acccf0336730937afd1a559dbf77141f4f19a39644                             0.0s
 => => exporting config sha256:cf01bfc40f1dceac97ca23d40a3d486f2f209cc70a22572d81b5a3c2fc2c0e45                               0.0s
 => => exporting attestation manifest sha256:ea13ef95edd28c9203d837c2093f6b245c7499a184d5144a39903afcca449909                 0.0s
 => => exporting manifest list sha256:5db6b6ebb44bc2639d4b6456caed4aaa6bf9a289c67ef37594143ea064e2cb17                        0.0s
 => => naming to docker.io/library/task-api:latest                                                                            0.0s
 => => unpacking to docker.io/library/task-api:latest                                                                         0.0s


walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test$ docker run -p 8000:8000 task-api
[2026-09-03 20:30:48 +0000] [1] [INFO] Starting gunicorn 22.0.0
[2026-09-03 20:30:48 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2026-09-03 20:30:48 +0000] [1] [INFO] Using worker: sync
[2026-09-03 20:30:48 +0000] [7] [INFO] Booting worker with pid: 7


walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test$ curl http://localhost:8000/health
{"status":"ok"}

Problèmes rencontrées 

- confusion entre useradd adduser 
- Erreurs de syntaxe sur HEALTHCHECK
- difficulté a trouver la commande python qui permet de lancer de lancer les requetes http  
 


                                                Pipelines

    Consignes et instructions

- Doit se déclencher sur chaque Pull Request et sur chaque push vers main
- Lint + tests
- Build de l'image Docker
- "Extra credit" (bonus, non obligatoire) : ajouter un scan de vulnérabilités
- Push de l'image vers un registre uniquement sur main 

    Plan 

- Mise en place de deux déclencheurs Pull request et Push

  Partie 1 :
- Analyse et test de l'application : 
  - Récupération du code avec checkout
  - Mise en place des environnements  
  - Analyse du style du code avec flake8
  - Exécution des tests avec pytest

  Partie 2 : 

- Construction et analyse de l'image et push dans le registre
  - Récupération du code
  - Construction de l'image docker
  - Scan trivy de l'image 
  - Condition : uniquement si push sur main  
  - Connexion au registre 
  - Tag de l'image  
  - Push dans le registre 

- Problèmes rencontés 
  - Au moment du merge, le pipeline a échoué à l'étape docker push avec le message denied: installation not allowed to Create organization package. En analysant l'erreur, j'ai compris que le token GITHUB_TOKEN n'avait pas la permission de créer un nouveau package lors du premier push. J'ai corrigé en ajoutant un bloc permissions: packages: write au niveau du job build_push
  - Confusion sur l'ordre des mots dans github.ref (écrit ref.github par erreur), et la syntaxe exacte refs/heads/main
  - impssibilité d'installer les dependances python dans la phase de test rajout de l'environnement python.  

                Terraform 

  consignes et instrusion

  -  Écrire du code Terraform
  -  Jamais de terraform apply

  Plan 

 -  Choix du provider et du cloud
 -  Construction de l'infrastructure réseau et compute, en respectant l'ordre de dépendance entre les ressources
 -  Variabilisation des paramètres pertinents
 -  Exposition des informations utiles en sortie
 -  Vérification de la validité du code, sans déploiement réel

  Resultat

  terraform init 
  walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test/terraform$ terraform init
Initializing the backend...

Initializing provider plugins...
- Reusing previous version of hashicorp/azurerm from the dependency lock file
- Using previously-installed hashicorp/azurerm v3.117.1


Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test/terraform$ 


walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test/terraform$ terraform validate
Success! The configuration is valid.

walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test/terraform$ 


consignes et instructions

- Packager l'app avec un vrai chart Helm (templates + values, pas des manifests bruts collés dans un dossier)

Plan 

metadonnes et configuration 
Chart.yaml : identification du chart (nom, description, version du chart et de l'application)
values.yaml : centralisation des valeurs configurables — image Docker, nombre de replicas, ressources CPU/mémoire, ports, activation de l'Ingress

templates 

deployment.yaml : gestion du cycle de vie des pods (nombre de copies, image utilisée, probes de santé)
service.yaml : exposition stable des pods à l'intérieur du cluster
ingress.yaml : exposition optionnelle vers l'extérieur du cluster, désactivée par défaut

Résultat 

walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test$ helm lint helm/task-api
==> Linting helm/task-api
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed


walker@walker:/mnt/c/Users/walke/Downloads/devops-junior-test$ helm template helm/task-api
---
# Source: task-api/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: release-name-task-api
spec:
  selector:
    app: task-api
  ports:
    - port: 80
      targetPort: 8000
---
# Source: task-api/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: release-name-task-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: task-api
  template:
    metadata:
      labels:
        app: task-api
    spec:
      containers:
        - name: task-api
          image: "ghcr.io/walkerulrich/task-api-devops-test:latest"
          ports:
            - containerPort: 8000
          resources:
            limits:
              cpu: 250m
              memory: 256Mi
            requests:
              cpu: 100m
              memory: 128Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
- problèmes rencontrées 
  - Confusion entre apiVersion et appVersion — deux mots-clés très proches visuellement (apiVersion pour le format du chart, appVersion pour la version de l'application), confondus au premier essai en un seul mot appiversion
  - Confusion entre .Values et .Release — ne pas distinguer clairement que .Values vient du fichier values.yaml (écrit par toi) alors que .Release est fourni automatiquement par Helm au moment de l'installation