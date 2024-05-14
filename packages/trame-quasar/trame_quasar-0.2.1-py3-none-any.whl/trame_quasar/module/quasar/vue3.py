from pathlib import Path

serve_path = str(Path(__file__).with_name("vue3").resolve())
serve = {"__trame_quasar": serve_path }
scripts = [
    "__trame_quasar/1.js",
    "__trame_quasar/trame_utils.js",
]
styles = [
    "__trame_quasar/fonts.css",
    "__trame_quasar/2.css",
]
vue_use = [
    "Quasar",
]
