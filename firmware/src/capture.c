#include "capture.h"

#include <string.h>

#include "timestamp.h"

static struct bledev_capture_stats capture_stats;

int bledev_capture_init(void)
{
	memset(&capture_stats, 0, sizeof(capture_stats));
	return 0;
}

void bledev_capture_record_packet(void)
{
	capture_stats.packets_captured++;
}

void bledev_capture_record_drop(void)
{
	capture_stats.packets_dropped++;
}

void bledev_capture_record_malformed_frame(void)
{
	capture_stats.malformed_frames++;
}

void bledev_capture_get_stats(struct bledev_capture_stats *stats)
{
	if (stats == NULL) {
		return;
	}

	*stats = capture_stats;
	stats->uptime_us = bledev_timestamp_now_us();
}
