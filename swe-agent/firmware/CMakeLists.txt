cmake_minimum_required(VERSION 3.20)
project(swe_agent_seed C)

set(CMAKE_C_STANDARD 11)

add_executable(firmware.elf
    src/main.c
    src/protection.c
    src/startup_stm32g474.c
)

target_include_directories(firmware.elf PRIVATE src)

set(LINKER_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/ld/stm32g474re.ld)
target_link_options(firmware.elf PRIVATE
    -T${LINKER_SCRIPT}
    -Wl,-Map=${CMAKE_CURRENT_BINARY_DIR}/firmware.map
)
set_target_properties(firmware.elf PROPERTIES LINK_DEPENDS ${LINKER_SCRIPT})

# 构建后产出 size 报告(gate 的断言输入)
add_custom_command(TARGET firmware.elf POST_BUILD
    COMMAND ${CMAKE_SIZE} --format=berkeley $<TARGET_FILE:firmware.elf> > ${CMAKE_CURRENT_BINARY_DIR}/size.txt
    COMMAND ${CMAKE_SIZE} --format=berkeley $<TARGET_FILE:firmware.elf>
)
