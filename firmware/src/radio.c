#include "radio.h"

#include <errno.h>
#include <stdbool.h>

#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(blueglyph_radio, LOG_LEVEL_INF);

static bool radio_initialized;
static bool radio_capturing;
static uint8_t selected_channel = 37;

int blueglyph_radio_init(void)
{
	radio_initialized = true;
	radio_capturing = false;
	LOG_INF("radio module initialized for future nRF52840 direct RADIO capture");
	return 0;
}

int blueglyph_radio_set_channel(uint8_t channel)
{
	if (!radio_initialized) {
		return -EAGAIN;
	}
	if (channel > 39) {
		return -EINVAL;
	}

	selected_channel = channel;
	LOG_DBG("radio channel set to %u", selected_channel);
	return 0;
}

int blueglyph_radio_start_passive_scan(void)
{
	if (!radio_initialized) {
		return -EAGAIN;
	}

	radio_capturing = true;
	LOG_INF("passive scan requested; hardware capture implementation is pending");
	return 0;
}

int blueglyph_radio_stop(void)
{
	radio_capturing = false;
	LOG_INF("radio capture stopped");
	return 0;
}

