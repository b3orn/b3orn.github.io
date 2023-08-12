SRC_DIR=src
BUILD_DIR=build
TEMPLATE_DIR=templates
ENV_FILE=fac3.yaml

.PHONY: all clean

all:
	python fac3.py --env ${ENV_FILE} --build-dir ${BUILD_DIR} --template-dir ${TEMPLATE_DIR} ${SRC_DIR}

clean:
	-rm -rf ${BUILD_DIR}
