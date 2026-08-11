#ifndef BLEDEV_RADIO_H
#define BLEDEV_RADIO_H

#include <stdint.h>

int bledev_radio_init(void);
int bledev_radio_set_channel(uint8_t channel);
int bledev_radio_start_passive_scan(void);
int bledev_radio_stop(void);

#endif /* BLEDEV_RADIO_H */

