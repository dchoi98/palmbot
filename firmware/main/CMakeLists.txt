idf_component_register(SRCS "main.cpp"
                    INCLUDE_DIRS ".")

target_compile_definitions(${COMPONENT_LIB} PRIVATE
    WIFI_SSID=\"${WIFI_SSID}\"
    WIFI_PASSWORD=\"${WIFI_PASSWORD}\"
)
