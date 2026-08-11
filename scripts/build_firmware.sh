#!/usr/bin/env sh
set -eu

PROJECT_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ZEPHYR_DEV_ROOT="${ZEPHYR_DEV_ROOT:-$HOME/Documents/projetos/zephyr-dev}"
ZEPHYR_WORKSPACE="${ZEPHYR_WORKSPACE:-$ZEPHYR_DEV_ROOT/workspaces/blueglyph}"
ZEPHYR_SDK_BASE="${ZEPHYR_SDK_BASE:-$ZEPHYR_DEV_ROOT/sdk}"
ZEPHYR_SDK_VERSION="${ZEPHYR_SDK_VERSION:-0.16.8}"
ZEPHYR_SDK_INSTALL_DIR="${ZEPHYR_SDK_INSTALL_DIR:-$ZEPHYR_SDK_BASE/zephyr-sdk-$ZEPHYR_SDK_VERSION}"

if command -v west >/dev/null 2>&1; then
	WEST="${WEST:-west}"
elif [ -x "$HOME/.local/bin/west" ]; then
	WEST="${WEST:-$HOME/.local/bin/west}"
else
	echo "west is required. Install it first, for example: uv tool install west" >&2
	exit 1
fi

if [ ! -f "$ZEPHYR_WORKSPACE/.west/config" ]; then
	echo "Zephyr workspace is not configured: $ZEPHYR_WORKSPACE" >&2
	echo "Run scripts/zephyr_setup.sh first." >&2
	exit 1
fi

if [ ! -d "$ZEPHYR_SDK_INSTALL_DIR" ]; then
	echo "Zephyr SDK is not installed: $ZEPHYR_SDK_INSTALL_DIR" >&2
	echo "Run scripts/zephyr_setup.sh first." >&2
	exit 1
fi

if [ "$#" -gt 0 ]; then
	BOARDS="$*"
elif [ -n "${BOARD:-}" ]; then
	BOARDS="$BOARD"
else
	BOARDS="nrf52840dk/nrf52840 nrf52840dongle/nrf52840"
fi

for board in $BOARDS; do
	build_name="$(printf '%s' "$board" | tr '/ ' '__')"
	(
		cd "$ZEPHYR_WORKSPACE"
		ZEPHYR_TOOLCHAIN_VARIANT=zephyr \
		ZEPHYR_SDK_INSTALL_DIR="$ZEPHYR_SDK_INSTALL_DIR" \
			"$WEST" build -p always -s "$PROJECT_ROOT/firmware" -b "$board" -d "build/blueglyph-$build_name"
	)
done
