# ---- kutuphaneler ----------------------------------------------------------

add_library(fcm_core
        src/core/legendre.cpp
        src/core/gauss.cpp
        src/core/linalg.cpp
)
target_include_directories(fcm_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_library(fcm1d_lib
        src/fcm1d/config.cpp
        src/fcm1d/mesh.cpp
        src/fcm1d/partition.cpp
        src/fcm1d/quadrature.cpp
        src/fcm1d/assembly.cpp
        src/fcm1d/solver.cpp
)
target_link_libraries(fcm1d_lib PUBLIC fcm_core)

# ---- surucu ----------------------------------------------------------------

add_executable(fcm1d apps/fcm1d.cpp)
target_link_libraries(fcm1d PRIVATE fcm1d_lib)

# ---- testler ---------------------------------------------------------------

function(fcm_add_test name lib)
    add_executable(${name} tests/${name}.cpp)
    target_link_libraries(${name} PRIVATE ${lib})
    target_compile_definitions(${name} PRIVATE
            FCM_REFERENCE_DIR="${CMAKE_SOURCE_DIR}/reference")
    add_test(NAME ${name} COMMAND ${name} "${CMAKE_SOURCE_DIR}/reference")
endfunction()

fcm_add_test(test_legendre  fcm_core)
fcm_add_test(test_gauss     fcm_core)
fcm_add_test(test_mesh      fcm1d_lib)
fcm_add_test(test_partition fcm1d_lib)
fcm_add_test(test_quadrature fcm1d_lib)
fcm_add_test(test_assembly fcm1d_lib)
fcm_add_test(test_solve fcm1d_lib)

find_package(Python3 COMPONENTS Interpreter)
if(Python3_FOUND)
    add_test(NAME validation_end_to_end
            COMMAND ${Python3_EXECUTABLE} check_validation.py $<TARGET_FILE:fcm1d>
            WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/python/FCM1D)
endif()
