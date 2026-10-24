#!/usr/bin/env python3
"""Patch an upstream Unciv checkout to avoid Ktor CIO's 8192-byte HTTP line limit.

This addresses a verified Android mod-download exception:
io.ktor.utils.io.charsets.TooLongLineException: Line exceeds limit of 8192 bytes

Only changes the Ktor engine from CIO to OkHttp. The Android test build receives
a distinct app id so it can coexist with an official installation. Unciv source
remains upstream; no user saves or official app signing keys are changed.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

def replace_one(path, original, replacement):
    p = root / path
    source = p.read_text(encoding="utf-8")
    if source.count(original) != 1:
        raise RuntimeError(f"Expected 1 match of {original!r} in {path}, found {source.count(original)}")
    p.write_text(source.replace(original, replacement), encoding="utf-8")
    print(f"Patched {path}")

replace_one(
    "core/src/com/unciv/logic/UncivKtor.kt",
    "import io.ktor.client.engine.cio.*",
    "import io.ktor.client.engine.okhttp.*"
)
replace_one(
    "core/src/com/unciv/logic/UncivKtor.kt",
    "val client = HttpClient(CIO) {",
    "val client = HttpClient(OkHttp) {"
)
replace_one(
    "gradle/libs.versions.toml",
    'ktor-client-cio = { group = "io.ktor", name = "ktor-client-cio", version.ref = "ktor" }',
    'ktor-client-cio = { group = "io.ktor", name = "ktor-client-cio", version.ref = "ktor" }\nktor-client-okhttp = { group = "io.ktor", name = "ktor-client-okhttp", version.ref = "ktor" }'
)
replace_one(
    "gradle/libs.versions.toml",
    '    "ktor-client-core", "ktor-client-cio",',
    '    "ktor-client-core", "ktor-client-cio", "ktor-client-okhttp",'
)
# Debug build should install alongside original game instead of replacing it.
replace_one(
    "android/build.gradle.kts",
    "        debug {\n            isDebuggable = true",
    '        debug {\n            applicationIdSuffix = ".httpfix"\n            isDebuggable = true'
)
print("PASS: OkHttp client selected; Ktor OkHttp dependency included; test build application ID suffixed with .httpfix")
