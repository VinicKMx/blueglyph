#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

#include "capture.h"
#include "radio.h"
#include "usb.h"

LOG_MODULE_REGISTER(bledev_main, LOG_LEVEL_INF);

int main(void)
{
	int err;

	LOG_INF("bledev firmware boot");

	err = bledev_capture_init();
	if (err != 0) {
		LOG_ERR("capture init failed: %d", err);
		return err;
	}

	err = bledev_radio_init();
	if (err != 0) {
		LOG_ERR("radio init failed: %d", err);
		return err;
	}

	err = bledev_usb_transport_init();
	if (err != 0) {
		LOG_ERR("USB transport init failed: %d", err);
		return err;
	}

	while (true) {
		struct bledev_capture_stats stats;

		bledev_capture_get_stats(&stats);
		LOG_DBG("capture idle, packets=%u dropped=%u malformed=%u",
			stats.packets_captured,
			stats.packets_dropped,
			stats.malformed_frames);
		k_sleep(K_SECONDS(1));
	}

	return 0;
}

