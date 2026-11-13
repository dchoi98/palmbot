# The following five lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.22)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)

if(NOT EXISTS "${CMAKE_CURRENT_LIST_DIR}/secrets.cmake")
    message(FATAL_ERROR
        "secrets.cmake not found — copy secrets.cmake.example to "
        "secrets.cmake and add your WiFi credentials.")
endif()
include(secrets.cmake)

project(firmware)
