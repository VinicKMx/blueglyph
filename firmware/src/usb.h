#ifndef BLEDEV_USB_H
#define BLEDEV_USB_H

#include <stddef.h>
#include <stdint.h>

int bledev_usb_transport_init(void);
int bledev_usb_transport_send(const uint8_t *data, size_t len);

#endif /* BLEDEV_USB_H */

