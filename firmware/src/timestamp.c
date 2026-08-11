#include "timestamp.h"

#include <zephyr/kernel.h>

uint64_t blueglyph_timestamp_now_us(void)
{
	return k_ticks_to_us_floor64(k_uptime_ticks());
}

