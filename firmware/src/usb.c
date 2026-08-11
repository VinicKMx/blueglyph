#include "usb.h"

#include <errno.h>

#include <zephyr/logging/log.h>
#include <zephyr/sys/util.h>

LOG_MODULE_REGISTER(bledev_usb, LOG_LEVEL_INF);

int bledev_usb_transport_init(void)
{
	LOG_INF("USB transport module initialized; endpoint binding is pending");
	return 0;
}

int bledev_usb_transport_send(const uint8_t *data, size_t len)
{
	ARG_UNUSED(data);
	ARG_UNUSED(len);

	return -ENOTSUP;
}
