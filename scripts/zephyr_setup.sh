#!/usr/bin/env sh
set -eu

PROJECT_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ZEPHYR_DEV_ROOT="${ZEPHYR_DEV_ROOT:-$HOME/Documents/projetos/zephyr-dev}"
ZEPHYR_WORKSPACE="${ZEPHYR_WORKSPACE:-$ZEPHYR_DEV_ROOT/workspaces/blueglyph}"
ZEPHYR_SDK_BASE="${ZEPHYR_SDK_BASE:-$ZEPHYR_DEV_ROOT/sdk}"
ZEPHYR_CACHE_DIR="${ZEPHYR_CACHE_DIR:-$ZEPHYR_DEV_ROOT/cache}"
ZEPHYR_SDK_VERSION="${ZEPHYR_SDK_VERSION:-0.16.8}"

if command -v west >/dev/null 2>&1; then
	WEST="${WEST:-west}"
elif [ -x "$HOME/.local/bin/west" ]; then
	WEST="${WEST:-$HOME/.local/bin/west}"
else
	echo "west is required. Install it first, for example: uv tool install west" >&2
	exit 1
fi

mkdir -p "$ZEPHYR_WORKSPACE/.west" "$ZEPHYR_SDK_BASE" "$ZEPHYR_CACHE_DIR"

MANIFEST_PATH="$(python3 -c 'import os, sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "$PROJECT_ROOT" "$ZEPHYR_WORKSPACE")"

cat > "$ZEPHYR_WORKSPACE/.west/config" <<EOF
[manifest]
path = $MANIFEST_PATH
file = west.yml

[zephyr]
base = zephyr
EOF

(
	cd "$ZEPHYR_WORKSPACE"
	if [ -f "$ZEPHYR_CACHE_DIR/zephyr/config" ]; then
		"$WEST" config --local update.name-cache "$ZEPHYR_CACHE_DIR"
	else
		"$WEST" config -d --local update.name-cache >/dev/null 2>&1 || true
	fi
	"$WEST" update
	"$WEST" zephyr-export
)

WEST_EXE="$(command -v "$WEST" 2>/dev/null || printf '%s' "$WEST")"
WEST_PYTHON="$(sed -n '1s/^#!//p' "$WEST_EXE" 2>/dev/null || true)"

if [ -z "$WEST_PYTHON" ] || [ ! -x "$WEST_PYTHON" ]; then
	echo "Could not resolve the Python interpreter used by west." >&2
	exit 1
fi

"$WEST_PYTHON" -m ensurepip --upgrade

if (
	cd "$ZEPHYR_WORKSPACE"
	"$WEST" help | grep -q "packages:"
); then
	(
		cd "$ZEPHYR_WORKSPACE"
		"$WEST" packages pip --install
	)
else
	"$WEST_PYTHON" -m pip install -r "$ZEPHYR_WORKSPACE/zephyr/scripts/requirements.txt"
fi

if [ -d "$ZEPHYR_SDK_BASE/zephyr-sdk-$ZEPHYR_SDK_VERSION" ]; then
	"$ZEPHYR_SDK_BASE/zephyr-sdk-$ZEPHYR_SDK_VERSION/setup.sh" -c
else
	(
		cd "$ZEPHYR_WORKSPACE"
		"$WEST" sdk install --version "$ZEPHYR_SDK_VERSION" -b "$ZEPHYR_SDK_BASE" -t arm-zephyr-eabi
	)
fi

echo "Zephyr workspace: $ZEPHYR_WORKSPACE"
echo "Zephyr SDK base:   $ZEPHYR_SDK_BASE"
