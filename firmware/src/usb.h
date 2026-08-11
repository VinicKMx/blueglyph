#ifndef BLUEGLYPH_USB_H
#define BLUEGLYPH_USB_H

#include <stddef.h>
#include <stdint.h>

int blueglyph_usb_transport_init(void);
int blueglyph_usb_transport_send(const uint8_t *data, size_t len);

#endif /* BLUEGLYPH_USB_H */

