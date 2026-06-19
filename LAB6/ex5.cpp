#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::map<std::string, std::vector<int>> gradebook = {
        {"alice",   {90, 85, 92}},
        {"bob",     {78, 88}},
        {"charlie", {95, 70, 80}},
    };

    // Reparat: Pentru sortare trebuie sa folosim un vector de perechi (map nu se poate sorta asa)
    std::vector<std::pair<std::string, int>> averages;
    for (auto& [name, scores] : gradebook) {
        int sum = 0;
        for (int s : scores) sum += s;
        averages.push_back({name, sum / scores.size()});
    }

    // Sortam vectorul dupa medie (accesand a.second)
    std::sort(averages.begin(), averages.end(), [](const auto& a, const auto& b) {
        return a.second < b.second;
    });

    std::cout << "Rankings:" << std::endl;
    for (auto& pair : averages) {
        std::cout << "  " << pair.first << ": " << pair.second << std::endl;
    }

    return 0;
}