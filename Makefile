PROTO_TAG ?= v0.0.1
PROTO_NAME := comment.proto

TMP_DIR := .build/proto
OUT_DIR := gen/python

.PHONY: clean fetch-proto gen-stubs update

clean:
	rm -rf $(TMP_DIR) $(OUT_DIR)

fetch-proto:
	mkdir -p $(TMP_DIR)
	wget \
		https://raw.githubusercontent.com/esclient/protos/$(PROTO_TAG)/$(PROTO_NAME) \
		-O $(TMP_DIR)/$(PROTO_NAME)

gen-stubs: fetch-proto
	mkdir -p $(OUT_DIR)
	python3 -m grpc_tools.protoc \
		--proto_path=$(TMP_DIR) \
		--python_out=$(OUT_DIR) \
		--grpc_python_out=$(OUT_DIR) \
		--pyi_out=$(OUT_DIR) \
		$(TMP_DIR)/$(PROTO_NAME)

update: clean gen-stubs
