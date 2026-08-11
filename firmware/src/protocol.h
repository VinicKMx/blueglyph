#ifndef BLEDEV_PROTOCOL_H
#define BLEDEV_PROTOCOL_H

#include <stddef.h>
#include <stdint.h>

#define BLEDEV_PROTOCOL_MAGIC 0xB1E0u
#define BLEDEV_PROTOCOL_VERSION 1u
#define BLEDEV_PROTOCOL_HEADER_SIZE 18u

enum bledev_message_type {
	BLEDEV_MSG_RADIO_PACKET = 0x01,
	BLEDEV_MSG_DEVICE_STATUS = 0x02,
	BLEDEV_MSG_CAPTURE_STATUS = 0x03,
	BLEDEV_MSG_ERROR = 0x04,
	BLEDEV_MSG_COMMAND_RESPONSE = 0x05,
	BLEDEV_MSG_FIRMWARE_INFO = 0x06,
	BLEDEV_MSG_TIME_SYNC = 0x07,
	BLEDEV_MSG_STATISTICS = 0x08,
	BLEDEV_MSG_LOG = 0x09,
};

struct bledev_message_header {
	uint8_t message_type;
	uint16_t payload_length;
	uint32_t sequence;
	uint64_t timestamp_us;
};

int bledev_protocol_encode_header(uint8_t *dst, size_t dst_len,
				  const struct bledev_message_header *header);
int bledev_protocol_decode_header(struct bledev_message_header *header,
				  const uint8_t *src, size_t src_len);

#endif /* BLEDEV_PROTOCOL_H */

