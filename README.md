# DevOps Junior — Practical Test

Hi, and thanks for taking the time to do this exercise.

Here's the scenario. A developer on our team hacked together a small task-list API in
Flask. It works fine on their laptop, and now it's landing on your desk with the classic
request: "can you make this production-ready?" Nothing will actually go to production —
this is an exercise — but we'd like you to do everything you'd normally do to get it there:
put it in Git properly, containerize it, wire up CI, write the infrastructure code, and
package it for Kubernetes.

One important thing up front: **you won't create any real cloud resources, and this test
should cost you exactly zero euros.** Where infrastructure is involved, we only want the
code and your reasoning. If any step in this test seems to require your credit card,
you've misread it — stop and re-read.

Plan for roughly 4 to 6 hours of actual work. You have 5 calendar days to send it back.
If you don't finish everything, that's genuinely fine — we're much more interested in how
you work than in a complete checklist. Push your progress as you go; an honest half-done
repo tells us more than a polished one uploaded at the last minute.

## The app you're given

It lives in the `app/` folder. A tiny REST API:

| Endpoint | What it does |
|---|---|
| `GET /health` | Health check, returns `{"status": "ok"}` |
| `GET /` | Service info |
| `GET /tasks` | List tasks |
| `POST /tasks` | Create a task (`{"title": "..."}`) |
| `DELETE /tasks/<id>` | Delete a task |

Before touching anything, run it locally and make sure the tests pass:

```bash
cd app
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
python app.py       # then, in another terminal: curl http://localhost:8000/health
```

---

## What we'd like you to do

### 1. Set up the repo like you mean it

Create a new public GitHub repository under your own account and push this code to it.
Protect the `main` branch so nothing lands on it without a Pull Request.

Then, for each of the tasks below, work the way you would on a real team: a dedicated
branch (`feature/dockerize`, `feature/ci-pipeline`, that kind of thing), a PR with a few
lines explaining what you did and why, then merge.

Fair warning: we read Git history the way other people read cover letters. A handful of
small, well-named commits says a lot more about you than one giant "final version" commit
at the end.

### 2. Put it in a container

Write a `Dockerfile` for the app. A few things we care about:

- an official Python base image (slim is a nice touch),
- the app served by `gunicorn` (it's already in `requirements.txt`) — not the Flask dev
  server,
- the process running as a non-root user,
- a `.dockerignore` so your image doesn't ship your venv and Git history.

The container should listen on port 8000 and answer on `/health`. Add the build/run
instructions to your README so we can try it ourselves:

```bash
docker build -t task-api .
docker run -p 8000:8000 task-api
curl http://localhost:8000/health
```

If you want to go further: multi-stage build, trimming the image size, a `HEALTHCHECK`
instruction. All appreciated, none required.

### 3. Wire up CI

Add a GitHub Actions workflow that runs on every PR and on pushes to `main`. It should
lint the code with `flake8`, run the tests with `pytest`, and build the Docker image.
On pushes to `main` only, push the image to a registry — GitHub Container Registry
(`ghcr.io`) is free and needs no extra account, so that's our suggestion. Tag the image
with the commit SHA as well as `latest`.

Whatever you build, the pipeline should be green on `main` when you submit.

Extra credit if you add a vulnerability scan (Trivy, for instance) on the built image.

### 4. Write the Terraform — but don't apply it

Now imagine where this app would actually run. Your job: write the Terraform code for a
Kubernetes-based environment on the cloud provider of your choice — EKS, GKE, AKS,
DigitalOcean, Civo, Scaleway, whatever you'd pick if this were real.

**Do not run `terraform apply`. Not once, not "just to check".** We evaluate the code and
the thinking behind it, not a running cluster — and we really don't want you spending
money on a hiring exercise.

This is the most open-ended part of the test, on purpose. There's no target architecture
we're comparing you against. Invent the environment: pick a provider, decide what a
sensible setup looks like for a small API like this, and tell us why in your README.

What we do expect:

- the code in a `terraform/` folder, defining at least the Kubernetes cluster and the
  networking it needs (VPC/subnets or your provider's equivalent);
- variables with sensible defaults (region, cluster name, node size and count) and
  outputs for whatever a user of your code would need — not values hardcoded all over;
- `terraform fmt -check` and `terraform validate` passing (`terraform init` works without
  any credentials, so no account is needed for this);
- no state files, no `.tfvars` with secrets, no credentials in Git — ever. The
  `.gitignore` helps, but it's your responsibility;
- a section in your README: which provider, why, what the architecture looks like, and
  the commands someone *would* run to bring it up for real.

Nice extras if you have time: splitting into modules, defining a remote state backend,
running fmt/validate as a CI job.

### 5. Package it with Helm

Write a Helm chart for the app — an actual chart with templates and values, not raw
manifests copied into a chart skeleton. Put it in a `helm/` folder.

The chart should give us a Deployment with at least 2 replicas, resource requests and
limits, and liveness + readiness probes hitting `/health`; a Service; and an Ingress that
can be switched off from the values (off by default is fine). Image repository and tag,
replica count, and resources should all be configurable through `values.yaml`, with the
image defaulting to the one your CI pushes.

`helm lint` must pass, and `helm template` must render valid manifests. Paste the lint
output and a snippet of the rendered templates into your README as proof — no cluster
needed, cloud or otherwise.

If you want to show off: deploy the chart to a local cluster (kind, minikube, k3d — all
free) and include the `kubectl get pods,svc` output and a successful `curl /health`. Or
add `helm lint` to CI, wire the `APP_VERSION` env var to the image tag, add an HPA
template. Your call.

---

## What to send us

A link to your GitHub repository, containing:

- the app, your `Dockerfile` and `.dockerignore`;
- the CI workflow, green on `main`;
- the `terraform/` folder (fmt and validate clean, never applied);
- the `helm/` chart (lint clean);
- a README written by you — how to run things, the choices you made and why, and what
  you'd improve with more time;
- and the merged PRs showing how you got there.

## A few ground rules

Use whatever you want — documentation, Google, AI assistants. That's how the job works.
The only condition: **you must be able to explain every line you submit.** The follow-up
interview is a walkthrough of your repo, and we ask "why" a lot. Code you can't explain
is worse than a task you skipped.

There's no single right answer here, especially for the Terraform part. When in doubt,
make a choice, write down your reasoning, and move on — that's the skill we're hiring for.

And if you get properly stuck on something, skip it and leave a note in your README about
what blocked you and what you tried. A documented dead end earns points; silence doesn't.

Good luck — we're looking forward to reading it.
