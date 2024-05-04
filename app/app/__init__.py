from pathlib import Path

HERE = Path(__file__).parent
appstore = HERE.parent / "store"
docstore = HERE.parent.parent / "docstore"
templates = docstore / "templates"
documents = docstore / "documents"
print(f"appstore path: {appstore}")
print(f"docstore path: {docstore}")

(models := appstore / "models").mkdir(exist_ok=True, parents=True)
(datasets := appstore / "datasets").mkdir(exist_ok=True, parents=True)
(outputs := appstore / "outputs").mkdir(exist_ok=True, parents=True)

(robot_dataset := datasets / "robot_maintenance").mkdir(exist_ok=True, parents=True)

if __name__ == "__main__":
    for path in (docstore).iterdir():
        print(path)
    #for path in here.parents:
    #    print(path)
    #    
        #/Users/Fr333y3d3a/repos/mlops_capstone/store/documents