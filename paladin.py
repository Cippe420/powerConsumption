import os

def elimina_png(root_path):
    for root, _, files in os.walk(root_path):
        for file in files:
            if file.endswith(".png"):
                file_path = os.path.join(root, file)
                os.remove(file_path)

# Specifica la directory di partenza
root_directory = "tests"

elimina_png(root_directory)