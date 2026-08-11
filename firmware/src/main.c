#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include "capture.h"
#include "radio.h"
#include "usb.h"

LOG_MODULE_REGISTER(blueglyph_main, LOG_LEVEL_INF);

int main(void)
{
	int err;

	LOG_INF("blueglyph firmware boot");

	err = blueglyph_capture_init();
	if (err != 0) {
		LOG_ERR("capture init failed: %d", err);
		return err;
	}

	err = blueglyph_radio_init();
	if (err != 0) {
		LOG_ERR("radio init failed: %d", err);
		return err;
	}

	err = blueglyph_usb_transport_init();
	if (err != 0) {
		LOG_ERR("USB transport init failed: %d", err);
		return err;
	}

	while (true) {
		struct blueglyph_capture_stats stats;

		blueglyph_capture_get_stats(&stats);
		LOG_DBG("capture idle, packets=%u dropped=%u malformed=%u",
			stats.packets_captured,
			stats.packets_dropped,
			stats.malformed_frames);
		k_sleep(K_SECONDS(1));
	}

	return 0;
}

