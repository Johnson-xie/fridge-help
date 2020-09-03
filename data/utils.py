import os

layer_map = {
    '28-1b20292fb8ff': '顶一里',
    '28-1b20292fb4ff': '顶一外',
    '28-1b20293100ff': '顶二里',
    '28-1b2029314eff': '顶二外',
    '28-1b202933b1ff': '顶三里',
    '28-1b20292f50ff': '顶三外',
}


def get_cache_html():
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'caches')
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    return {file.split('.')[0] for file in os.listdir(cache_path) if file.endswith('html')}


print(get_cache_html())