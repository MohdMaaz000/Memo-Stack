import subprocess

result = subprocess.run(
    ["venv\\Scripts\\python.exe", "-m", "pytest", "tests/", "-v", "--tb=short"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)
with open("test_log.txt", "w", encoding="utf-8") as f:
    f.write(result.stdout)
    f.write(result.stderr)
print("Done writing to test_log.txt")
