#include "protocol.h"

#include <errno.h>

#include <zephyr/sys/byteorder.h>

int blueglyph_protocol_encode_header(uint8_t *dst, size_t dst_len,
				  const struct blueglyph_message_header *header)
{
	if (dst == NULL || header == NULL) {
		return -EINVAL;
	}
	if (dst_len < BLUEGLYPH_PROTOCOL_HEADER_SIZE) {
		return -EMSGSIZE;
	}

	sys_put_le16(BLUEGLYPH_PROTOCOL_MAGIC, &dst[0]);
	dst[2] = BLUEGLYPH_PROTOCOL_VERSION;
	dst[3] = header->message_type;
	sys_put_le16(header->payload_length, &dst[4]);
	sys_put_le32(header->sequence, &dst[6]);
	sys_put_le64(header->timestamp_us, &dst[10]);

	return 0;
}

int blueglyph_protocol_decode_header(struct blueglyph_message_header *header,
				  const uint8_t *src, size_t src_len)
{
	uint16_t magic;
	uint8_t version;

	if (header == NULL || src == NULL) {
		return -EINVAL;
	}
	if (src_len < BLUEGLYPH_PROTOCOL_HEADER_SIZE) {
		return -EMSGSIZE;
	}

	magic = sys_get_le16(&src[0]);
	if (magic != BLUEGLYPH_PROTOCOL_MAGIC) {
		return -EINVAL;
	}

	version = src[2];
	if (version != BLUEGLYPH_PROTOCOL_VERSION) {
		return -ENOTSUP;
	}

	header->message_type = src[3];
	header->payload_length = sys_get_le16(&src[4]);
	header->sequence = sys_get_le32(&src[6]);
	header->timestamp_us = sys_get_le64(&src[10]);

	return 0;
}

