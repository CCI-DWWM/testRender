# testRender
Essai déploiement

### Installation

```bash
 python3.13 -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt
```

### Execution locale
```bash
 fastapi dev main.py
```

## DOCKER
### Build
```bash
 docker build --tag render .
```
### Execution de l'image -> conteneur
```bash
 # -it : mode interactif
 # --rm : supprimer l'instance après execution
  docker run -it --rm -p 8000:8000 --name renderinstance render
```
