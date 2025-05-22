from cx_Freeze import setup, Executable


build_exe_options = {
    "packages": ["os"],
    "include_files": [
        ("assets", "assets"),
    ],  # (source, target) tuple
}
  
setup(
    name = "CashCade",
    version = "0.1.0",
    options = {"build_exe": build_exe_options},
    description = "CashCade: Catch the CashFlow",
    executables = [Executable("main.py")],
)


