"""Vérifie les outils nécessaires aux labs IA132.

    python scripts/verifier_env.py
"""

import shutil
import subprocess
import sys

OK, KO = "  [ok] ", "  [!!] "


def version(cmd: list[str]) -> str | None:
    exe = shutil.which(cmd[0])
    if not exe:
        return None
    try:
        out = subprocess.run([exe, *cmd[1:]], capture_output=True, text=True, timeout=15)  # noqa: S603
    except (OSError, subprocess.SubprocessError):
        return None
    return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else None


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    problemes = 0
    print("Labs IA132 · vérification de l'environnement\n")

    py = sys.version_info
    if py >= (3, 10):
        print(f"{OK}Python {py.major}.{py.minor}.{py.micro}")
    else:
        print(f"{KO}Python {py.major}.{py.minor} : il faut 3.10 ou plus récent")
        problemes += 1

    for module, role in (("pytest", "tests Python"), ("pytest_cov", "couverture (lab 08)")):
        try:
            __import__(module)
            print(f"{OK}{module} ({role})")
        except ImportError:
            print(f"{KO}{module} manquant : pip install -r requirements-dev.txt")
            problemes += 1

    ruff = version(["ruff", "--version"]) or version([sys.executable, "-m", "ruff", "--version"])
    print(f"{OK}{ruff}" if ruff else f"{KO}ruff manquant (labs 03 et 07) : pip install -r requirements-dev.txt")
    problemes += 0 if ruff else 1

    git = version(["git", "--version"])
    print(f"{OK}{git}" if git else f"{KO}git introuvable")
    problemes += 0 if git else 1

    node = version(["node", "--version"])
    if node:
        major, minor = (int(x) for x in node.lstrip("v").split(".")[:2])
        if (major, minor) >= (22, 18):
            print(f"{OK}Node.js {node} (TypeScript exécuté directement)")
        else:
            print(f"{KO}Node.js {node} : il faut 22.18 ou plus récent pour les labs TypeScript")
            problemes += 1
    else:
        print(f"{KO}Node.js introuvable (facultatif si vous faites les labs en Python)")

    print("\nTout est prêt !" if problemes == 0 else f"\n{problemes} point(s) à corriger.")
    return 0 if problemes == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
