/**
 * Copyright 2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MATMUL_TILING_UTILS_H
#define MATMUL_TILING_UTILS_H

#include <stdint.h>
#include <sstream>
#include <cstdlib>
#include <vector>

namespace mindspore {
namespace internal {
namespace tiling {

static std::vector<int> getMatMulTilingFromEnv() {
    std::vector<int> result;
    auto env_name = "INTERNAL_MATMUL_TILING";
    const char* envVarValue = std::getenv(env_name);

    if (envVarValue != nullptr) {
        std::string envVarString(envVarValue);
        std::stringstream ss(envVarString);
        std::string item;

        while (std::getline(ss, item, ',')) {
            result.push_back(std::stoi(item));
        }
    }

    return result;
}


static bool getShuffleFlagFromEnv() {
    auto env_name = "CUSTOM_MATMUL_SHUFFLE";
    const char* envVarValue = std::getenv(env_name);
    if (envVarValue != nullptr) {
        std::string envVarString(envVarValue);
        if (envVarString != "0" && envVarString != "off") {
            return true;
        }
        return false;
    }
    return true;
}


}  // namespace tiling
}  // namespace internal
}  // namespace mindspore
#endif  // MATMUL_TILING_UTILS_H