#ifndef BLUEGLYPH_PROTOCOL_H
#define BLUEGLYPH_PROTOCOL_H

#include <stddef.h>
#include <stdint.h>

#define BLUEGLYPH_PROTOCOL_MAGIC 0xB1E0u
#define BLUEGLYPH_PROTOCOL_VERSION 1u
#define BLUEGLYPH_PROTOCOL_HEADER_SIZE 18u

enum blueglyph_message_type {
	BLUEGLYPH_MSG_RADIO_PACKET = 0x01,
	BLUEGLYPH_MSG_DEVICE_STATUS = 0x02,
	BLUEGLYPH_MSG_CAPTURE_STATUS = 0x03,
	BLUEGLYPH_MSG_ERROR = 0x04,
	BLUEGLYPH_MSG_COMMAND_RESPONSE = 0x05,
	BLUEGLYPH_MSG_FIRMWARE_INFO = 0x06,
	BLUEGLYPH_MSG_TIME_SYNC = 0x07,
	BLUEGLYPH_MSG_STATISTICS = 0x08,
	BLUEGLYPH_MSG_LOG = 0x09,
};

struct blueglyph_message_header {
	uint8_t message_type;
	uint16_t payload_length;
	uint32_t sequence;
	uint64_t timestamp_us;
};

int blueglyph_protocol_encode_header(uint8_t *dst, size_t dst_len,
				  const struct blueglyph_message_header *header);
int blueglyph_protocol_decode_header(struct blueglyph_message_header *header,
				  const uint8_t *src, size_t src_len);

#endif /* BLUEGLYPH_PROTOCOL_H */

