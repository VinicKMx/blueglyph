#ifndef BLUEGLYPH_RADIO_H
#define BLUEGLYPH_RADIO_H

#include <stdint.h>

int blueglyph_radio_init(void);
int blueglyph_radio_set_channel(uint8_t channel);
int blueglyph_radio_start_passive_scan(void);
int blueglyph_radio_stop(void);

#endif /* BLUEGLYPH_RADIO_H */

