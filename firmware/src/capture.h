#ifndef BLEDEV_CAPTURE_H
#define BLEDEV_CAPTURE_H

#include <stdint.h>

struct bledev_capture_stats {
	uint32_t packets_captured;
	uint32_t packets_dropped;
	uint32_t malformed_frames;
	uint64_t uptime_us;
};

int bledev_capture_init(void);
void bledev_capture_record_packet(void);
void bledev_capture_record_drop(void);
void bledev_capture_record_malformed_frame(void);
void bledev_capture_get_stats(struct bledev_capture_stats *stats);

#endif /* BLEDEV_CAPTURE_H */

