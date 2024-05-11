from pathlib import Path

HERE = Path(__file__).parent
appstore = HERE.parent / "store"
docstore = HERE.parent.parent / "docstore"
templates = docstore / "templates"
documents = docstore / "documents"

(models := appstore / "models").mkdir(exist_ok=True, parents=True)
(datasets := appstore / "datasets").mkdir(exist_ok=True, parents=True)
(outputs := appstore / "outputs").mkdir(exist_ok=True, parents=True)

if __name__ == "__main__":
    for path in (docstore).iterdir():
        print(path)
