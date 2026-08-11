#ifndef BLUEGLYPH_CAPTURE_H
#define BLUEGLYPH_CAPTURE_H

#include <stdint.h>

struct blueglyph_capture_stats {
	uint32_t packets_captured;
	uint32_t packets_dropped;
	uint32_t malformed_frames;
	uint64_t uptime_us;
};

int blueglyph_capture_init(void);
void blueglyph_capture_record_packet(void);
void blueglyph_capture_record_drop(void);
void blueglyph_capture_record_malformed_frame(void);
void blueglyph_capture_get_stats(struct blueglyph_capture_stats *stats);

#endif /* BLUEGLYPH_CAPTURE_H */

