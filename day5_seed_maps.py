import sys
import copy


def read_file(filename):
    with open(filename, 'r', encoding='utf8') as fh:
        maps = {}
        for line in fh.readlines():
            line = line.strip()
            if line.startswith("seeds"):
                seeds = [int(n) for n in line.split(":")[1].split(" ") if n]
            elif line.endswith("map:"):
                map_name = line.split(" ")[0]
                maps[map_name] = []
            elif not line:
                pass
            else:
                maps[map_name].append([int(n) for n in line.split(" ")])
    return seeds, maps


class Map:
    def __init__(self, name, map_list):
        self.name = name
        self.src, _, self.dst = name.split('-')
        self.map_items = sorted([MapItem(*item) for item in map_list], key=lambda x: x.min_s)

    def map(self, src_num):
        for map_item in self.map_items:
            if map_item.min_s <= src_num <= map_item.max_s:
                delta = src_num - map_item.min_s
                return map_item.min_d + delta
        return src_num

    def map_range(self, min_src_num, max_src_num):
        scratch_map_items = copy.deepcopy(self.map_items)
        current_min = min_src_num
        res_ranges = []
        current_item = scratch_map_items.pop(0)
        while current_min < max_src_num:
            if current_min < current_item.min_s:
                res_ranges.append(PropertyRange(current_min, current_item.min_s - 1))
                current_min = current_item.min_s
            elif current_item.min_s <= current_min <= current_item.max_s:
                delta = current_min - current_item.min_s
                if max_src_num <= current_item.max_s:
                    res_ranges.append(PropertyRange(current_item.min_d + delta,
                                                    current_item.min_d + delta + max_src_num - current_min))
                    current_min = max_src_num
                elif max_src_num > current_item.max_s:
                    res_ranges.append(PropertyRange(current_item.min_d + delta,
                                                    current_item.min_d + delta + current_item.max_s - current_min))
                    current_min = current_item.max_s + 1
            elif current_min > current_item.max_s:
                try:
                    current_item = scratch_map_items.pop(0)
                except IndexError:
                    res_ranges.append(PropertyRange(current_min, max_src_num))
                    current_min = current_item.max_s + 1
        return res_ranges


class MapItem:
    def __init__(self, min_d, min_s, range_len):
        self.min_s, self.min_d = min_s, min_d
        self.max_s, self.max_d = self.min_s + range_len - 1, self.min_d + range_len - 1
        self.range_len = range_len

    def __repr__(self):
        return f"({self.min_s}..{self.max_s} -> {self.min_d}..{self.max_d} [{self.min_d-self.min_s}])"


def location_from_seed(seed, maps):
    # order = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
    level = "seed"
    level_value = seed
    while level != "location":
        from_level, _, to_level = [x for x in maps.keys() if x.startswith(level)][0].split("-")
        current_map = maps[f"{from_level}-to-{to_level}"]
        level_value = current_map.map(level_value)
        level = to_level
    return level_value


def locations_from_seeds(level_range, maps):
    level = "seed"
    level_values = [level_range]
    while level != "location":
        from_level, _, to_level = [x for x in maps.keys() if x.startswith(level)][0].split("-")
        current_map = maps[f"{from_level}-to-{to_level}"]
        new_level_values = []
        for level_value in level_values:
            new_level_values.extend(current_map.map_range(level_value.start, level_value.end))
        level_values = new_level_values
        level = to_level
    return level_values


class PropertyRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"({self.start}..{self.end})"


if __name__ == '__main__':
    input_file = sys.argv[1]
    try:
        part = sys.argv[2]
    except IndexError:
        print("Specify the task part")
        exit(1)

    input_seeds, input_maps_dict = read_file(input_file)
    input_maps = {k: Map(k, input_maps_dict[k]) for k in input_maps_dict}
    locations = []

    if part == "1":
        for input_seed in input_seeds:
            locations.append(location_from_seed(input_seed, input_maps))
        print("Min location:", min(locations))
    elif part == "2":
        seed_ranges = [PropertyRange(input_seeds[i], input_seeds[i] + input_seeds[i + 1] - 1)
                       for i in range(0, len(input_seeds), 2)]
        for seed_range in seed_ranges:
            locations.extend(locations_from_seeds(seed_range, input_maps))
        print("Min location:", min(locations, key=lambda x: x.start).start)
